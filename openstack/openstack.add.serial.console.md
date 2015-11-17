
## Add read-write serial console support to VM instance on Openstack Juno

* add the following to /etc/nova/nova.conf

    ```
    [serial_console]
    enabled=true
    
    # Location of serial console proxy. (string value)
    base_url=ws://0.0.0.0:6083/
    
    # IP address on which instance serial console should listen
    # (string value)
    listen=0.0.0.0
    
    # The address to which proxy clients (like nova-serialproxy)
    # should connect (string value)
    # proxyclient_address=127.0.0.1
    
    ```

* restart nova

## note

* if you just want simple serial console accessible via telnet, no need to start the serial console proxy. 
* serial console proxy is only required if you want to do the openstack way, accessing virtual serial console via websocket.
