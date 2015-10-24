
# JunOS LDP-based VPLS with BGP autodiscovery (FEC 129+BGP AD)

## General
* The configuration is pretty much similar as normal LDP-based VPLS
* The only difference is, no neighbor IP that need to be defined, and include "l2vpn-id" in addition to route-distingusher and vrf-target
* In term of BGP configuration, we need to add "family l2vpn auto-discovery-only"

## Configuration

### Topology
* consist of 3 PEs

* generic BGP config

    ```
    rwibawa@vmx-13-17# show protocols bgp 
    group IBGP {
        type internal;
        local-address 67.176.255.7;
        import rtbh;
        ...
        family l2vpn {
            auto-discovery-only;    ---> this is needed for LDP + BGP-AD
        }
        ...
    }
    ```

* note: "family l2vpn signalling" is not required for LDP VPLS + BGP AD. It is only required by BGP-based VPLS, which is outside of this article scope. 

* PE1

    ```
    rwibawa@vmx-13-11# show routing-instances VLDP5    
    instance-type vpls;
    vlan-id 955;
    interface ge-0/0/0.956;
    route-distinguisher 67.176.255.1:778;
    l2vpn-id l2vpn-id:7041:778;
    vrf-target target:7041:778;
    protocols {
        vpls {
            no-tunnel-services;
        }
    }
    
    [edit]
    rwibawa@vmx-13-11# show interfaces ge-0/0/0.956 
    apply-groups-except interface-group;
    encapsulation vlan-vpls;
    vlan-id 956;
    family vpls;
    ```

* PE4

    ```
    rwibawa@vmx-13-14# show routing-instances VLDP5  
    instance-type vpls;
    vlan-id 955;
    interface ge-0/0/0.957;
    route-distinguisher 67.176.255.4:778;
    l2vpn-id l2vpn-id:7041:778;
    vrf-target target:7041:778;
    protocols {
        vpls {
            no-tunnel-services;
        }
    }
    
    [edit]
    rwibawa@vmx-13-14# show interfaces ge-0/0/0.957 
    apply-groups-except interface-group;
    encapsulation vlan-vpls;
    vlan-id 957;
    family vpls;
    ```

* PE7

    ```
    rwibawa@vmx-13-17# show routing-instances VLDP5  
    instance-type vpls;
    vlan-id 955;
    interface ge-0/0/0.958;
    route-distinguisher 67.176.255.7:778;
    l2vpn-id l2vpn-id:7041:778;
    vrf-target target:7041:778;
    protocols {
        vpls {
            no-tunnel-services;
        }
    }
    
    [edit]
    rwibawa@vmx-13-17# show interfaces ge-0/0/0.958 
    apply-groups-except interface-group;
    encapsulation vlan-vpls;
    vlan-id 958;
    family vpls;
    ```

* Notes
    * due to limitation on the lab topology, each PE-CE interface is using different vlan-id
    * as a workaround, to make sure each CE can talk each other via VPLS, "vlan-id" knob is used to do automatica vlan-swapping.
    
    

## Verification

* PE1

    ```
    rwibawa@vmx-13-11# run show vpls connections instance VLDP5  
    ...
    
    Instance: VLDP5
      L2vpn-id: 7041:778
      Local-id: 67.176.255.1
        Remote-id                 Type  St     Time last up          # Up trans
        67.176.255.4              rmt   Up     Oct 21 02:40:43 2015           1
          Remote PE: 67.176.255.4, Negotiated control-word: No
          Incoming label: 262151, Outgoing label: 262151
          Negotiated PW status TLV: No
          Local interface: lsi.1048936, Status: Up, Encapsulation: ETHERNET
            Description: Intf - vpls VLDP5 local-id 67.176.255.1 remote-id 67.176.255.4 neighbor 67.176.255.4
          Flow Label Transmit: No, Flow Label Receive: No
        67.176.255.7              rmt   Up     Oct 21 02:40:43 2015           1
          Remote PE: 67.176.255.7, Negotiated control-word: No
          Incoming label: 262152, Outgoing label: 262151
          Negotiated PW status TLV: No
          Local interface: lsi.1048937, Status: Up, Encapsulation: ETHERNET
            Description: Intf - vpls VLDP5 local-id 67.176.255.1 remote-id 67.176.255.7 neighbor 67.176.255.7
          Flow Label Transmit: No, Flow Label Receive: No
    ```

* PE4

    ```
    rwibawa@vmx-13-14# run show vpls connections instance VLDP5  
    ...
    Instance: VLDP5
      L2vpn-id: 7041:778
      Local-id: 67.176.255.4
        Remote-id                 Type  St     Time last up          # Up trans
        67.176.255.1              rmt   Up     Oct 21 02:40:45 2015           1
          Remote PE: 67.176.255.1, Negotiated control-word: No
          Incoming label: 262151, Outgoing label: 262151
          Negotiated PW status TLV: No
          Local interface: lsi.1048621, Status: Up, Encapsulation: ETHERNET
            Description: Intf - vpls VLDP5 local-id 67.176.255.4 remote-id 67.176.255.1 neighbor 67.176.255.1
          Flow Label Transmit: No, Flow Label Receive: No
        67.176.255.7              rmt   Up     Oct 21 02:40:45 2015           1
          Remote PE: 67.176.255.7, Negotiated control-word: No
          Incoming label: 262152, Outgoing label: 262152
          Negotiated PW status TLV: No
          Local interface: lsi.1048622, Status: Up, Encapsulation: ETHERNET
            Description: Intf - vpls VLDP5 local-id 67.176.255.4 remote-id 67.176.255.7 neighbor 67.176.255.7
          Flow Label Transmit: No, Flow Label Receive: No
    ```

* PE7

    ```
    rwibawa@vmx-13-17# run show vpls connections instance VLDP5 
    ...
    
    Instance: VLDP5
      L2vpn-id: 7041:778
      Local-id: 67.176.255.7
        Remote-id                 Type  St     Time last up          # Up trans
        67.176.255.1              rmt   Up     Oct 21 02:40:43 2015           1
          Remote PE: 67.176.255.1, Negotiated control-word: No
          Incoming label: 262151, Outgoing label: 262152
          Negotiated PW status TLV: No
          Local interface: lsi.1048626, Status: Up, Encapsulation: ETHERNET
            Description: Intf - vpls VLDP5 local-id 67.176.255.7 remote-id 67.176.255.1 neighbor 67.176.255.1
          Flow Label Transmit: No, Flow Label Receive: No
        67.176.255.4              rmt   Up     Oct 21 02:40:43 2015           1
          Remote PE: 67.176.255.4, Negotiated control-word: No
          Incoming label: 262152, Outgoing label: 262152
          Negotiated PW status TLV: No
          Local interface: lsi.1048627, Status: Up, Encapsulation: ETHERNET
            Description: Intf - vpls VLDP5 local-id 67.176.255.7 remote-id 67.176.255.4 neighbor 67.176.255.4
          Flow Label Transmit: No, Flow Label Receive: No
    ```
