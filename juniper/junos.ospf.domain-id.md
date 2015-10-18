
# OSPF Domain ID

## Official version

#### source:
* http://www.juniper.net/techpubs/en_US/junos12.1/topics/usage-guidelines/vpns-configuring-routing-between-pe-and-ce-routers-in-layer-3-vpns.html
* http://www.juniper.net/documentation/en_US/junos12.1/topics/usage-guidelines/routing-configuring-ospf-domain-ids-for-vpns.html

This extended community ID can then be carried across the BGP VPN backbone. When the route is redistributed back as an OSPF or OSPFv3 route on the PE router and advertised to the CE near the destination, the domain ID identifies which domain the route originated from. The routing instance checks incoming routes for the domain ID. The route is then propagated as either a Type 3 LSA or Type 5 LSA.

When a PE router receives a route, it redistributes and advertises the route as either a Type 3 LSA or a Type 5 LSA, depending on the following:
* If the receiving PE router sees a Type 3 route with a matching domain ID, the route is redistributed and advertised as a Type 3 LSA.
* If the receiving PE router sees a Type 3 route without a domain ID (the extended attribute field of the route’s BGP update does not include a domain ID), the route is redistributed and advertised as a Type 3 LSA.
* If the receiving PE router sees a Type 3 route with a non-matching domain ID, the route is redistributed and advertised as a Type 5 LSA.
* If the receiving PE router sees a Type 3 route with a domain ID, but the router does not have a domain ID configured, the route is redistributed and advertised as a Type 5 LSA.
* If the receiving PE router sees a Type 5 route, the route is redistributed and advertised as a Type 5 LSA, regardless of the domain ID.

On the local PE router, the prefix of the directly connected PE/CE interface is an active direct route. This route is also an OSPF or OSPFv3 route.

In the VRF export policy, the direct prefix is exported to advertise the route to the remote PE. This route is injected as an AS-External-LSA, much as when a direct route is exported into OSPF or OSPFv3.

Domain ID ensures that an originated summary LSA arrives at the remote PE as a summary LSA. Domain ID does not translate AS-external-LSAs into summary LSAs.

#### other links: 
* http://www.juniper.net/documentation/en_US/junos15.1/topics/example/vpn-ospf-domain-id-for-layer-3-configuring.html


## Personal Observation
* if vrf-target is being used at the prefix-advertiser PE, JunOS automatically include BGP extended attribute "domain-id:a.b.c.d:e" and "rte-type:<ospf area>:<lsa-type>"
  * config @ prefix-advertiser PE 
  
    ```
    lab@vmx-13-14# show routing-instances HP
    instance-type vrf;
    interface ge-0/0/0.937;
    interface lo0.937;
    route-distinguisher 67.176.255.4:7743;
    inactive: vrf-import HP-import;
    inactive: vrf-export HP-export;
    vrf-target target:7041:7742;
    vrf-table-label;
    protocols {
        ospf {
            export rw-redistribute-bgp-all;
            area 0.0.3.6 {
                interface all;
            }
        }
    }
    ```

  * config @ prefix-receiver PE

    ```
    lab@vmx-13-12# show routing-instances HP
    instance-type vrf;
    interface ge-0/0/0.936;
    interface lo0.936;
    route-distinguisher 67.176.255.2:7742;
    inactive: vrf-import HP-import;
    inactive: vrf-export HP-export;
    vrf-target target:7041:7742;
    protocols {
        ospf {
            export rw-redistribute-bgp-all;
            area 0.0.3.6 {
                interface all;
            }
        }
    }
    ```

  * OSPF database @ prefix-receiver PE

    ```
    lab@vmx-13-12# run show ospf database instance HP
    
        OSPF database, Area 0.0.3.6
     Type       ID               Adv Rtr           Seq      Age  Opt  Cksum  Len
    Router  *77.4.0.2         77.4.0.2         0x80000002   564  0x22 0xba19  48
    Summary *77.4.0.14        77.4.0.2         0x80000001   337  0xa2 0x7e8a  28
        OSPF AS SCOPE link state database
     Type       ID               Adv Rtr           Seq      Age  Opt  Cksum  Len
    Extern  *77.4.0.4         77.4.0.2         0x80000001   952  0xa2 0x74a7  36
    Extern  *77.4.4.0         77.4.0.2         0x80000002   341  0xa2 0x5cc1  36
    Extern  *77.4.44.0        77.4.0.2         0x80000001   572  0xa2 0xb63d  36
    Extern  *77.4.45.0        77.4.0.2         0x80000001   572  0xa2 0xab47  36
    Extern  *77.4.46.0        77.4.0.2         0x80000001   572  0xa2 0xa051  36
    Extern  *77.4.47.0        77.4.0.2         0x80000001   572  0xa2 0x955b  36
    ```

  * BGP route @ prefix-receiver PE (see the line with Communities ... below)

    ```
    89.100.255.4:7743:77.4.0.14/32 (1 entry, 0 announced)
            *BGP    Preference: 170/-101
                    Route Distinguisher: 89.100.255.4:7743
                    Next hop type: Indirect
                    Address: 0xa67d280
                    Next-hop reference count: 21
                    Source: 89.100.255.3
                    Next hop type: Router, Next hop index: 1147
                    Next hop: 89.100.0.34 via ge-0/0/3.0, selected
                    Label-switched-path r2-to-r4
                    Label operation: Push 25, Push 303872(top)
                    Label TTL action: prop-ttl, prop-ttl(top)
                    Load balance label: Label 25: None; Label 303872: None;
                    Session Id: 0x147
                    Protocol next hop: 89.100.255.4
                    Label operation: Push 25
                    Label TTL action: prop-ttl
                    Load balance label: Label 25: None;
                    Indirect next hop: 0x9b60bb0 1048590 INH Session ID: 0x199
                    State: <Active Int Ext ProtectionPath ProtectionCand>
                    Local AS: 1093737345 Peer AS: 1093737345
                    Age: 7:11       Metric: 1       Metric2: 1
                    Validation State: unverified
                    Task: BGP_1093737345.89.100.255.3+55462
                    AS path: I (Originator)
                    Cluster list:  89.100.255.3
                    Originator ID: 89.100.255.4
                    Communities: target:7041:7742 rte-type:0.0.3.6:1:0
                    Import Accepted
                    VPN Label: 25
                    Localpref: 100
                    Router ID: 89.100.255.3
                    Secondary Tables: HP.inet.0
                    Indirect next hops: 1
                            Protocol next hop: 89.100.255.4 Metric: 1
                            Label operation: Push 25
                            Label TTL action: prop-ttl
                            Load balance label: Label 25: None;
                            Indirect next hop: 0x9b60bb0 1048590 INH Session ID: 0x199
                            Indirect path forwarding next hops: 1
                                    Next hop type: Router
                                    Next hop: 89.100.0.34 via ge-0/0/3.0
                                    Session Id: 0x147
                            89.100.255.4/32 Originating RIB: inet.3
                              Metric: 1                       Node path count: 1
                              Forwarding nexthops: 1
                                    Nexthop: 89.100.0.34 via ge-0/0/3.0
    ```


* if vrf-export is being used at the prefix-advertiser PE, for some reason, the prefix-receiver PE is ignoring "domain-id:...." community and make it as LSA type 5.

...to be continued...
