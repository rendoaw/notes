
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


## how to find the actual virtual serial console TCP port for specific VM  instance 

* find the vm name

    ```
    stack@openstack1:~/devstack$ nova list
    +--------------------------------------+----------------+---------+------------+-------------+--------------------------------------------------------------+
    | ID                                   | Name           | Status  | Task State | Power State | Networks                                                     |
    +--------------------------------------+----------------+---------+------------+-------------+--------------------------------------------------------------+
    | 8ad5a2c1-0a38-4972-87a4-953c22d80742 | testvm         | ACTIVE  | -          | Running     | private3=172.19.2.104; private2=172.19.1.103                 |
    +--------------------------------------+----------------+---------+------------+-------------+--------------------------------------------------------------+
    ```

* find the instance name and which compute node that host it

    ```
    stack@openstack1:~/devstack$ nova show testvm
    +--------------------------------------+----------------------------------------------------------+
    | Property                             | Value                                                    |
    +--------------------------------------+----------------------------------------------------------+
    | OS-DCF:diskConfig                    | AUTO                                                     |
    | OS-EXT-AZ:availability_zone          | nova                                                     |
    | OS-EXT-SRV-ATTR:host                 | openstack1                                               |
    | OS-EXT-SRV-ATTR:hostname             | testvm                                                   |
    | OS-EXT-SRV-ATTR:hypervisor_hostname  | openstack1        --> this the compute node hostname     |
    | OS-EXT-SRV-ATTR:instance_name        | instance-0000000d --> this is the instance name          |
    | OS-EXT-SRV-ATTR:kernel_id            |                                                          |
    | OS-EXT-SRV-ATTR:launch_index         | 0                                                        |
    | OS-EXT-SRV-ATTR:ramdisk_id           |                                                          |
    | OS-EXT-SRV-ATTR:reservation_id       | r-0biaimu9                                               |
    | OS-EXT-SRV-ATTR:root_device_name     | /dev/hda                                                 |
    | OS-EXT-SRV-ATTR:user_data            | -                                                        |
    | OS-EXT-STS:power_state               | 4                                                        |
    | OS-EXT-STS:task_state                | -                                                        |
    | OS-EXT-STS:vm_state                  | stopped                                                  |
    | OS-SRV-USG:launched_at               | 2015-11-15T03:11:41.000000                               |
    | OS-SRV-USG:terminated_at             | -                                                        |
    | accessIPv4                           |                                                          |
    | accessIPv6                           |                                                          |
    | config_drive                         | True                                                     |
    | created                              | 2015-11-15T03:11:33Z                                     |
    | flavor                               | m1.small (2)                                             |
    | hostId                               | 7662b19b5e897d4e6b924daea7cea3cdd50b66c419cba06fa2171180 |
    | id                                   | 8ad5a2c1-0a38-4972-87a4-953c22d80742                     |
    | image                                | junosvm (37d7696c-8c77-433f-881a-2754e14bc0c1)           |
    | key_name                             | -                                                        |
    | metadata                             | {}                                                       |
    | name                                 | junosvm-serial                                           |
    | os-extended-volumes:volumes_attached | []                                                       |
    | private2 network                     | 172.19.1.103                                             |
    | private3 network                     | 172.19.2.104                                             |
    | security_groups                      | allow                                                    |
    | status                               | SHUTOFF                                                  |
    | tenant_id                            | f27176e44f9e42f594fd823a0407b0e6                         |
    | updated                              | 2015-11-15T03:37:26Z                                     |
    | user_id                              | 08c7216b91054517925a3456f9e3bc2c                         |
    +--------------------------------------+----------------------------------------------------------+
    ```

* use kvm standard command to find the actual TCP port 

    ```
    stack@openstack1:~/devstack$ virsh dumpxml instance-0000000d
    <domain type='kvm'>
      <name>instance-0000000d</name>
    
    ..deleted..
    
        <serial type='tcp'>
          <source mode='bind' host='192.168.155.7' service='10001'/>
          <protocol type='raw'/>
          <target port='0'/>
        </serial>

    ..deleted..
    
    </domain>
    ```
