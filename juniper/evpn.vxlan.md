
## vmx01

#### interface

```
admin@vmx01# show interfaces ge-0/0/5
flexible-vlan-tagging;
encapsulation flexible-ethernet-services;
unit 0 {
    family bridge {
        interface-mode trunk;
        vlan-id-list [ 100 200 300 500 ];
    }
}


admin@vmx01# show interfaces irb
unit 100 {
    family inet {
        address 10.11.12.101/24;
    }
}
unit 300 {
    family inet {
        address 30.11.12.101/24;
    }
}
unit 500 {
    family inet {
        address 50.11.12.101/24;
    }
}
```

#### routing-instance

```
admin@vmx01# show routing-instances evpn1-vxlan-bd
vtep-source-interface lo0.0;
instance-type virtual-switch;
interface ge-0/0/5.0;
route-distinguisher 10.0.0.1:100;
vrf-target target:64200:100;
protocols {
    evpn {
        encapsulation vxlan;
        extended-vni-list 1100;
    }
}
bridge-domains {
    vlan100 {
        domain-type bridge;
        vlan-id 100;
        routing-interface irb.100;
        vxlan {
            vni 1100;
            ingress-node-replication;
        }
    }
    vlan200 {
        domain-type bridge;
        vlan-id 200;
        vxlan {
            vni 1200;
        }
    }
    vlan300 {
        domain-type bridge;
        vlan-id 300;
        routing-interface irb.300;
        vxlan {
            vni 1300;
        }
    }
    vlan500 {
        domain-type bridge;
        vlan-id 500;
        routing-interface irb.500;
        vxlan {
            vni 1500;
        }
    }
}


[edit]
admin@vmx01# show routing-instances evpn1-irb-vr
interface irb.100;

admin@vmx01# show routing-instances evpn2-type-5-mpls
instance-type vrf;
interface irb.300;
interface irb.500;
route-distinguisher 10.0.0.1:1001;
vrf-target target:64200:1001;
vrf-table-label;
protocols {
    evpn {
        ip-prefix-routes {
            advertise direct-nexthop;
            encapsulation mpls;
        }
    }
}
```

#### bgp

```
admin@vmx01# show routing-options autonomous-system
64200;

[edit]
admin@vmx01# show protocols bgp
group mesh {
    type internal;
    local-address 10.0.0.1;
    family evpn {
        signaling;
    }
    neighbor 10.0.0.2;
    neighbor 10.0.0.8;
    neighbor 10.0.0.9;
}
```



## vmx02


#### interface

```
admin@vmx02# show interfaces ge-0/0/5
flexible-vlan-tagging;
encapsulation flexible-ethernet-services;
unit 0 {
    family bridge {
        interface-mode trunk;
        vlan-id-list [ 100 200 500 310 ];
    }
}

[edit]
admin@vmx02# show interfaces irb
unit 100 {
    family inet {
        address 10.11.12.102/24;
    }
}
unit 200 {
    family inet {
        address 20.11.12.102/24;
    }
}
unit 310 {
    family inet {
        address 31.11.12.102/24;
    }
}
unit 500 {
    family inet {
        address 50.11.12.102/24;
    }
}

[edit]
admin@vmx02# show interfaces lo0
unit 0 {
    family inet {
        address 10.0.0.2/32;
    }
    family iso;
    family mpls;
}
```

#### routing-instance

```
admin@vmx02# show routing-instances evpn1-vxlan-bd
vtep-source-interface lo0.0;
instance-type virtual-switch;
interface ge-0/0/5.0;
route-distinguisher 10.0.0.2:100;
vrf-target target:64200:100;
protocols {
    evpn {
        encapsulation vxlan;
        extended-vni-list 1100;
    }
}
bridge-domains {
    vlan100 {
        domain-type bridge;
        vlan-id 100;
        routing-interface irb.100;
        vxlan {
            vni 1100;
        }
    }
    vlan200 {
        domain-type bridge;
        vlan-id 200;
        routing-interface irb.200;
        vxlan {
            vni 1200;
        }
    }
    vlan310 {
        domain-type bridge;
        vlan-id 310;
        routing-interface irb.310;
        vxlan {
            vni 1310;
        }
    }
    vlan500 {
        domain-type bridge;
        vlan-id 500;
        routing-interface irb.500;
        vxlan {
            vni 1500;
        }
    }
}

[edit]
admin@vmx02# show routing-instances evpn1-irb-vr
instance-type virtual-router;
interface irb.100;

[edit]
admin@vmx02# show routing-instances evpn2-type-5-mpls
vtep-source-interface lo0.0;
instance-type vrf;
interface irb.310;
interface irb.500;
interface lo0.1001; ## 'lo0.1001' is not defined
route-distinguisher 10.0.0.2:1001;
vrf-target target:64200:1001;
vrf-table-label;
protocols {
    evpn {
        ip-prefix-routes {
            advertise direct-nexthop;
            encapsulation mpls;
        }
    }
}
```

#### bgp

```
admin@vmx02# show routing-options autonomous-system
64200;

[edit]
admin@vmx02# show protocols bgp
group mesh {
    type internal;
    local-address 10.0.0.2;
    family evpn {
        signaling;
    }
    neighbor 10.0.0.1;
    neighbor 10.0.0.8;
    neighbor 10.0.0.9;
}
```

