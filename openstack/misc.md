
* openstack with ovs - disable snat on neutron router

    ```
    neutron router-gateway-set --disable-snat <routername> <external network name>
    
    example:
    neutron router-gateway-set --disable-snat r2 public
    ```
