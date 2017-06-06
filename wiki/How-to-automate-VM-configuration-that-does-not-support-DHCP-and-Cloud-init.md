# How to automate VM configuration that does not support DHCP and Cloud init

In some cases, you want to spawn a VM on OpenStack, but the VM Operating System does not have DHCP client capability and also no cloud-init support. 
In this case we have to use VNC console to configure the VM, at least to configure basic connectivity e.g: IP address, default gateway, etc

To automate this VM basic connectivity configuration, one of the possibility is to use python vncdotool module. 
* http://vncdotool.readthedocs.io/en/latest/
* https://pypi.python.org/pypi/vncdotool

And here is the sample workflow

* Find the direct access VNC port (vncdotool does not work with novnc)

    * Find the compute node of this VM

        ```
        # nova show 68fb6821-4d46-48c4-91f5-3b1d3d02ccbd | grep "| OS-EXT-SRV-ATTR:host"
        | OS-EXT-SRV-ATTR:host                 | brg-ct1-compute9                                                                         |
        ```

    * Find the KVM instance ID for this VM

        ```
        # nova show 68fb6821-4d46-48c4-91f5-3b1d3d02ccbd | grep "instance_name"
        | OS-EXT-SRV-ATTR:instance_name        | instance-00001256        
        ```

    * Go to the compute node ( i am using ssh-key on my script to auto-login to the compute node), and find the VNC port
    
        ```
        # ssh root@brg-ct1-compute9 "virsh dumpxml instance-00001256 | grep vnc | grep port"
            <graphics type='vnc' port='5919' autoport='yes' listen='10.25.155.165' keymap='en-us'>        
        ```
        
* OK, now we find the direct address, which is 10.25.155.165 port 5919

* Next Step, use vncdotool to send command thru vnc

    ```
    # vncdo -s <computenodeip>::<vncport> <vncdotool command> <message>
    
    e.g:
    # vncdo -s 10.25.155.165::5919 type "configure"
    # vncdo -s 10.25.155.165::5919 key enter
    # vncdo -s 10.25.155.165::5919 type "set interfaces fxp0 unit 0 family inet address 192.168.100.10/24"
    # vncdo -s 10.25.155.165::5919 key enter
    # vncdo -s 10.25.155.165::5919 type "set routing-options static route 0.0.0.0/0 next-hop 192.168.100.1"
    # vncdo -s 10.25.155.165::5919 key enter
    # vncdo -s 10.25.155.165::5919 type "commit"
    # vncdo -s 10.25.155.165::5919 key enter
    # vncdo -s 10.25.155.165::5919 type "exit"
    # vncdo -s 10.25.155.165::5919 key enter
    ```

* Wait, how do we get the output of the command that we send?
    * No, we can't. VNC has graphical output, so basically we are blindly typing the keyboard keys.
    
* So, how do we know when we can send the login or any other command?
    * specific to my use case, i am waiting for the VM to give me the login prompt which is i can check via console-port
    * for example, if i see login prompt, i know the VM is ready to accept the command
    
        ```
        # nova console-log  68fb6821-4d46-48c4-91f5-3b1d3d02ccbd
        ...
        
        vmx104 (ttyd0)
        
        login:
        ...
        ```

* Notes:
    * The workflow above works only if you have configure nova vnc port to listen in non-localhost IP
        * make sure you have the following setting on your nova configuration
            
            ```
            vncserver_enabled = true
            vncserver_listen = 10.25.155.165
            ```
            
    * If you don't like this approach, alternatively you can you may be able to find something to bridge/convert novnc to a standard socket or to send any command thru novnc
        

