
# Example: Map prefix to specific LSP

## Configuration 

* at egress PE, tag the prefix with specific community

    ```
    rwibawa@vmx-13-11# show routing-instances ASUS
    instance-type vrf;
    interface ge-0/0/0.943;
    interface lo0.943;
    route-distinguisher 67.176.255.1:773;
    vrf-import ASUS-import;
    vrf-export ASUS-export;
    vrf-table-label;
    protocols {
        ospf {
            export rw-redistribute-bgp-all;
            area 0.0.0.0 {
                interface all;
            }
        }
    }

    [edit]
    rwibawa@vmx-13-11# show policy-options policy-statement ASUS-export
    term 1 {
        from {
            route-filter 77.3.0.11/32 exact;
        }
        then {
            community set ASUS;
            community add ASUS-1-1;
            accept;
        }
    }
    term default {
        from protocol [ ospf direct ];
        then {
            community set ASUS;
            community add ASUS-1-2;
            accept;
        }
    }

    [edit]
    rwibawa@vmx-13-11# show policy-options community ASUS-1-1
    members 773:101;

    [edit]
    rwibawa@vmx-13-11# show policy-options community ASUS-1-2
    members 773:102;
    ```


* at ingress PE, configure routing-options - forwarding-table policy to match the community and assign specific LSP

```
rwibawa@vmx-13-12# show routing-options forwarding-table
export ASUS-LSP;

[edit]
rwibawa@vmx-13-12# show policy-options policy-statement ASUS-LSP
term 1 {
    from {
        rib bgp.l3vpn.0;
        community ASUS-1-1;
    }
    then {
        install-nexthop lsp r2-to-r1-b;
        accept;
    }
}
term 2 {
    from {
        rib bgp.l3vpn.0;
        community ASUS-1-2;
    }
    then {
        install-nexthop lsp r2-to-r1;
        accept;
    }
}
term default {
    then accept;
}

[edit]
rwibawa@vmx-13-12# show routing-instances ASUS
instance-type vrf;
interface ge-0/0/0.932;
interface lo0.932;
route-distinguisher 67.176.255.2:773;
inactive: vrf-import ASUS-import;
inactive: vrf-export ASUS-export;
vrf-target target:7041:773;
vrf-table-label;
protocols {
    ospf {
        export rw-redistribute-bgp-all;
        area 0.0.0.0 {
            interface all;
        }
    }
}

```


## Verification 

* traffic going to 77.3.0.11 will be using lsp r2-to-r1-b, the other prefix from R1 will be using lsp r2-to-r1

    ```

    rwibawa@vmx-13-12# run show route table ASUS.inet 77.3.0.11/32

    ASUS.inet.0: 37 destinations, 41 routes (37 active, 0 holddown, 0 hidden)
    + = Active Route, - = Last Active, * = Both

    77.3.0.11/32       *[BGP/170] 00:07:16, MED 1, localpref 100, from 67.176.255.103
                        AS path: I, validation-state: unverified
                        to 67.176.0.26 via ge-0/0/1.0, label-switched-path r2-to-r1-b



    rwibawa@vmx-13-12# run show route table ASUS.inet 77.3.0.111/32

    ASUS.inet.0: 37 destinations, 41 routes (37 active, 0 holddown, 0 hidden)
    + = Active Route, - = Last Active, * = Both

    77.3.0.111/32      *[BGP/170] 00:07:19, MED 1, localpref 100, from 67.176.255.103
                        AS path: I, validation-state: unverified
                        to 67.176.0.26 via ge-0/0/1.0, label-switched-path r2-to-r1




    rwibawa@vmx-13-12# run show route table ASUS.inet 77.3.0.11/32 detail

    ASUS.inet.0: 37 destinations, 41 routes (37 active, 0 holddown, 0 hidden)
    77.3.0.11/32 (1 entry, 1 announced)
            *BGP    Preference: 170/-101
                    Route Distinguisher: 67.176.255.1:773
                    Next hop type: Indirect
                    Address: 0xa5e7490
                    Next-hop reference count: 3
                    Source: 67.176.255.103
                    Next hop type: Router, Next hop index: 1048582
                    Next hop: 67.176.0.26 via ge-0/0/1.0 weight 0x1
                    Label-switched-path r2-to-r1
                    Label operation: Push 18
                    Label TTL action: prop-ttl
                    Load balance label: Label 18: None;
                    Session Id: 0x141
                    Next hop: 67.176.0.26 via ge-0/0/1.0 weight 0x1, selected
                    Label-switched-path r2-to-r1-b
                    Label operation: Push 18
                    Label TTL action: prop-ttl
                    Load balance label: Label 18: None;
                    Session Id: 0x141
                    Protocol next hop: 67.176.255.1
                    Label operation: Push 18
                    Label TTL action: prop-ttl
                    Load balance label: Label 18: None;
                    Indirect next hop: 0x97b9210 1048601 INH Session ID: 0x1e7
                    State: <Secondary Active Int Ext ProtectionCand>
                    Local AS: 1093737345 Peer AS: 1093737345
                    Age: 1:10       Metric: 1       Metric2: 1
                    Validation State: unverified
                    Task: BGP_1093737345.67.176.255.103+64248
                    Announcement bits (2): 0-KRT 1-ASUS-OSPF
                    AS path: I (Originator)
                    Cluster list:  67.176.255.103
                    Originator ID: 67.176.255.1
                    Communities: 773:101 target:7041:773
                    Import Accepted
                    VPN Label: 18
                    Localpref: 100
                    Router ID: 67.176.255.103
                    Primary Routing Table bgp.l3vpn.0

    [edit]
    rwibawa@vmx-13-12# run show route table ASUS.inet 77.3.0.111/32 detail

    ASUS.inet.0: 37 destinations, 41 routes (37 active, 0 holddown, 0 hidden)
    77.3.0.111/32 (1 entry, 1 announced)
            *BGP    Preference: 170/-101
                    Route Distinguisher: 67.176.255.1:773
                    Next hop type: Indirect
                    Address: 0xa5e6c20
                    Next-hop reference count: 21
                    Source: 67.176.255.103
                    Next hop type: Router, Next hop index: 1048582
                    Next hop: 67.176.0.26 via ge-0/0/1.0 weight 0x1, selected
                    Label-switched-path r2-to-r1
                    Label operation: Push 18
                    Label TTL action: prop-ttl
                    Load balance label: Label 18: None;
                    Session Id: 0x141
                    Next hop: 67.176.0.26 via ge-0/0/1.0 weight 0x1
                    Label-switched-path r2-to-r1-b
                    Label operation: Push 18
                    Label TTL action: prop-ttl
                    Load balance label: Label 18: None;
                    Session Id: 0x141
                    Protocol next hop: 67.176.255.1
                    Label operation: Push 18
                    Label TTL action: prop-ttl
                    Load balance label: Label 18: None;
                    Indirect next hop: 0x97b9100 1048600 INH Session ID: 0x1e7
                    State: <Secondary Active Int Ext ProtectionCand>
                    Local AS: 1093737345 Peer AS: 1093737345
                    Age: 1:21       Metric: 1       Metric2: 1
                    Validation State: unverified
                    Task: BGP_1093737345.67.176.255.103+64248
                    Announcement bits (2): 0-KRT 1-ASUS-OSPF
                    AS path: I (Originator)
                    Cluster list:  67.176.255.103
                    Originator ID: 67.176.255.1
                    Communities: 773:102 target:7041:773
                    Import Accepted
                    VPN Label: 18
                    Localpref: 100
                    Router ID: 67.176.255.103
                    Primary Routing Table bgp.l3vpn.0

    ```

