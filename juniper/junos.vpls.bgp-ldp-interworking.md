
# VPLS LDP-BGP interworking


## Topology

```
  ---------------------------------MPLS Backbone---------------------------------
  |                                      |                                       |
PE11 (ldp)                       PE14(LDP+BGP)                                PE17(BGP)
  |                                      |                                       |
 CE1                                    CE2                                     CE3
```

## Configuration

* PE11

    ```
    rwibawa@vmx-13-11# show interfaces ge-0/0/0.960    
    apply-groups-except interface-group;
    encapsulation vlan-vpls;
    vlan-id 960;
    family vpls;
    
    [edit]
    rwibawa@vmx-13-11# show routing-instances VPLS6    
    instance-type vpls;
    vlan-id 959;
    interface ge-0/0/0.960;
    protocols {
        vpls {
            no-tunnel-services;
            vpls-id 779;
            neighbor 67.176.255.4;
        }
    }
    ```

* PE14

    ```
    rwibawa@vmx-13-14# show routing-instances VPLS6  
    instance-type vpls;
    vlan-id 959;
    interface ge-0/0/0.961;
    route-distinguisher 67.176.255.4:779;
    vrf-target target:7041:779;
    protocols {
        vpls {
            no-tunnel-services;
            site 4 {
                site-identifier 4;
            }
            vpls-id 779;
            mesh-group LDP_PE {
                neighbor 67.176.255.1;
            }
        }
    }
    
    [edit]
    rwibawa@vmx-13-14# show interfaces ge-0/0/0.961 
    apply-groups-except interface-group;
    encapsulation vlan-vpls;
    vlan-id 961;
    family vpls;
    ```

* PE17

    ```
    rwibawa@vmx-13-17# show routing-instances VPLS6    
    instance-type vpls;
    vlan-id 959;
    interface ge-0/0/0.962;
    route-distinguisher 67.176.255.7:779;
    vrf-target target:7041:779;
    protocols {
        vpls {
            no-tunnel-services;
            site 7 {
                site-identifier 7;
            }
            mac-flush;
        }
    }
    
    [edit]
    rwibawa@vmx-13-17# show interfaces ge-0/0/0.962    
    apply-groups-except interface-group;
    encapsulation vlan-vpls;
    vlan-id 962;
    family vpls;
    ```


## Verification

* PE11

    ```
    rwibawa@vmx-13-11# run show vpls connections instance VPLS6              
    ...
    
    Instance: VPLS6
      VPLS-id: 779
        Neighbor                  Type  St     Time last up          # Up trans
        67.176.255.4(vpls-id 779) rmt   Up     Oct 21 02:48:22 2015           1
          Remote PE: 67.176.255.4, Negotiated control-word: No
          Incoming label: 262153, Outgoing label: 262154
          Negotiated PW status TLV: No
          Local interface: lsi.1048938, Status: Up, Encapsulation: ETHERNET
            Description: Intf - vpls VPLS6 neighbor 67.176.255.4 vpls-id 779
          Flow Label Transmit: No, Flow Label Receive: No
    ```

* PE14

    ```
    rwibawa@vmx-13-14# run show vpls connections instance VPLS6 
    ...
    
    Instance: VPLS6
    Edge protection: Not-Primary
      BGP-VPLS State
      Local site: 4 (4)
        connection-site           Type  St     Time last up          # Up trans
        7                         rmt   Up     Oct 24 01:49:51 2015           1
          Remote PE: 67.176.255.7, Negotiated control-word: No
          Incoming label: 262567, Outgoing label: 262532
          Local interface: lsi.1048627, Status: Up, Encapsulation: VPLS
            Description: Intf - vpls VPLS6 local site 4 remote site 7
      LDP-VPLS State
      VPLS-id: 779
      Mesh-group connections: LDP_PE
        Neighbor                  Type  St     Time last up          # Up trans
        67.176.255.1(vpls-id 779) rmt   Up     Oct 21 03:05:43 2015           1
          Remote PE: 67.176.255.1, Negotiated control-word: No
          Incoming label: 262154, Outgoing label: 262153
          Negotiated PW status TLV: No
          Local interface: lsi.1048625, Status: Up, Encapsulation: ETHERNET
            Description: Intf - vpls VPLS6 neighbor 67.176.255.1 vpls-id 779
          Flow Label Transmit: No, Flow Label Receive: No
    ```

* PE17

    ```
    rwibawa@vmx-13-17# run show vpls connections instance VPLS6       
    ...
    Instance: VPLS6
    Edge protection: Not-Primary
      Local site: 7 (7)
        connection-site           Type  St     Time last up          # Up trans
        4                         rmt   Up     Oct 24 01:49:49 2015           1
          Remote PE: 67.176.255.4, Negotiated control-word: No
          Incoming label: 262532, Outgoing label: 262567
          Local interface: lsi.1048631, Status: Up, Encapsulation: VPLS
            Description: Intf - vpls VPLS6 local site 7 remote site 4
    ```

## Conclusion


... to be continued ...
