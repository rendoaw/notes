# A hack to create routed virtual network in Openstack with Openvswitch

This is the hack to create a routed (not NAT-ed) virtual network in Openstack with Openvswitch that was installed using PackStack.

* create a new virtual network as usual
    * let say vnet1 with subnet=subnet1
    * do not mark this new vnet as external
    
* create a new neutron router
    * let say r1
    * use existing external network as the gateway interface
    * take a note on what is the external network IP assigned to this router
        * let say the IP=gw_ip_1
    * attach the new vnet to this neutron router
        * in this example, attach vnet1 to this neutron router

* disable snat on this neutron router

    ```
    neutron router-gateway-set --disable-snat <routername> <external network name>
    
    example:
    neutron router-gateway-set --disable-snat r2 public
    ```

* Add routes to the new virtual network via the newly created neutron router external IP

    ```
    example: 
    # ip r add subnet1 via gw_ip_1
    ```

* Outside openstack, make sure you have route towards your new subnet (subnet1) point to the network node IP address
    







* openstack with ovs - disable snat on neutron router

    
 
* packstack - add non-nat virtual network
    * create new vnet as usual, let say vnet1 with subnet=subnet1
    * do not mark this new vnet as external
    * create a new neutron router, let say r1
        * use existing external network as the gateway interface
        * take a note on what is the external network IP assigned to this router, let say the IP=gw_ip_1
        * attach the new vnet to this neutron router
    * disable snat on this neutron router
        * see "openstack with ovs - disable snat on neutron router" section above
    * go to network node
        * add static route to the new vnet subnet via the external 
            * example: ip r add subnet1 via gw_ip_1
    * Outside openstack, make sure you have route towards your new subnet (subnet1) point to the network node IP address
    




