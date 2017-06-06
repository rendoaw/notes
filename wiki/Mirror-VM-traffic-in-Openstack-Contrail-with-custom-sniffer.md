# Mirror VM traffic in Openstack Contrail with custom sniffer

The proper way to mirror VM traffic in Contrail is by using its analyzer VM as documented in 
* (https://www.juniper.net/documentation/en_US/contrail3.0/topics/task/configuration/configure-traffic-analyzer-vnc.html)

If you follow one of the procedures that documented in the link above, Analyzer VM will automatically give you a wireshark via VNC console. This is good enough for quick troubleshooting purpose, but i started to have a problem if i want to generate and download the pcap file. 

> note: we can always doing tcpdump on VM tap interface but it is not the focus of this post


I don't know what is the credential to access the Analyzer VM (probably there is none), so i want to use my own linux VM as the sniffer. 

Here is what i have done and what i found:


## Launch a linux VM as a sniffer instance

To use we own VM as sniffer VM, we need to launch the VM as an Service Instance. Basically we will do the same as the official procedure but we are going to use our own VM image, not the analyzer VM.

* Upload the VM

    * Since it seems there is no way to specify ssh key pair or any cloud init configuration when launching a VM as Contrail Service Instance, we need to make sure we inject a default username/password inside the VM. 

    * In my case, i am using a minimal ubuntu image which the following changes:
        * set default root password
        * allow root ssh access using password inside sshd.conf
        * enable dhcp client on eth0 interface

    * Upload the image to glance as usual
        * for further reference, let's call this image name: ubuntu-sniffer

* Create a service template

    * Go to Contrail web UI -> Configure -> Services -> Service Templates

    * Click on '+' to create a new template, and use the following entries:
        * Put any name
            * for further reference in this post, i use name = st-mirror
        * Version: v1
        * Virtualization type: Virtual Machine
        * Service mode: transparent
        * Service type: Analyzer
        * Image name: ubuntu-sniffer - or any name that we assign when we upload the image -
        * Instance flavor: - select any appropriate flavor -
        * Interfaces: one should be enough, but for flexibility i add 2 interfaces
            * first interface: management
                * i will use this interface to access the VM and run tcpdump or any other sniffing tool
            * second interface: left
                * I will use this interface to receive the mirrored packet


* Create a service instance

    * Go to Contrail web UI -> Configure -> Services -> Service Instances     

    * Click on '+' to create a new instance, and use the following entries:
        * Put any name
            * for further reference, let put name: capture1
        * Service template: st-mirror - or any service template name that we just created in previous step - 
        * Number of instance: 1
        * HA mode: none
        * Interface type: 
            * management: attach to any virtual network that you can access
            * left: doesn't really matter, we can choose auto-configured


* wait until the service VM is spawned and up



## Setup the sniffer

* create a network policy
    
    * this is required to enable the packet mirroring on specific virtual network

    * Go to Contrail web UI -> Configure -> Networking -> Policies

    * Click on '+' to create a new policy, and use the following entries:
        * Put any name
            * for further reference, let say name: policy_capture
        * add rule
            * adjust the rule depending on what traffic that we want to mirror
            * check the "mirror" option
        * mirror
            * select the service instance that we created in previous step, in this example: we choose 'capture1'


* apply the capture policy to the virtual network

    * Go to Contrail web UI -> Configure -> Networking -> Networks
    
    * find the virtual network that the target VM interface is attached to
    
    * modify the network
    
    * add the mirror policy to existng network policies
        * in this example, add policy_capture to existing network policies




## Sniff the mirrored packet

In my example above, i assigned second interface as left interface, this means the mirrored packet will be sent to this interface. Before we continue to decode the mirrored packets, let go back and see what is the actual wireshark output from the official Analyzer VM. 


![analyzer vm wireshark output](https://raw.github.com/rendoaw/notes/master/images/wireshark_in_analyzer_vm.png)

From the output above, we can see that the mirrored packet received by Analyzer VM with some additional headers. 
Yes, vrouter will send the mirrored packet to the sniffer encapsulated inside UDP port 8099 with some additional header describing about which the virtual-network that the mirroring was performed.


OK, now let try to run tcpdump on our own custom sniffer VM. Here is what i got

    ```
    root@capture1001:~# tcpdump -s 0 -n -i eth1
    tcpdump: WARNING: eth1: no IPv4 address assigned
    tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
    listening on eth1, link-type EN10MB (Ethernet), capture size 65535 bytes
    20:33:49.627119 IP 100.64.1.10.61378 > 100.64.1.17.8099: UDP, length 170
    20:33:49.627182 IP 100.64.1.10.21994 > 100.64.1.17.8099: UDP, length 170
    20:33:49.627193 IP 10.250.2.252.53471 > 100.64.1.17.8099: UDP, length 317
    20:33:50.632005 IP 100.64.1.10.61378 > 100.64.1.17.8099: UDP, length 170
    ...
    ```

As expected, sniffer receives UDP encapsulated packets. I went to try again and this time i save it to a pcap file then open it via wireshark on my pc.

Here is the result from wireshark, it can't decode UDP 8099. 

![wireshark output vanilla](https://raw.github.com/rendoaw/notes/master/images/contrail_wireshark_vanilla.png)


I also found out that there is a Lua-based custom dissectore provided by Contrail installation, they are:
* /usr/share/contrail-utils/agent_dissector.lua 
* /usr/share/contrail-utils/mpls_dissector.lua

I loaded them into wireshark and try to decode again. It's a bit better now, it can decode some of the headers but it still can't decode the original mirrored packets.

![wireshark output with agent_dissector](https://raw.github.com/rendoaw/notes/master/images/contrail_wireshark_with_agent_dissector.png)


So far, i have no idea where to get the proper dissector. Maybe later i will modify the agent_dissector to be able to decode the original packets, but for now, i'll take the simple approach but removing the contrail header from original packet manually using editcap. 


Looking back to the wireshark output above, and since i know the VM interface that i mirrored the packet from has MAC address start with 00:00:5e, i can guess that the original packet start from byte 0x72 (114 decimal). 
So, let's remove the first 114 byte from the pcap file

```
# editcap -C 114 -F pcap contrail-mirror.pcap contrail-mirror-no-header.pcap
```

Now, if we open contrail-mirror-no-header.pcap, we will see the original mirrored packets.

![wireshark output no header](https://raw.github.com/rendoaw/notes/master/images/contrail_wireshark_no_header.png)



## Conclusion

* It is possible to mirror the VM traffic without official Analyzer VM, although it a bit tricky.

* Ideally, if Analyzer VM can provide ssh access into it, then we don't need to go this hard way.

* As a side note, it would be nice if we have the following:

    * ability to specify ssh key pair when launching a service instance VM

    * ability to use cloud init when launching a service instance VM

* This is maybe supported but i don't know how to do it yet, i want to create service template and launch service instance VMs via HEAT template. 



