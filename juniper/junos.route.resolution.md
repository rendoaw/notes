
## Problem
It is common that people configure route-reflector outside the PE, either on dedicated router or on the P router. 
Those type of routers sometime doesn't have lsp configured (in rsvp-based network) or even may not running mpls at all. 

## Symptomp

* all non inet.0 routes become hidden with error message "next-hop unusable", for example

    ```
    rwibawa@vmx-13-13# run show bgp summary
    ...
    Peer                     AS      InPkt     OutPkt    OutQ   Flaps Last Up/Dwn State|#Active/Received/Accepted/Damped...
    67.176.255.1     16689.7041        183       9403       0       0       58:32 Establ
      inet.0: 7/7/7/0
      inet6.0: 0/4/4/0
      bgp.l3vpn.0: 0/45/45/0
      bgp.l2vpn.0: 0/1/1/0
    ...
    
    bgp.l3vpn.0: 148 destinations, 162 routes (0 active, 0 holddown, 162 hidden)
    
    22:4003:108.42.0.22/32 (1 entry, 0 announced)
             BGP    Preference: 170/-101
                    Route Distinguisher: 22:4003
                    Next hop type: Unusable
                    Address: 0x94129e4
                    Next-hop reference count: 186
                    State: <Hidden Int Ext ProtectionPath ProtectionCand>
                    Local AS: 16689.7041 Peer AS: 16689.7041
                    Age: 59:38
                    Validation State: unverified
                    Task: BGP_16689.7041.67.176.255.1+179
                    AS path: 22 I
                    Communities: target:22:4003
                    Accepted
                    VPN Label: 17
                    Localpref: 100
                    Router ID: 67.176.255.1
                    Indirect next hops: 1
                            Protocol next hop: 67.176.255.1
                            Label operation: Push 17
                            Label TTL action: prop-ttl
                            Load balance label: Label 17: None;
                            Indirect next hop: 0x2 no-forward INH Session ID: 0x0
    
    
    ```

## Solution

* for most cases, we can solve this issue by configuring either one of the following

    * option 1: for rsvp-based network, setup LSP from the RR to each BGP peering
        * this option doesn't work if RR has no MPLS configured at all

    * option 2:  configure static route from inet.3 to inet.0

        ```
        rwibawa@vmx-13-13# show routing-options
        rib inet.3 {
            static {
                route 0.0.0.0/0 next-table inet.0;
            }
        }
        ```

    * option 3:  configure route resolution mapping
    
        ```
        rwibawa@vmx-13-13# show routing-options
        ...
        resolution {
            rib inet.3 {
                resolution-ribs inet.0;
            }
            rib bgp.l3vpn.0 {
                resolution-ribs inet.0;
            }
            rib bgp.l2vpn.0 {
                resolution-ribs inet.0;
            }
        }
        ...
        
        ```
    * option 4:  configure rib-groups inet.0 to inet.3
    
        ```
        rwibawa@vmx-13-13# show routing-options
        ...
        rib-groups {
            inet0-to-inet3 {
                import-rib [ inet.0 inet.3 ];
                import-policy loopbacks;
            }
        }
        ...
        
        [edit logical-systems R3RR]
        rwibawa@vmx-13-13# show protocols ospf
        rib-group inet0-to-inet3;
        ...
        ```

* if you have 6PE configured, we also need the following rib-group configuration. The reason is, JunOS doesn't allow inet6.{0|3} resolution using inet.0

    * if you are using option 2 or option 3 above, you need to add rib-group for inet6.0
    
        ```
        rwibawa@vmx-13-13# show routing-options
        ...
        rib-groups {
            inet0-to-inet6 {
                import-rib [ inet.0 inet6.0 ];
                import-policy loopbacks;
            }
        }
        ...
        
        rwibawa@vmx-13-13# show protocols ospf
        rib-group inet0-to-inet6;
        ...
        ```

    * if you are using option 4 above, you need to modify your rib-group
    
        ```
        rwibawa@vmx-13-13# show routing-options
        ...
        rib-groups {
            inet0-to-inet3-and-inet6 {
                import-rib [ inet.0 inet.3 inet6.0 ];
                import-policy loopbacks;
            }
        }
        ...
        
        rwibawa@vmx-13-13# show protocols ospf
        rib-group inet0-to-inet3-and-inet6;
        ...
        ```

References:
* http://www.juniper.net/documentation/en_US/junos14.1/topics/example/vpns-layer-3-route-resolution-route-reflector.html
* http://blog.inetsix.net/2012/09/junos-as-pe-with-route-reflector-to-learn-vpn/
* http://www.gossamer-threads.com/lists/nsp/juniper/54404
