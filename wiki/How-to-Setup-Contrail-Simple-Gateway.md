# How to Setup Contrail Simple Gateway

## Overview
You have OpenStack with Contrail as neutron module but you don't have any gateway router to connect the VM inside OpenStack to the outside network


## Procedure to Setup a contrail simple gateway

The following example shows how to add simple gateway on the fly

* select one of the compute node/control node that has vrouter-agent running as the gateway point, for example: compute01
* if you haven't create the virtual network, create it first thru contrail API/GUI
* find out the vrf name of the virtual network that you want to access from outside
    * the standard vrf naming conventions is: 
    
      ```
      <domain-name>:<project-name>:<virtual network name>:<virtual network name>
      ```
      
    * example: 
    
      ``` 
      default-domain:admin:public:public
      ````
      
* create the simple gateway instance

    ```
    # /opt/contrail/utils/provision_vgw_interface.py --oper create --interface vgw1 --subnets 10.16.1.0/24 --routes 0.0.0.0/0 --vrf default-domain:admin:public:public 
    ```

* Note that the example above assumes:
    * network name is public and it is created inside admin project
    * the subnet for public is 10.16.1.0/24
    * VM connected to public will have default gateway (0.0.0.0/0) thru this simple gateway

* at this point, the VM should be reachable from this compute node
* To allow traffic from the other machine beside this compute node, simply add a static route towards 10.16.1.0/24 via this compute node IP

## Note
* the example above will create simple gateway on the fly. It will not persist compute node reboot.
* AFAIK, single simple gateway can only be associated with single VRF (single virtual network)
* It is OK to create simple gateway on multiple compute node for the same virtual network 

## Reference
* https://github.com/Juniper/contrail-controller/wiki/Simple-Gateway
* http://www.juniper.net/techpubs/en_US/contrail2.2/topics/task/configuration/simple-gateway-support-vnc.html

