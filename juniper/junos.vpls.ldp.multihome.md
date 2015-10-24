
# LDP-based VPLS  - Multihoming

## General

### Topology

```
  |--------PE12-----                  -------PE11----|
CE01                   MPLS Backbone               CE02
  |--------PE14-----                  -------PE17----|
```

### Configuration

* PE12

    ```
    rwibawa@vmx-13-12# show routing-instances VLDP4 
    instance-type vpls;
    vlan-id 952;
    interface ge-0/0/0.953;
    protocols {
        vpls {
            no-tunnel-services;
            vpls-id 777;
            neighbor 67.176.255.1 {
                backup-neighbor 67.176.255.7 {
                    standby;
                }
            }
        }
    }
    
    [edit]
    rwibawa@vmx-13-12# show interfaces ge-0/0/0.953  
    apply-groups-except interface-group;
    encapsulation vlan-vpls;
    vlan-id 953;
    family vpls;
    ```

* PE14

    ```
    rwibawa@vmx-13-14# show routing-instances VLDP4  
    instance-type vpls;
    vlan-id 952;
    interface ge-0/0/0.953;
    protocols {
        vpls {
            no-tunnel-services;
            vpls-id 777;
            neighbor 67.176.255.1 {
                backup-neighbor 67.176.255.7 {
                    standby;
                }
            }
        }
    }
    
    [edit]
    rwibawa@vmx-13-14# show interfaces ge-0/0/0.953 
    apply-groups-except interface-group;
    encapsulation vlan-vpls;
    vlan-id 953;
    family vpls;
    ```

* PE11

    ```
    rwibawa@vmx-13-11# show routing-instances VLDP4  
    instance-type vpls;
    interface ge-0/0/0.954;
    protocols {
        vpls {
            no-tunnel-services;
            vpls-id 777;
            neighbor 67.176.255.2 {
                backup-neighbor 67.176.255.4 {
                    standby;
                }
            }
        }
    }
    
    [edit]
    rwibawa@vmx-13-11# show interfaces ge-0/0/0.954 
    apply-groups-except interface-group;
    encapsulation vlan-vpls;
    vlan-id 954;
    input-vlan-map {
        swap;
        vlan-id 952;
    }
    output-vlan-map swap;
    family vpls;
    ```

* PE17

    ```
    rwibawa@vmx-13-17# show routing-instances VLDP4  
    instance-type vpls;
    interface ge-0/0/0.954;
    protocols {
        vpls {
            no-tunnel-services;
            vpls-id 777;
            neighbor 67.176.255.2 {
                backup-neighbor 67.176.255.4 {
                    standby;
                }
            }
        }
    }
    
    [edit]
    rwibawa@vmx-13-17# show interfaces ge-0/0/0.954 
    apply-groups-except interface-group;
    encapsulation vlan-vpls;
    vlan-id 954;
    input-vlan-map {
        swap;
        vlan-id 952;
    }
    output-vlan-map swap;
    family vpls;
    ```

## Verification

* PE12 (primary PE for site 1)

    ```
    rwibawa@vmx-13-12# run show vpls connections instance VLDP4                
    ...
    
    Instance: VLDP4
      VPLS-id: 777
        Neighbor                  Type  St     Time last up          # Up trans
        67.176.255.1(vpls-id 777) rmt   Up     Oct 21 02:32:17 2015           1
          Remote PE: 67.176.255.1, Negotiated control-word: No
          Incoming label: 262403, Outgoing label: 262149
          Negotiated PW status TLV: No
          Local interface: lsi.1049612, Status: Up, Encapsulation: ETHERNET
            Description: Intf - vpls VLDP4 neighbor 67.176.255.1 vpls-id 777
          Flow Label Transmit: No, Flow Label Receive: No
        67.176.255.7(vpls-id 777) rmt   ST   
        

    rwibawa@vmx-13-12# run show vpls mac-table instance VLDP4 
    
    MAC flags       (S -static MAC, D -dynamic MAC, L -locally learned, C -Control MAC
        O -OVSDB MAC, SE -Statistics enabled, NM -Non configured MAC, R -Remote PE MAC)
    
    Routing instance : VLDP4
     Bridging domain : __VLDP4__, VLAN : 952
       MAC                 MAC      Logical          NH     RTR
       address             flags    interface        Index  ID
       00:50:58:13:13:04   D        lsi.1049612     
       00:50:58:13:19:04   D        ge-0/0/0.953    
    ```

* PE14 (backup PE for site 1)

    ```
    rwibawa@vmx-13-14# run show vpls connections instance VLDP4  
    ...
    
    Instance: VLDP4
      VPLS-id: 777
        Neighbor                  Type  St     Time last up          # Up trans
        67.176.255.1(vpls-id 777) rmt   Up     Oct 21 02:32:33 2015           1
          Remote PE: 67.176.255.1, Negotiated control-word: No
          Incoming label: 262149, Outgoing label: 262150
          Negotiated PW status TLV: No
          Local interface: lsi.1048616, Status: Up, Encapsulation: ETHERNET
            Description: Intf - vpls VLDP4 neighbor 67.176.255.1 vpls-id 777
          Flow Label Transmit: No, Flow Label Receive: No
        67.176.255.7(vpls-id 777) rmt   ST   


    rwibawa@vmx-13-14# run show vpls mac-table instance VLDP4 
    
    MAC flags       (S -static MAC, D -dynamic MAC, L -locally learned, C -Control MAC
        O -OVSDB MAC, SE -Statistics enabled, NM -Non configured MAC, R -Remote PE MAC)
    
    Routing instance : VLDP4
     Bridging domain : __VLDP4__, VLAN : 952
       MAC                 MAC      Logical          NH     RTR
       address             flags    interface        Index  ID
       00:50:58:13:13:04   D        ge-0/0/0.953    
       00:50:58:13:19:04   D        ge-0/0/0.953  
    ```

* PE11 (primary PE for Site 2)

    ```
    rwibawa@vmx-13-11# run show vpls connections instance VLDP4  
    ...
    
    Instance: VLDP4
      VPLS-id: 777
        Neighbor                  Type  St     Time last up          # Up trans
        67.176.255.2(vpls-id 777) rmt   Up     Oct 21 02:32:26 2015           1
          Remote PE: 67.176.255.2, Negotiated control-word: No
          Incoming label: 262149, Outgoing label: 262403
          Negotiated PW status TLV: No
          Local interface: lsi.1048933, Status: Up, Encapsulation: ETHERNET
            Description: Intf - vpls VLDP4 neighbor 67.176.255.2 vpls-id 777
          Flow Label Transmit: No, Flow Label Receive: No
        67.176.255.4(vpls-id 777) rmt   ST  
    ```

* PE17 (backup PE for Site 2)

    ```
    rwibawa@vmx-13-17# run show vpls connections instance VLDP4 
    ...
    
    Instance: VLDP4
      VPLS-id: 777
        Neighbor                  Type  St     Time last up          # Up trans
        67.176.255.2(vpls-id 777) rmt   Up     Oct 21 02:32:34 2015           1
          Remote PE: 67.176.255.2, Negotiated control-word: No
          Incoming label: 262149, Outgoing label: 262404
          Negotiated PW status TLV: No
          Local interface: lsi.1048622, Status: Up, Encapsulation: ETHERNET
            Description: Intf - vpls VLDP4 neighbor 67.176.255.2 vpls-id 777
          Flow Label Transmit: No, Flow Label Receive: No
        67.176.255.4(vpls-id 777) rmt   ST   
        

    rwibawa@vmx-13-17# run show vpls mac-table instance VLDP4 
    
    MAC flags       (S -static MAC, D -dynamic MAC, L -locally learned, C -Control MAC
        O -OVSDB MAC, SE -Statistics enabled, NM -Non configured MAC, R -Remote PE MAC)
    
    Routing instance : VLDP4
     Bridging domain : __VLDP4__, VLAN : NA
       MAC                 MAC      Logical          NH     RTR
       address             flags    interface        Index  ID
       00:50:58:13:13:04   D        ge-0/0/0.954    
       00:50:58:13:19:04   D        ge-0/0/0.954    
    ```


## Conclusion

* if we look in detail the verification section above, we will see that:
    * both primary and backup PE on local site setup pseudowire to the __primary_ PE on remote site
    * both primary and backup PE on local site put pseudowire to the __backup_ PE on remote site as __standby__
    * show mac table shows that primary PE will learn mac address from local PE-CE interface and also from lsi interface which represent pseudowire to remote site 
    * on the other hand, backup PE only learn mac address from local PE-CE interface only.
        * this is because there is no return pseudowire connection from remote primary PE to the local backup PE.
        * this is to prevent layer 2 domain looping.
* unlike BGP-based VPLS, in LDP-based VPLS, it is the remote PE that decide which local PE that become primary and which one become backup
* It is recommended that on local PE, both PE has consistent configuration, which means, refer to example above: 
    * if PE12 choose PE11 as remote primary PE, PE14 must do the same. 
    * the same thing from other side, if PE11 choose PE12 as primary, PE17 must choose PE12 as primary as well.
    
## Misc
* we are using different vlan between site 1 and site 2, therefore, vlan conversion is required.
    * at site 1, we use "vlan-id" knob within routing-instance stanza
    * at site 2, we use input/output vlan mapping within logical interface stanza
