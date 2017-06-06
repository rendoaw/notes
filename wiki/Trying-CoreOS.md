# Trying CoreOS

## Overview
* CoreOS is a lot different compared with other normal Linux distros. 
* CoreOS does not have its own package manager and expect to run application inside docker container.
* CoreOS has built-in clustering support, mainly managed by etcd and fleet.


## Creating first CoreOS machine

#### Installing CoreOS

For this purpose, i wanted to try CoreOS on VM, in this case is a KVM-based VM.

```
Lesson #1:

CoreOS ISO does not provide a complete installation mechanism like CentOS anaconda or Ubuntu installer. 
CoreOS ISO actually is an live CD, which allow you to download CoreOS image from internet and re-image your hard drive. 

note: i don't know how to do offline CoreOS installation yet.
```

For the installation procedure, i was following https://coreos.com/os/docs/latest/installing-to-disk.html


#### Booting CoreOS

```
Lesson #2:

Although we installed CoreOS using "ISO", the result is similar as if you are using other distro ready-made cloud image. 
By default, CoreOS fresh system has no username/password set. 
```

How do you set the default credential?
Apparently, there are 2 common ways to do this:

* Option 1:
  * Create a cloud-config file, and use it when you run coreos-install, e.g:
  
    ```
    # coreos-install -d /dev/sda -c cloud-config.yaml
    ```
  
  * example of the cloud-config
  
    ```
    #cloud-config
    
    hostname: coreos
    users:
      - name: "rendo"
        passwd: "$1$9DHHJV.z$vY1BrX8dK4tgALvg6DWHz0"
        groups:
          - "sudo"
          - "docker"
    ```

  * this method actually works once, but i have hard time to reproduce it. The problem is not on the cloud config itself, but more on the coreos-install script. 
    * For some reason, i got "BLKRRPART: Device or resource busy" more frequently if i use "-c <cloud config filename>" parameters.
    * seems i am hitting the same issue as https://github.com/coreos/bugs/issues/152
  

* Option 2:
  * The second approach basially is using standard installation without any username/password set
  * Then, similar as what we do with any cloud-init based image, we use cloud-init config to "initialize" the VM
  * Since i am running CoreOS on KVM, i don't have metadata service, so i have to use config-drivae to inject my cloud-init configuration.
  * Procedure:
    * Create an ISO file contains the the cloud init config, e.g:
    
      ```
      # cat coreos/openstack/latest/user_data
      #cloud-config
      
      hostname: coreos
      users:
        - name: "rendo"
          passwd: "$1$9DHHJV.z$vY1BrX8dK4tgALvg6DWHz0"
          groups:
            - "sudo"
            - "docker"
            
      ```
  
    * create the ISO
      
      ```
      # mkisofs -R -V config-2 -o coreos-configdrive.iso coreos
      ```

    * attach the ISO as 2nd disk on KVM VM
    
      ```
      # virsh dumpxml coreos
      
      ...deleted..
      
      <disk type='file' device='cdrom'>
        <driver name='qemu' type='raw'/>
        <source file='/data/kvm/coreos/coreos-configdrive.iso'/>
        <target dev='hda' bus='ide'/>
        <readonly/>
        <boot order='2'/>
        <address type='drive' controller='0' bus='0' target='0' unit='0'/>
      </disk>
      <disk type='file' device='disk'>
        <driver name='qemu' type='qcow2'/>
        <source file='/data/kvm/coreos/coreos.qcow2'/>
        <target dev='vda' bus='virtio'/>
        <boot order='1'/>
        <address type='pci' domain='0x0000' bus='0x00' slot='0x07' function='0x0'/>
      </disk>
      
      ..deleted..
      ```
    
    * start the CoreOS VM
    
  * we should be able to login with user/password as specified in the cloud-init file
  
  
#### Static IP instead of DHCP

* By default CoreOS will use DHCP to get the IP. To use static IP, I was modifying the cloud-init as below

    ```
    #cloud-config
    
    hostname: coreos
    users:
      - name: "rendo"
        passwd: "$1$9DHHJV.z$vY1BrX8dK4tgALvg6DWHz0"
        groups:
          - "sudo"
          - "docker"
    
    write_files:
    
    coreos:
      units:
        - name: 00-eth0.network
          permissions: 0644
          runtime: true
          content: |
            [Match]
            Name=eth0
    
            [Network]
            Address=192.168.1.23/24
            Gateway=192.168.1.1
            DNS=8.8.8.8
            DNS=8.8.4.4
        - name: systemd-networkd.service
          command: start    
    ```
    

## Trying CoreOS clustering

I was following the great tutorial provided by Digital Ocean: https://www.digitalocean.com/community/tutorials/an-introduction-to-coreos-system-components
Almost everything from the tutorial as working as expected but I do have some issues that mainly because of my specific setup. 

#### Setup Overview

* I created 3 CoreOS VM to test clustering

#### List of issues

* etcd2 discovery service is not working

    * i am using discovery.etcd.io as discovery service
    
        ```
        # curl --silent -H "Accept: text/plain" https://discovery.etcd.io/new?size=3
        ```
    
    * Error messages
    
        ```
        Jun 05 23:42:01 coreos-1 etcd2[914]: member "2987153e1354f8c11c8360f6fd80a02d" has previously registered with discovery service token (https://discovery.etcd.io/cb525330fb8159eed9ff784287608e5b).
        Jun 05 23:42:01 coreos-1 etcd2[914]: But etcd could not find valid cluster configuration in the given data dir (/var/lib/etcd2).
        ```
    
    * I am not 100% sure about the root cause, but most likely it because all my CoreOS instances are behind N-to-1 NAT. In this case, all 3 nodes are using the same Public IP.

    * To solve this issue, i am using static etcd2 configuration. I changed my cloud-init to be something like this:
    
        ```
        #cloud-config
        
        hostname: coreos-1
        users:
          - name: "rendo"
            passwd: "$1$9DHHJV.z$vY1BrX8dK4tgALvg6DWHz0"
            groups:
              - "sudo"
              - "docker"
        
        write_files:
        
        coreos:
          etcd2:
            name: coreos-1
            initial-advertise-peer-urls: http://192.168.1.24:2380               ---> adjust this with each node IP
            listen-peer-urls: http://192.168.1.24:2380                          ---> adjust this with each node IP
            listen-client-urls: http://192.168.1.24:2379,http://127.0.0.1:2379  ---> adjust this with each node IP
            advertise-client-urls: http://192.168.1.24:2379                     ---> adjust this with each node IP
            initial-cluster-token: etcd-cluster-1
            initial-cluster: coreos-1=http://192.168.1.24:2380,coreos-2=http://192.168.1.25:2380,coreos-3=http://192.168.1.26:2380
            initial-cluster-state: new
          fleet:
            public-ip: 192.168.1.24   # used for fleetctl ssh command           ---> adjust this with each node IP
          units:
            - name: etcd2.service
              command: start
            - name: fleet.service
              command: start
            - name: 00-eth0.network
              permissions: 0755
              runtime: true
              content: |
                [Match]
                Name=eth0
        
                [Network]
                Address=192.168.1.24/24                                         ---> adjust this with each node IP
                Gateway=192.168.1.1
                DNS=8.8.8.8
                DNS=8.8.4.4
            - name: systemd-networkd.service
              command: start        
        ```
    
    * verify
    
        ```
        coreos-1 rendo # etcdctl member list
        4c5bf3f20ea95537: name=coreos-2 peerURLs=http://192.168.1.25:2380 clientURLs=http://192.168.1.25:2379 isLeader=false
        567623728ce92b28: name=coreos-1 peerURLs=http://192.168.1.24:2380 clientURLs=http://192.168.1.24:2379 isLeader=true
        e54d504de5fc9f4d: name=coreos-3 peerURLs=http://192.168.1.26:2380 clientURLs=http://192.168.1.26:2379 isLeader=false        
        ```

* with the change above, etcd2 now works, but "fleetctl list-machines" always give me one machine instead of all 3 nodes.
    * list-machine output
    
        ```
        coreos-1 rendo # fleetctl list-machines
        MACHINE		IP		METADATA
        2987153e...	192.168.1.24	-        
        ```
    
    * error message
    
        ```
        coreos-1 journal # journalctl -b -u fleet
        
        Jun 06 00:25:45 coreos-1 fleetd[671]: ERROR engine.go:217: Engine leadership lost, renewal failed: 101: Compare failed ([61 != 62])
        Jun 06 00:25:49 coreos-1 fleetd[671]: ERROR engine.go:217: Engine leadership lost, renewal failed: 101: Compare failed ([66 != 67])
        ```

    * problem
        * it found out that the problem was because all my CoreOS instances has the same machine-id
            * https://groups.google.com/forum/#!topic/coreos-user/_wmOxOfMsEY
            
        * to fix the machine id, as mentioned in the post above, i run
        
            ```
            # rm /etc/machine-id
            # reboot
            ```

    * verification, now fleetctl list-machines gives me complete member
    
        ```
        coreos-1 rendo # fleetctl list-machines
        MACHINE		IP		METADATA
        19081653...	192.168.1.26	-
        2987153e...	192.168.1.24	-
        46c715ec...	192.168.1.25	-
        ```


## Todo
* find out how to inject all member ssh key to each node cloud-init config
