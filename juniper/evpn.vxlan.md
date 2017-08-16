
## Topology

#### Diagram

```
 +------+                                                                                         +------+
 |      |0/0/6                                                                              0/0/6 |      |
 |ce1-1 +----------+                                                                 +------------+ ce2-1|
 |      +vl 100,500|      +---------+     +------+     +------+      +---------+     | vl 100,500,|      |
 +------+   400,700|0/0/5 |         |     |      |     |      |      |         |0/0/5|    600,700 +------+
                   +------+   PE1   +-----+  P3  +-----+  P4  +------+   PE2   +-----+
 +------+          |      |  vmx01  |     |      |     |      |      |  vmx02  |     |            +------+
 |      +vl 300    |      |         |     |      |     |      |      |         |     | Vl  Vl 310 |      |
 |ce1-2 +----------+      +---------+     +------+     +------+      +---------+     +------------+ ce2-2|
 |      |0/0/6                 |0/0/3.18                                             |      0/0/6 |      |
 +------+                      |                                                     |            +------+
                               |                                                     |
                               |                                                     |            +------+
                               |                                                     |     Vl 500 |      |
                               |swp1.18                                              +------------+  ce4 |
                          +---------+                                                        eth1 |      |
+-------+                 |         |                                                             +------+
|       |eth1         swp2| cumulus |
|  ce3  +-----------------+   01    |
|       | vl 100,500      |         |
+-------+                 +---------+
```

#### Detail

* 3 EVPN services
    * service 1: 
        * vlan 100: 
            * same vlan, same vni, route-type 2, vxlan encapsulation  on both side
        * vlan 400
            * only on vmx01, route-type 2 (vxlan encap) + type 5 (mpls encap)
            * opposite of vlan 600
        * vlan 500
            * same vlan, same vni, route-type 2, vxlan encapsulation on both side
            * no irb on vmx02
        * vlan 600
            * only on vmx01, route-type 2 (vxlan encap) + type 5 (mpls encap)
            * opposite of vlan 400
        * vlan 700
            * vlan 700 on vmx01
            * vlan 710 on vmx02
            * same vni, route-type 2, vxlan encapsulation  on both side
        * vlan 710
            * vlan 700 on vmx01
            * vlan 710 on vmx02
            * same vni, route-type 2, vxlan encapsulation  on both side

    * service 2: pure type-5
        * vlan 300
            * only on vmx01, route-type 5 only with mpls encapsulation
        * vlan 310
            * only on vmx02, route-type 5 only with mpls encapsulation


* Backbone Protocols
    * OSPF area 0
    * MPLS
    * LDP

* 3 PE devices
    * PE1: vmx 17.2
    * PE2: vmx 17.2
    * PE3: CumulusVX
    
* 5 CEs
    * CE1-1: logical-system of vmx01
        * vlan: 100, 400, 500, 700
    * CE1-2: logical-system of vmx01
        * vlan: 300
    * CE2-1: logical-system of vmx02
        * vlan: 100, 500, 600, 700
    * CE2-2: logical-system of vmx02
        * vlan: 310
    * CE3: ubuntu 
        * vlan: 100, 500
    * CE4: ubuntu
        * vlan: 100, 500



## Finding

* Cumulus Linux only support type 2 and 3
* some issue with vxlan routing, possibly related to symmetric vs asymmetric routing
* vlan 100:
    * no issue at all
* vlan 500
    * 50.11.12.1 and 50.11.12.2 can't ping each other but 50.11.12.2 and 50.11.12.101 can
        * most likely due to asymmetric bcause vmx02 has no irb for vlan 500
        * since vmx02 has no irb, and it has type 5 routes, it tried to use L3
    * 50.11.12.1, 50.11.12.3, 50.11.12.4 can ping each other
    * 50.11.12.4 and 50.11.12.101 works but not 50.11.12.101 and 50.11.12.3
* vlan 300/310
    * no issue, can ping each other
* vlan 400/600
    * 40.11.12.1 and 60.11.12.2 can ping each other
    * 10.1.0.21 and 10.1.0.11 can ping each other
* inter vlan routing

    * from CE4 to 40.11.12.x and 60.11.12.x
        
        ```
        root@u2:/home/ubuntu# ip r
        default via 100.64.1.1 dev eth0
        10.11.12.0/24 dev eth1.100  proto kernel  scope link  src 10.11.12.4
        40.11.12.0/24 via 10.11.12.101 dev eth1.100
        50.11.12.0/24 dev eth1.500  proto kernel  scope link  src 50.11.12.4
        60.11.12.0/24 via 10.11.12.101 dev eth1.100
        100.64.1.0/24 dev eth0  proto kernel  scope link  src 100.64.1.22

        root@u2:/home/ubuntu# traceroute to 60.11.12.2 (60.11.12.2), 30 hops max, 60 byte packets
         1  10.11.12.102 (10.11.12.102)  1.399 ms  1.361 ms  1.317 ms
         2  60.11.12.2 (60.11.12.2)  3.404 ms  3.384 ms  3.351 ms
        
        root@u2:/home/ubuntu# ping -s 10.11.12.4 60.11.12.2
        PING 60.11.12.2 (60.11.12.2) 10(38) bytes of data.
        18 bytes from 60.11.12.2: icmp_seq=1 ttl=63
        18 bytes from 60.11.12.2: icmp_seq=2 ttl=63
        ^C
        --- 60.11.12.2 ping statistics ---
        2 packets transmitted, 2 received, 0% packet loss, time 1001ms   
        
        root@u2:/home/ubuntu# traceroute 40.11.12.1
        traceroute to 40.11.12.1 (40.11.12.1), 30 hops max, 60 byte packets
         1  10.11.12.102 (10.11.12.102)  1.213 ms  1.169 ms  1.116 ms
         2  * * *
         3  40.11.12.1 (40.11.12.1)  5.981 ms  6.987 ms  6.960 ms
        root@u2:/home/ubuntu# ping -c 3 -s 10.11.12.4 40.11.12.1
        PING 40.11.12.1 (40.11.12.1) 10(38) bytes of data.
        18 bytes from 40.11.12.1: icmp_seq=1 ttl=62
        18 bytes from 40.11.12.1: icmp_seq=2 ttl=62
        18 bytes from 40.11.12.1: icmp_seq=3 ttl=62

        --- 40.11.12.1 ping statistics ---
        3 packets transmitted, 3 received, 0% packet loss, time 2003ms
        ```
        
    * from CE3 to 40.11.12.x and 60.11.12.x
    
```
root@u1:/home/ubuntu# ping -c 3 -s 10.11.12.3 10.11.12.1
PING 10.11.12.1 (10.11.12.1) 10(38) bytes of data.
18 bytes from 10.11.12.1: icmp_seq=1 ttl=64
18 bytes from 10.11.12.1: icmp_seq=2 ttl=64
18 bytes from 10.11.12.1: icmp_seq=3 ttl=64

--- 10.11.12.1 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2003ms

root@u1:/home/ubuntu# ping -c 3 -s 10.11.12.3 10.11.12.2
PING 10.11.12.2 (10.11.12.2) 10(38) bytes of data.
18 bytes from 10.11.12.2: icmp_seq=1 ttl=64
18 bytes from 10.11.12.2: icmp_seq=2 ttl=64
18 bytes from 10.11.12.2: icmp_seq=3 ttl=64

--- 10.11.12.2 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2003ms

root@u1:/home/ubuntu# ping -c 3 -s 10.11.12.3 10.11.12.4
PING 10.11.12.4 (10.11.12.4) 10(38) bytes of data.
18 bytes from 10.11.12.4: icmp_seq=1 ttl=64
18 bytes from 10.11.12.4: icmp_seq=2 ttl=64
18 bytes from 10.11.12.4: icmp_seq=3 ttl=64

--- 10.11.12.4 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2002ms



root@u1:/home/ubuntu# ping -c 2 -s 50.11.12.3 50.11.12.1
PING 50.11.12.1 (50.11.12.1) 50(78) bytes of data.
58 bytes from 50.11.12.1: icmp_seq=1 ttl=64 time=2.45 ms
58 bytes from 50.11.12.1: icmp_seq=2 ttl=64 time=2.30 ms

--- 50.11.12.1 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1001ms
rtt min/avg/max/mdev = 2.302/2.377/2.452/0.075 ms
root@u1:/home/ubuntu# ping -c 2 -s 50.11.12.3 50.11.12.2
PING 50.11.12.2 (50.11.12.2) 50(78) bytes of data.
From 50.11.12.3 icmp_seq=1 Destination Host Unreachable
From 50.11.12.3 icmp_seq=2 Destination Host Unreachable

--- 50.11.12.2 ping statistics ---
2 packets transmitted, 0 received, +2 errors, 100% packet loss, time 1007ms
pipe 2
root@u1:/home/ubuntu# ping -c 2 -s 50.11.12.3 50.11.12.4
PING 50.11.12.4 (50.11.12.4) 50(78) bytes of data.
58 bytes from 50.11.12.4: icmp_seq=1 ttl=64 time=8.46 ms
58 bytes from 50.11.12.4: icmp_seq=2 ttl=64 time=5.09 ms

--- 50.11.12.4 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1001ms
rtt min/avg/max/mdev = 5.095/6.780/8.466/1.687 ms


PING 50.11.12.101 (50.11.12.101) 50(78) bytes of data.
^C
--- 50.11.12.101 ping statistics ---
2 packets transmitted, 0 received, 100% packet loss, time 1008ms

root@u1:/home/ubuntu# ping -c 2 -s 50.11.12.3 50.11.12.102
PING 50.11.12.102 (50.11.12.102) 50(78) bytes of data.
From 50.11.12.3 icmp_seq=1 Destination Host Unreachable
From 50.11.12.3 icmp_seq=2 Destination Host Unreachable

--- 50.11.12.102 ping statistics ---
2 packets transmitted, 0 received, +2 errors, 100% packet loss, time 1009ms

```



## Config

### vmx01

#### interface

```
[edit]
admin@vmx01# show interfaces ge-0/0/5
flexible-vlan-tagging;
encapsulation flexible-ethernet-services;
unit 0 {
    family bridge {
        interface-mode trunk;
        vlan-id-list [ 100 500 300 700 400 ];
    }
}

[edit]
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
unit 400 {
    family inet {
        address 40.11.12.102/24;
    }
}
unit 500 {
    family inet {
        address 50.11.12.101/24;
    }
}
unit 700 {
    family inet {
        address 70.11.12.101/24;
    }
}
```

#### routing-instance

```
admin@vmx01# show routing-instances
evpn1-type-5-mpls {
    instance-type vrf;
    interface irb.100;
    interface irb.400;
    interface irb.700;
    route-distinguisher 10.0.0.1:1001;
    vrf-target target:64200:1001;
    vrf-table-label;
    protocols {
        ospf {
            export evpn_routes;
            area 0.0.1.244 {
                interface irb.700;
                interface irb.400;
            }
        }
        evpn {
            ip-prefix-routes {
                advertise direct-nexthop;
                encapsulation mpls;
                export [ ospf_routes direct_routes ];
            }
        }
    }
}
evpn1-vxlan-bd {
    vtep-source-interface lo0.0;
    instance-type virtual-switch;
    interface ge-0/0/5.0;
    route-distinguisher 10.0.0.1:100;
    vrf-target target:64200:100;
    protocols {
        evpn {
            encapsulation vxlan;
            extended-vni-list [ 1100 1400 1500 1700 ];
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
        vlan300 {
            domain-type bridge;
            vlan-id 300;
            routing-interface irb.300;
            vxlan {
                vni 1300;
            }
        }
        vlan400 {
            domain-type bridge;
            vlan-id 400;
            routing-interface irb.400;
            vxlan {
                vni 1400;
                ingress-node-replication;
            }
        }
        vlan500 {
            domain-type bridge;
            vlan-id 500;
            routing-interface irb.500;
            vxlan {
                vni 1500;
                ingress-node-replication;
            }
        }
        vlan700 {
            domain-type bridge;
            vlan-id 700;
            routing-interface irb.700;
            vxlan {
                vni 1700;
                ingress-node-replication;
            }
        }
    }
}
evpn2-type-5-mpls {
    instance-type vrf;
    interface irb.300;
    route-distinguisher 10.0.0.1:1002;
    vrf-target target:64200:1002;
    vrf-table-label;
    protocols {
        evpn {
            ip-prefix-routes {
                advertise direct-nexthop;
                encapsulation mpls;
            }
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
}
```



### vmx02


#### interface

```
admin@vmx02# show interfaces ge-0/0/5
flexible-vlan-tagging;
encapsulation flexible-ethernet-services;
unit 0 {
    family bridge {
        interface-mode trunk;
        vlan-id-list [ 100 500 310 600 710 ];
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
    family inet;
}
unit 310 {
    family inet {
        address 31.11.12.102/24;
    }
}
unit 600 {
    family inet {
        address 60.11.12.102/24;
    }
}
unit 700 {
    family inet {
        address 70.11.12.102/24;
    }
}
```

#### routing-instance

```
admin@vmx02# show routing-instances
evpn1-type-5-mpls {
    instance-type vrf;
    interface irb.100;
    interface irb.600;
    interface irb.700;
    route-distinguisher 10.0.0.1:1001;
    vrf-target target:64200:1001;
    vrf-table-label;
    protocols {
        ospf {
            export evpn_routes;
            area 0.0.1.244 {
                interface irb.600;
                interface irb.700;
            }
        }
        evpn {
            ip-prefix-routes {
                advertise direct-nexthop;
                encapsulation mpls;
                export [ ospf_routes direct_routes ];
            }
        }
    }
}
evpn1-vxlan-bd {
    vtep-source-interface lo0.0;
    instance-type virtual-switch;
    interface ge-0/0/5.0;
    route-distinguisher 10.0.0.1:100;
    vrf-target target:64200:100;
    protocols {
        evpn {
            encapsulation vxlan;
            extended-vni-list [ 1100 1500 1600 1700 ];
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
            vxlan {
                vni 1500;
                ingress-node-replication;
            }
        }
        vlan600 {
            domain-type bridge;
            vlan-id 600;
            routing-interface irb.600;
            vxlan {
                vni 1600;
                ingress-node-replication;
            }
        }
        vlan710 {
            domain-type bridge;
            vlan-id 710;
            routing-interface irb.700;
            vxlan {
                vni 1700;
                ingress-node-replication;
            }
        }
    }
}
evpn2-type-5-mpls {
    instance-type vrf;
    interface irb.310;
    route-distinguisher 10.0.0.1:1002;
    vrf-target target:64200:1002;
    vrf-table-label;
    protocols {
        evpn {
            ip-prefix-routes {
                advertise direct-nexthop;
                encapsulation mpls;
            }
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
}
```


### routes

#### vmx01

```
admin@vmx01# run show route table evpn

evpn1-type-5-mpls.inet.0: 20 destinations, 23 routes (20 active, 0 holddown, 0 hidden)
+ = Active Route, - = Last Active, * = Both

10.1.0.11/32       *[OSPF/10] 00:58:59, metric 1
                    > to 40.11.12.1 via irb.400
10.1.0.21/32       *[OSPF/10] 05:13:46, metric 2
                    > to 70.11.12.102 via irb.700
10.11.12.0/24      *[Direct/0] 08:00:01
                    > via irb.100
10.11.12.1/32      *[EVPN/7] 00:01:56
                    > via irb.100
                    [EVPN/170] 05:13:46
                    > to 10.1.3.2 via ge-0/0/1.13, Push 16, Push 299840(top)
10.11.12.2/32      *[OSPF/150] 05:13:46, metric 0, tag 0
                    > to 70.11.12.102 via irb.700
10.11.12.4/32      *[OSPF/150] 01:37:32, metric 0, tag 0
                    > to 70.11.12.102 via irb.700
10.11.12.101/32    *[Local/0] 08:00:01
                      Local via irb.100
40.11.12.0/24      *[Direct/0] 00:59:39
                    > via irb.400
40.11.12.1/32      *[EVPN/7] 00:59:38
                    > via irb.400
                    [EVPN/170] 01:00:36
                    > to 10.1.3.2 via ge-0/0/1.13, Push 16, Push 299840(top)
40.11.12.2/32      *[EVPN/170] 05:11:17
                    > to 10.1.3.2 via ge-0/0/1.13, Push 16, Push 299840(top)
40.11.12.101/32    *[Local/0] 00:59:39
                      Local via irb.400
50.11.12.0/24      *[Direct/0] 00:21:45
                    > via irb.500
                    [OSPF/150] 00:21:45, metric 0, tag 0
                    > to 70.11.12.102 via irb.700
50.11.12.1/32      *[EVPN/170] 05:13:46
                    > to 10.1.3.2 via ge-0/0/1.13, Push 16, Push 299840(top)
50.11.12.101/32    *[Local/0] 00:21:45
                      Local via irb.500
51.11.12.2/32      *[OSPF/150] 05:13:46, metric 0, tag 0
                    > to 70.11.12.102 via irb.700
60.11.12.0/24      *[OSPF/10] 05:13:46, metric 2
                    > to 70.11.12.102 via irb.700
60.11.12.2/32      *[OSPF/150] 05:13:46, metric 0, tag 0
                    > to 70.11.12.102 via irb.700
70.11.12.0/24      *[Direct/0] 05:13:57
                    > via irb.700
70.11.12.101/32    *[Local/0] 05:13:57
                      Local via irb.700
224.0.0.5/32       *[OSPF/10] 07:45:44, metric 1
                      MultiRecv

evpn2-type-5-mpls.inet.0: 3 destinations, 3 routes (3 active, 0 holddown, 0 hidden)
+ = Active Route, - = Last Active, * = Both

30.11.12.0/24      *[Direct/0] 07:53:46
                    > via irb.300
30.11.12.101/32    *[Local/0] 07:53:46
                      Local via irb.300
31.11.12.0/24      *[EVPN/170] 06:02:09
                    > to 10.1.3.2 via ge-0/0/1.13, Push 17, Push 299840(top)

evpn1-type-5-mpls.evpn.0: 16 destinations, 23 routes (16 active, 0 holddown, 0 hidden)
+ = Active Route, - = Last Active, * = Both

5:10.0.0.1:1001::0::10.11.12.0::24/248
                   *[EVPN/170] 07:25:42
                      Indirect
                    [BGP/170] 07:24:45, localpref 100, from 10.0.0.2
                      AS path: I, validation-state: unverified
                    > to 10.1.3.2 via ge-0/0/1.13, Push 299840
5:10.0.0.1:1001::0::40.11.12.0::24/248
                   *[EVPN/170] 05:11:59
                      Indirect
                    [BGP/170] 00:58:59, localpref 100, from 10.0.0.2
                      AS path: I, validation-state: unverified
                    > to 10.1.3.2 via ge-0/0/1.13, Push 299840
5:10.0.0.1:1001::0::50.11.12.0::24/248
                   *[EVPN/170] 00:21:45
                      Indirect
5:10.0.0.1:1001::0::60.11.12.0::24/248
                   *[EVPN/170] 05:13:46
                      Indirect
                    [BGP/170] 05:14:35, localpref 100, from 10.0.0.2
                      AS path: I, validation-state: unverified
                    > to 10.1.3.2 via ge-0/0/1.13, Push 299840
5:10.0.0.1:1001::0::70.11.12.0::24/248
                   *[EVPN/170] 05:13:57
                      Indirect
                    [BGP/170] 05:14:35, localpref 100, from 10.0.0.2
                      AS path: I, validation-state: unverified
                    > to 10.1.3.2 via ge-0/0/1.13, Push 299840
5:10.0.0.1:1001::0::10.1.0.11::32/248
                   *[EVPN/170] 00:58:59
                      Indirect
                    [BGP/170] 00:58:59, localpref 100, from 10.0.0.2
                      AS path: I, validation-state: unverified
                    > to 10.1.3.2 via ge-0/0/1.13, Push 299840
5:10.0.0.1:1001::0::10.1.0.21::32/248
                   *[EVPN/170] 05:13:46
                      Indirect
                    [BGP/170] 05:13:55, localpref 100, from 10.0.0.2
                      AS path: I, validation-state: unverified
                    > to 10.1.3.2 via ge-0/0/1.13, Push 299840
5:10.0.0.1:1001::0::10.11.12.1::32/248
                   *[BGP/170] 05:13:46, localpref 100, from 10.0.0.2
                      AS path: I, validation-state: unverified
                    > to 10.1.3.2 via ge-0/0/1.13, Push 299840
5:10.0.0.1:1001::0::10.11.12.2::32/248
                   *[EVPN/170] 05:13:46
                      Indirect
5:10.0.0.1:1001::0::10.11.12.4::32/248
                   *[EVPN/170] 01:37:32
                      Indirect
5:10.0.0.1:1001::0::40.11.12.1::32/248
                   *[BGP/170] 01:00:36, localpref 100, from 10.0.0.2
                      AS path: I, validation-state: unverified
                    > to 10.1.3.2 via ge-0/0/1.13, Push 299840
5:10.0.0.1:1001::0::40.11.12.2::32/248
                   *[BGP/170] 05:11:17, localpref 100, from 10.0.0.2
                      AS path: I, validation-state: unverified
                    > to 10.1.3.2 via ge-0/0/1.13, Push 299840
5:10.0.0.1:1001::0::50.11.12.1::32/248
                   *[BGP/170] 05:13:46, localpref 100, from 10.0.0.2
                      AS path: I, validation-state: unverified
                    > to 10.1.3.2 via ge-0/0/1.13, Push 299840
5:10.0.0.1:1001::0::51.11.12.2::32/248
                   *[EVPN/170] 05:13:46
                      Indirect
5:10.0.0.1:1001::0::60.11.12.2::32/248
                   *[EVPN/170] 05:13:46
                      Indirect
5:10.0.0.1:1001::0::224.0.0.5::32/248
                   *[EVPN/170] 07:35:37
                      Indirect
                    [BGP/170] 07:34:00, localpref 100, from 10.0.0.2
                      AS path: I, validation-state: unverified
                    > to 10.1.3.2 via ge-0/0/1.13, Push 299840

evpn2-type-5-mpls.evpn.0: 2 destinations, 2 routes (2 active, 0 holddown, 0 hidden)
+ = Active Route, - = Last Active, * = Both

5:10.0.0.1:1002::0::30.11.12.0::24/248
                   *[EVPN/170] 07:53:46
                      Indirect
5:10.0.0.1:1002::0::31.11.12.0::24/248
                   *[BGP/170] 06:02:09, localpref 100, from 10.0.0.2
                      AS path: I, validation-state: unverified
                    > to 10.1.3.2 via ge-0/0/1.13, Push 299840

evpn1-vxlan-bd.evpn.0: 42 destinations, 42 routes (42 active, 0 holddown, 0 hidden)
+ = Active Route, - = Last Active, * = Both

1:10.0.0.2:0::050000fac80000044c00::FFFF:FFFF/192 AD/ESI
                   *[BGP/170] 08:02:05, localpref 100, from 10.0.0.2
                      AS path: I, validation-state: unverified
                    > to 10.1.3.2 via ge-0/0/1.13, Push 299840
1:10.0.0.2:0::050000fac80000051e00::FFFF:FFFF/192 AD/ESI
                   *[BGP/170] 06:02:09, localpref 100, from 10.0.0.2
                      AS path: I, validation-state: unverified
                    > to 10.1.3.2 via ge-0/0/1.13, Push 299840
1:10.0.0.2:0::050000fac80000064000::FFFF:FFFF/192 AD/ESI
                   *[BGP/170] 05:14:34, localpref 100, from 10.0.0.2
                      AS path: I, validation-state: unverified
                    > to 10.1.3.2 via ge-0/0/1.13, Push 299840
1:10.0.0.2:0::050000fac8000006a400::FFFF:FFFF/192 AD/ESI
                   *[BGP/170] 05:14:34, localpref 100, from 10.0.0.2
                      AS path: I, validation-state: unverified
                    > to 10.1.3.2 via ge-0/0/1.13, Push 299840
2:10.0.0.1:100::1100::00:05:86:35:e9:f0/304 MAC/IP
                   *[BGP/170] 08:02:05, localpref 100, from 10.0.0.2
                      AS path: I, validation-state: unverified
                    > to 10.1.3.2 via ge-0/0/1.13, Push 299840
2:10.0.0.1:100::1100::00:05:86:5f:ce:f0/304 MAC/IP
                   *[EVPN/170] 08:00:00
                      Indirect
2:10.0.0.1:100::1100::02:30:7b:77:27:c5/304 MAC/IP
                   *[BGP/170] 05:48:32, localpref 100, from 10.0.0.2
                      AS path: I, validation-state: unverified
                    > to 10.1.3.2 via ge-0/0/1.13, Push 299840
2:10.0.0.1:100::1100::02:70:8a:fc:05:8a/304 MAC/IP
                   *[EVPN/170] 00:01:56
                      Indirect
2:10.0.0.1:100::1100::02:79:90:c0:1e:0f/304 MAC/IP
                   *[BGP/170] 01:37:32, localpref 100, from 10.0.0.2
                      AS path: I, validation-state: unverified
                    > to 10.1.3.2 via ge-0/0/1.13, Push 299840
2:10.0.0.1:100::1400::00:05:86:5f:ce:f0/304 MAC/IP
                   *[EVPN/170] 05:11:58
                      Indirect
2:10.0.0.1:100::1400::02:70:8a:fc:05:8a/304 MAC/IP
                   *[EVPN/170] 05:11:58
                      Indirect
2:10.0.0.1:100::1500::00:05:86:5f:ce:f0/304 MAC/IP
                   *[EVPN/170] 00:21:44
                      Indirect
2:10.0.0.1:100::1500::02:30:7b:77:27:c5/304 MAC/IP
                   *[BGP/170] 00:02:22, localpref 100, from 10.0.0.2
                      AS path: I, validation-state: unverified
                    > to 10.1.3.2 via ge-0/0/1.13, Push 299840
2:10.0.0.1:100::1500::02:79:90:c0:1e:0f/304 MAC/IP
                   *[BGP/170] 00:09:24, localpref 100, from 10.0.0.2
                      AS path: I, validation-state: unverified
                    > to 10.1.3.2 via ge-0/0/1.13, Push 299840
2:10.0.0.1:100::1600::00:05:86:35:e9:f0/304 MAC/IP
                   *[BGP/170] 05:14:34, localpref 100, from 10.0.0.2
                      AS path: I, validation-state: unverified
                    > to 10.1.3.2 via ge-0/0/1.13, Push 299840
2:10.0.0.1:100::1600::02:30:7b:77:27:c5/304 MAC/IP
                   *[BGP/170] 05:14:32, localpref 100, from 10.0.0.2
                      AS path: I, validation-state: unverified
                    > to 10.1.3.2 via ge-0/0/1.13, Push 299840
2:10.0.0.1:100::1700::00:05:86:35:e9:f0/304 MAC/IP
                   *[BGP/170] 05:14:34, localpref 100, from 10.0.0.2
                      AS path: I, validation-state: unverified
                    > to 10.1.3.2 via ge-0/0/1.13, Push 299840
2:10.0.0.1:100::1700::00:05:86:5f:ce:f0/304 MAC/IP
                   *[EVPN/170] 05:13:56
                      Indirect
2:10.0.0.1:100::1700::02:30:7b:77:27:c5/304 MAC/IP
                   *[BGP/170] 00:04:18, localpref 100, from 10.0.0.2
                      AS path: I, validation-state: unverified
                    > to 10.1.3.2 via ge-0/0/1.13, Push 299840
2:10.0.0.1:100::1700::02:70:8a:fc:05:8a/304 MAC/IP
                   *[EVPN/170] 00:04:18
                      Indirect
2:10.0.0.1:100::1100::00:05:86:35:e9:f0::10.11.12.102/304 MAC/IP
                   *[BGP/170] 08:02:05, localpref 100, from 10.0.0.2
                      AS path: I, validation-state: unverified
                    > to 10.1.3.2 via ge-0/0/1.13, Push 299840
2:10.0.0.1:100::1100::00:05:86:5f:ce:f0::10.11.12.101/304 MAC/IP
                   *[EVPN/170] 08:00:00
                      Indirect
2:10.0.0.1:100::1100::02:30:7b:77:27:c5::10.11.12.2/304 MAC/IP
                   *[BGP/170] 05:48:14, localpref 100, from 10.0.0.2
                      AS path: I, validation-state: unverified
                    > to 10.1.3.2 via ge-0/0/1.13, Push 299840
2:10.0.0.1:100::1100::02:70:8a:fc:05:8a::10.11.12.1/304 MAC/IP
                   *[EVPN/170] 00:01:56
                      Indirect
2:10.0.0.1:100::1100::02:79:90:c0:1e:0f::10.11.12.4/304 MAC/IP
                   *[BGP/170] 01:37:32, localpref 100, from 10.0.0.2
                      AS path: I, validation-state: unverified
                    > to 10.1.3.2 via ge-0/0/1.13, Push 299840
2:10.0.0.1:100::1400::00:05:86:5f:ce:f0::40.11.12.101/304 MAC/IP
                   *[EVPN/170] 00:59:39
                      Indirect
2:10.0.0.1:100::1400::02:70:8a:fc:05:8a::40.11.12.1/304 MAC/IP
                   *[EVPN/170] 00:59:38
                      Indirect
2:10.0.0.1:100::1500::00:05:86:5f:ce:f0::50.11.12.101/304 MAC/IP
                   *[EVPN/170] 00:21:44
                      Indirect
2:10.0.0.1:100::1600::00:05:86:35:e9:f0::60.11.12.102/304 MAC/IP
                   *[BGP/170] 05:14:34, localpref 100, from 10.0.0.2
                      AS path: I, validation-state: unverified
                    > to 10.1.3.2 via ge-0/0/1.13, Push 299840
2:10.0.0.1:100::1600::02:30:7b:77:27:c5::60.11.12.2/304 MAC/IP
                   *[BGP/170] 05:13:54, localpref 100, from 10.0.0.2
                      AS path: I, validation-state: unverified
                    > to 10.1.3.2 via ge-0/0/1.13, Push 299840
2:10.0.0.1:100::1700::00:05:86:35:e9:f0::70.11.12.102/304 MAC/IP
                   *[BGP/170] 05:14:34, localpref 100, from 10.0.0.2
                      AS path: I, validation-state: unverified
                    > to 10.1.3.2 via ge-0/0/1.13, Push 299840
2:10.0.0.1:100::1700::00:05:86:5f:ce:f0::70.11.12.101/304 MAC/IP
                   *[EVPN/170] 05:13:56
                      Indirect
2:10.0.0.8:100::0::02:1c:a7:ef:4d:dc::10.11.12.3/304 MAC/IP
                   *[BGP/170] 05:28:51, localpref 100, from 10.0.0.8
                      AS path: I, validation-state: unverified
                    > to 10.1.8.2 via ge-0/0/3.18
3:10.0.0.1:100::1100::10.0.0.1/248 IM
                   *[EVPN/170] 09:32:42
                      Indirect
3:10.0.0.1:100::1100::10.0.0.2/248 IM
                   *[BGP/170] 08:02:04, localpref 100, from 10.0.0.2
                      AS path: I, validation-state: unverified
                    > to 10.1.3.2 via ge-0/0/1.13, Push 299840
3:10.0.0.1:100::1400::10.0.0.1/248 IM
                   *[EVPN/170] 05:11:58
                      Indirect
3:10.0.0.1:100::1500::10.0.0.1/248 IM
                   *[EVPN/170] 07:53:44
                      Indirect
3:10.0.0.1:100::1500::10.0.0.2/248 IM
                   *[BGP/170] 07:54:06, localpref 100, from 10.0.0.2
                      AS path: I, validation-state: unverified
                    > to 10.1.3.2 via ge-0/0/1.13, Push 299840
3:10.0.0.1:100::1600::10.0.0.2/248 IM
                   *[BGP/170] 05:14:33, localpref 100, from 10.0.0.2
                      AS path: I, validation-state: unverified
                    > to 10.1.3.2 via ge-0/0/1.13, Push 299840
3:10.0.0.1:100::1700::10.0.0.1/248 IM
                   *[EVPN/170] 05:13:56
                      Indirect
3:10.0.0.1:100::1700::10.0.0.2/248 IM
                   *[BGP/170] 05:14:33, localpref 100, from 10.0.0.2
                      AS path: I, validation-state: unverified
                    > to 10.1.3.2 via ge-0/0/1.13, Push 299840
3:10.0.0.8:100::0::10.0.0.8/248 IM
                   *[BGP/170] 05:28:51, localpref 100, from 10.0.0.8
                      AS path: I, validation-state: unverified
                    > to 10.1.8.2 via ge-0/0/3.18

```

#### vmx02

```
admin@vmx02# run show route table evpn

evpn1-type-5-mpls.inet.0: 19 destinations, 22 routes (19 active, 0 holddown, 0 hidden)
+ = Active Route, - = Last Active, * = Both

10.1.0.11/32       *[OSPF/10] 00:59:35, metric 2
                    > to 70.11.12.101 via irb.700
10.1.0.21/32       *[OSPF/10] 05:14:31, metric 1
                    > to 60.11.12.2 via irb.600
10.11.12.0/24      *[Direct/0] 08:02:41
                    > via irb.100
10.11.12.1/32      *[OSPF/150] 05:14:22, metric 0, tag 0
                    > to 70.11.12.101 via irb.700
10.11.12.2/32      *[EVPN/7] 00:00:09
                    > via irb.100
                    [EVPN/170] 05:14:22
                    > to 10.2.4.2 via ge-0/0/1.24, Push 16, Push 299792(top)
10.11.12.4/32      *[EVPN/7] 00:02:30
                    > via irb.100
                    [EVPN/170] 01:38:08
                    > to 10.2.4.2 via ge-0/0/1.24, Push 16, Push 299792(top)
10.11.12.102/32    *[Local/0] 08:02:41
                      Local via irb.100
40.11.12.0/24      *[OSPF/10] 00:59:35, metric 2
                    > to 70.11.12.101 via irb.700
40.11.12.1/32      *[OSPF/150] 01:01:12, metric 0, tag 0
                    > to 70.11.12.101 via irb.700
40.11.12.2/32      *[OSPF/150] 05:11:54, metric 0, tag 0
                    > to 70.11.12.101 via irb.700
50.11.12.0/24      *[EVPN/170] 00:22:21
                    > to 10.2.4.2 via ge-0/0/1.24, Push 16, Push 299792(top)
50.11.12.1/32      *[OSPF/150] 05:14:22, metric 0, tag 0
                    > to 70.11.12.101 via irb.700
51.11.12.2/32      *[EVPN/170] 05:14:22
                    > to 10.2.4.2 via ge-0/0/1.24, Push 16, Push 299792(top)
60.11.12.0/24      *[Direct/0] 05:15:11
                    > via irb.600
60.11.12.2/32      *[EVPN/7] 05:14:30
                    > via irb.600
                    [EVPN/170] 05:14:22
                    > to 10.2.4.2 via ge-0/0/1.24, Push 16, Push 299792(top)
60.11.12.102/32    *[Local/0] 05:15:11
                      Local via irb.600
70.11.12.0/24      *[Direct/0] 05:15:11
                    > via irb.700
70.11.12.102/32    *[Local/0] 05:15:11
                      Local via irb.700
224.0.0.5/32       *[OSPF/10] 07:34:37, metric 1
                      MultiRecv

evpn2-type-5-mpls.inet.0: 3 destinations, 3 routes (3 active, 0 holddown, 0 hidden)
+ = Active Route, - = Last Active, * = Both

30.11.12.0/24      *[EVPN/170] 08:00:31
                    > to 10.2.4.2 via ge-0/0/1.24, Push 17, Push 299792(top)
31.11.12.0/24      *[Direct/0] 06:02:46
                    > via irb.310
31.11.12.102/32    *[Local/0] 06:02:46
                      Local via irb.310

evpn1-type-5-mpls.evpn.0: 16 destinations, 23 routes (16 active, 0 holddown, 0 hidden)
+ = Active Route, - = Last Active, * = Both

5:10.0.0.1:1001::0::10.11.12.0::24/248
                   *[EVPN/170] 07:25:22
                      Indirect
                    [BGP/170] 07:26:18, localpref 100, from 10.0.0.1
                      AS path: I, validation-state: unverified
                    > to 10.2.4.2 via ge-0/0/1.24, Push 299792
5:10.0.0.1:1001::0::40.11.12.0::24/248
                   *[EVPN/170] 00:59:35
                      Indirect
                    [BGP/170] 05:12:35, localpref 100, from 10.0.0.1
                      AS path: I, validation-state: unverified
                    > to 10.2.4.2 via ge-0/0/1.24, Push 299792
5:10.0.0.1:1001::0::50.11.12.0::24/248
                   *[BGP/170] 00:22:21, localpref 100, from 10.0.0.1
                      AS path: I, validation-state: unverified
                    > to 10.2.4.2 via ge-0/0/1.24, Push 299792
5:10.0.0.1:1001::0::60.11.12.0::24/248
                   *[EVPN/170] 05:15:11
                      Indirect
                    [BGP/170] 05:14:22, localpref 100, from 10.0.0.1
                      AS path: I, validation-state: unverified
                    > to 10.2.4.2 via ge-0/0/1.24, Push 299792
5:10.0.0.1:1001::0::70.11.12.0::24/248
                   *[EVPN/170] 05:15:11
                      Indirect
                    [BGP/170] 05:14:33, localpref 100, from 10.0.0.1
                      AS path: I, validation-state: unverified
                    > to 10.2.4.2 via ge-0/0/1.24, Push 299792
5:10.0.0.1:1001::0::10.1.0.11::32/248
                   *[EVPN/170] 00:59:35
                      Indirect
                    [BGP/170] 00:59:35, localpref 100, from 10.0.0.1
                      AS path: I, validation-state: unverified
                    > to 10.2.4.2 via ge-0/0/1.24, Push 299792
5:10.0.0.1:1001::0::10.1.0.21::32/248
                   *[EVPN/170] 05:14:31
                      Indirect
                    [BGP/170] 05:14:22, localpref 100, from 10.0.0.1
                      AS path: I, validation-state: unverified
                    > to 10.2.4.2 via ge-0/0/1.24, Push 299792
5:10.0.0.1:1001::0::10.11.12.1::32/248
                   *[EVPN/170] 05:14:22
                      Indirect
5:10.0.0.1:1001::0::10.11.12.2::32/248
                   *[BGP/170] 05:14:22, localpref 100, from 10.0.0.1
                      AS path: I, validation-state: unverified
                    > to 10.2.4.2 via ge-0/0/1.24, Push 299792
5:10.0.0.1:1001::0::10.11.12.4::32/248
                   *[BGP/170] 01:38:08, localpref 100, from 10.0.0.1
                      AS path: I, validation-state: unverified
                    > to 10.2.4.2 via ge-0/0/1.24, Push 299792
5:10.0.0.1:1001::0::40.11.12.1::32/248
                   *[EVPN/170] 01:01:12
                      Indirect
5:10.0.0.1:1001::0::40.11.12.2::32/248
                   *[EVPN/170] 05:11:54
                      Indirect
5:10.0.0.1:1001::0::50.11.12.1::32/248
                   *[EVPN/170] 05:14:22
                      Indirect
5:10.0.0.1:1001::0::51.11.12.2::32/248
                   *[BGP/170] 05:14:22, localpref 100, from 10.0.0.1
                      AS path: I, validation-state: unverified
                    > to 10.2.4.2 via ge-0/0/1.24, Push 299792
5:10.0.0.1:1001::0::60.11.12.2::32/248
                   *[BGP/170] 05:14:22, localpref 100, from 10.0.0.1
                      AS path: I, validation-state: unverified
                    > to 10.2.4.2 via ge-0/0/1.24, Push 299792
5:10.0.0.1:1001::0::224.0.0.5::32/248
                   *[EVPN/170] 07:34:37
                      Indirect
                    [BGP/170] 07:36:13, localpref 100, from 10.0.0.1
                      AS path: I, validation-state: unverified
                    > to 10.2.4.2 via ge-0/0/1.24, Push 299792

evpn2-type-5-mpls.evpn.0: 2 destinations, 2 routes (2 active, 0 holddown, 0 hidden)
+ = Active Route, - = Last Active, * = Both

5:10.0.0.1:1002::0::30.11.12.0::24/248
                   *[BGP/170] 07:54:22, localpref 100, from 10.0.0.1
                      AS path: I, validation-state: unverified
                    > to 10.2.4.2 via ge-0/0/1.24, Push 299792
5:10.0.0.1:1002::0::31.11.12.0::24/248
                   *[EVPN/170] 06:02:46
                      Indirect

evpn1-vxlan-bd.evpn.0: 43 destinations, 43 routes (43 active, 0 holddown, 0 hidden)
+ = Active Route, - = Last Active, * = Both

1:10.0.0.1:0::050000fac80000044c00::FFFF:FFFF/192 AD/ESI
                   *[BGP/170] 09:33:18, localpref 100, from 10.0.0.1
                      AS path: I, validation-state: unverified
                    > to 10.2.4.2 via ge-0/0/1.24, Push 299792
1:10.0.0.1:0::050000fac80000051400::FFFF:FFFF/192 AD/ESI
                   *[BGP/170] 07:54:21, localpref 100, from 10.0.0.1
                      AS path: I, validation-state: unverified
                    > to 10.2.4.2 via ge-0/0/1.24, Push 299792
1:10.0.0.1:0::050000fac80000057800::FFFF:FFFF/192 AD/ESI
                   *[BGP/170] 05:12:35, localpref 100, from 10.0.0.1
                      AS path: I, validation-state: unverified
                    > to 10.2.4.2 via ge-0/0/1.24, Push 299792
1:10.0.0.1:0::050000fac8000005dc00::FFFF:FFFF/192 AD/ESI
                   *[BGP/170] 09:33:18, localpref 100, from 10.0.0.1
                      AS path: I, validation-state: unverified
                    > to 10.2.4.2 via ge-0/0/1.24, Push 299792
1:10.0.0.1:0::050000fac8000006a400::FFFF:FFFF/192 AD/ESI
                   *[BGP/170] 05:14:33, localpref 100, from 10.0.0.1
                      AS path: I, validation-state: unverified
                    > to 10.2.4.2 via ge-0/0/1.24, Push 299792
2:10.0.0.1:100::1100::00:05:86:35:e9:f0/304 MAC/IP
                   *[EVPN/170] 08:02:41
                      Indirect
2:10.0.0.1:100::1100::00:05:86:5f:ce:f0/304 MAC/IP
                   *[BGP/170] 09:33:18, localpref 100, from 10.0.0.1
                      AS path: I, validation-state: unverified
                    > to 10.2.4.2 via ge-0/0/1.24, Push 299792
2:10.0.0.1:100::1100::02:30:7b:77:27:c5/304 MAC/IP
                   *[EVPN/170] 00:00:09
                      Indirect
2:10.0.0.1:100::1100::02:70:8a:fc:05:8a/304 MAC/IP
                   *[BGP/170] 05:45:41, localpref 100, from 10.0.0.1
                      AS path: I, validation-state: unverified
                    > to 10.2.4.2 via ge-0/0/1.24, Push 299792
2:10.0.0.1:100::1100::02:79:90:c0:1e:0f/304 MAC/IP
                   *[EVPN/170] 00:02:30
                      Indirect
2:10.0.0.1:100::1400::00:05:86:5f:ce:f0/304 MAC/IP
                   *[BGP/170] 05:12:34, localpref 100, from 10.0.0.1
                      AS path: I, validation-state: unverified
                    > to 10.2.4.2 via ge-0/0/1.24, Push 299792
2:10.0.0.1:100::1400::02:70:8a:fc:05:8a/304 MAC/IP
                   *[BGP/170] 05:12:34, localpref 100, from 10.0.0.1
                      AS path: I, validation-state: unverified
                    > to 10.2.4.2 via ge-0/0/1.24, Push 299792
2:10.0.0.1:100::1500::00:05:86:5f:ce:f0/304 MAC/IP
                   *[BGP/170] 07:54:21, localpref 100, from 10.0.0.1
                      AS path: I, validation-state: unverified
                    > to 10.2.4.2 via ge-0/0/1.24, Push 299792
2:10.0.0.1:100::1500::02:30:7b:77:27:c5/304 MAC/IP
                   *[EVPN/170] 00:02:58
                      Indirect
2:10.0.0.1:100::1500::02:79:90:c0:1e:0f/304 MAC/IP
                   *[EVPN/170] 00:10:01
                      Indirect
2:10.0.0.1:100::1600::00:05:86:35:e9:f0/304 MAC/IP
                   *[EVPN/170] 05:15:10
                      Indirect
2:10.0.0.1:100::1600::02:30:7b:77:27:c5/304 MAC/IP
                   *[EVPN/170] 05:15:09
                      Indirect
2:10.0.0.1:100::1700::00:05:86:35:e9:f0/304 MAC/IP
                   *[EVPN/170] 05:15:10
                      Indirect
2:10.0.0.1:100::1700::00:05:86:5f:ce:f0/304 MAC/IP
                   *[BGP/170] 05:14:32, localpref 100, from 10.0.0.1
                      AS path: I, validation-state: unverified
                    > to 10.2.4.2 via ge-0/0/1.24, Push 299792
2:10.0.0.1:100::1700::02:30:7b:77:27:c5/304 MAC/IP
                   *[EVPN/170] 00:04:55
                      Indirect
2:10.0.0.1:100::1700::02:70:8a:fc:05:8a/304 MAC/IP
                   *[BGP/170] 00:04:54, localpref 100, from 10.0.0.1
                      AS path: I, validation-state: unverified
                    > to 10.2.4.2 via ge-0/0/1.24, Push 299792
2:10.0.0.1:100::1100::00:05:86:35:e9:f0::10.11.12.102/304 MAC/IP
                   *[EVPN/170] 08:02:41
                      Indirect
2:10.0.0.1:100::1100::00:05:86:5f:ce:f0::10.11.12.101/304 MAC/IP
                   *[BGP/170] 08:00:37, localpref 100, from 10.0.0.1
                      AS path: I, validation-state: unverified
                    > to 10.2.4.2 via ge-0/0/1.24, Push 299792
2:10.0.0.1:100::1100::02:30:7b:77:27:c5::10.11.12.2/304 MAC/IP
                   *[EVPN/170] 00:00:09
                      Indirect
2:10.0.0.1:100::1100::02:70:8a:fc:05:8a::10.11.12.1/304 MAC/IP
                   *[BGP/170] 05:45:36, localpref 100, from 10.0.0.1
                      AS path: I, validation-state: unverified
                    > to 10.2.4.2 via ge-0/0/1.24, Push 299792
2:10.0.0.1:100::1100::02:79:90:c0:1e:0f::10.11.12.4/304 MAC/IP
                   *[EVPN/170] 00:02:30
                      Indirect
2:10.0.0.1:100::1400::00:05:86:5f:ce:f0::40.11.12.101/304 MAC/IP
                   *[BGP/170] 01:00:15, localpref 100, from 10.0.0.1
                      AS path: I, validation-state: unverified
                    > to 10.2.4.2 via ge-0/0/1.24, Push 299792
2:10.0.0.1:100::1400::02:70:8a:fc:05:8a::40.11.12.1/304 MAC/IP
                   *[BGP/170] 01:01:12, localpref 100, from 10.0.0.1
                      AS path: I, validation-state: unverified
                    > to 10.2.4.2 via ge-0/0/1.24, Push 299792
2:10.0.0.1:100::1500::00:05:86:5f:ce:f0::50.11.12.101/304 MAC/IP
                   *[BGP/170] 00:22:21, localpref 100, from 10.0.0.1
                      AS path: I, validation-state: unverified
                    > to 10.2.4.2 via ge-0/0/1.24, Push 299792
2:10.0.0.1:100::1600::00:05:86:35:e9:f0::60.11.12.102/304 MAC/IP
                   *[EVPN/170] 05:15:10
                      Indirect
2:10.0.0.1:100::1600::02:30:7b:77:27:c5::60.11.12.2/304 MAC/IP
                   *[EVPN/170] 05:14:30
                      Indirect
2:10.0.0.1:100::1700::00:05:86:35:e9:f0::70.11.12.102/304 MAC/IP
                   *[EVPN/170] 05:15:10
                      Indirect
2:10.0.0.1:100::1700::00:05:86:5f:ce:f0::70.11.12.101/304 MAC/IP
                   *[BGP/170] 05:14:32, localpref 100, from 10.0.0.1
                      AS path: I, validation-state: unverified
                    > to 10.2.4.2 via ge-0/0/1.24, Push 299792
2:10.0.0.8:100::0::02:1c:a7:ef:4d:dc::10.11.12.3/304 MAC/IP
                   *[BGP/170] 05:29:27, localpref 100, from 10.0.0.8
                      AS path: I, validation-state: unverified
                    > to 10.2.4.2 via ge-0/0/1.24
3:10.0.0.1:100::1100::10.0.0.1/248 IM
                   *[BGP/170] 09:33:18, localpref 100, from 10.0.0.1
                      AS path: I, validation-state: unverified
                    > to 10.2.4.2 via ge-0/0/1.24, Push 299792
3:10.0.0.1:100::1100::10.0.0.2/248 IM
                   *[EVPN/170] 08:02:41
                      Indirect
3:10.0.0.1:100::1400::10.0.0.1/248 IM
                   *[BGP/170] 05:12:34, localpref 100, from 10.0.0.1
                      AS path: I, validation-state: unverified
                    > to 10.2.4.2 via ge-0/0/1.24, Push 299792
3:10.0.0.1:100::1500::10.0.0.1/248 IM
                   *[BGP/170] 07:54:20, localpref 100, from 10.0.0.1
                      AS path: I, validation-state: unverified
                    > to 10.2.4.2 via ge-0/0/1.24, Push 299792
3:10.0.0.1:100::1500::10.0.0.2/248 IM
                   *[EVPN/170] 07:54:43
                      Indirect
3:10.0.0.1:100::1600::10.0.0.2/248 IM
                   *[EVPN/170] 05:15:10
                      Indirect
3:10.0.0.1:100::1700::10.0.0.1/248 IM
                   *[BGP/170] 05:14:32, localpref 100, from 10.0.0.1
                      AS path: I, validation-state: unverified
                    > to 10.2.4.2 via ge-0/0/1.24, Push 299792
3:10.0.0.1:100::1700::10.0.0.2/248 IM
                   *[EVPN/170] 05:15:10
                      Indirect
3:10.0.0.8:100::0::10.0.0.8/248 IM
                   *[BGP/170] 05:29:27, localpref 100, from 10.0.0.8
                      AS path: I, validation-state: unverified
                    > to 10.2.4.2 via ge-0/0/1.24

[edit]
admin@vmx02#
```

#### cumulus

```
root@cumulus-1:/home/cumulus# net show bgp evpn route
BGP table version is 0, local router ID is 10.0.0.8
Status codes: s suppressed, d damped, h history, * valid, > best, i - internal
Origin codes: i - IGP, e - EGP, ? - incomplete
EVPN type-2 prefix: [2]:[ESI]:[EthTag]:[MAClen]:[MAC]
EVPN type-3 prefix: [3]:[EthTag]:[IPlen]:[OrigIP]

   Network          Next Hop            Metric LocPrf Weight Path
Route Distinguisher: 10.0.0.1:100
*>i[2]:[0]:[0]:[48]:[00:05:86:35:e9:f0]
                    10.0.0.2                      100      0 i
*>i[2]:[0]:[0]:[48]:[00:05:86:35:e9:f0]:[32]:[10.11.12.102]
                    10.0.0.2                      100      0 i
*>i[2]:[0]:[0]:[48]:[00:05:86:35:e9:f0]:[32]:[60.11.12.102]
                    10.0.0.2                      100      0 i
*>i[2]:[0]:[0]:[48]:[00:05:86:35:e9:f0]:[32]:[70.11.12.102]
                    10.0.0.2                      100      0 i
*>i[2]:[0]:[0]:[48]:[00:05:86:5f:ce:f0]
                    10.0.0.1                      100      0 i
*>i[2]:[0]:[0]:[48]:[00:05:86:5f:ce:f0]:[32]:[10.11.12.101]
                    10.0.0.1                      100      0 i
*>i[2]:[0]:[0]:[48]:[00:05:86:5f:ce:f0]:[32]:[40.11.12.101]
                    10.0.0.1                      100      0 i
*>i[2]:[0]:[0]:[48]:[00:05:86:5f:ce:f0]:[32]:[50.11.12.101]
                    10.0.0.1                      100      0 i
*>i[2]:[0]:[0]:[48]:[00:05:86:5f:ce:f0]:[32]:[70.11.12.101]
                    10.0.0.1                      100      0 i
*>i[2]:[0]:[0]:[48]:[02:30:7b:77:27:c5]
                    10.0.0.2                      100      0 i
*>i[2]:[0]:[0]:[48]:[02:30:7b:77:27:c5]:[32]:[10.11.12.2]
                    10.0.0.2                      100      0 i
*>i[2]:[0]:[0]:[48]:[02:30:7b:77:27:c5]:[32]:[60.11.12.2]
                    10.0.0.2                      100      0 i
*>i[2]:[0]:[0]:[48]:[02:70:8a:fc:05:8a]:[32]:[10.11.12.1]
                    10.0.0.1                      100      0 i
*>i[2]:[0]:[0]:[48]:[02:70:8a:fc:05:8a]:[32]:[40.11.12.1]
                    10.0.0.1                      100      0 i
*>i[2]:[0]:[0]:[48]:[02:79:90:c0:1e:0f]
                    10.0.0.2                      100      0 i
*>i[2]:[0]:[0]:[48]:[02:79:90:c0:1e:0f]:[32]:[10.11.12.4]
                    10.0.0.2                      100      0 i
*>i[3]:[0]:[32]:[10.0.0.1]
                    10.0.0.1                      100      0 i
*>i[3]:[0]:[32]:[10.0.0.2]
                    10.0.0.2                      100      0 i
Route Distinguisher: 10.0.0.8:2
*> [2]:[0]:[0]:[48]:[02:1c:a7:ef:4d:dc]
                    10.0.0.8                           32768 i
*> [2]:[0]:[0]:[48]:[02:1c:a7:ef:4d:dc]:[32]:[50.11.12.3]
                    10.0.0.8                           32768 i
*> [2]:[0]:[0]:[48]:[02:30:7b:77:27:c5]:[32]:[50.11.12.2]
                    10.0.0.8                           32768 i
*> [3]:[0]:[32]:[10.0.0.8]
                    10.0.0.8                           32768 i
Route Distinguisher: 10.0.0.8:100
*> [2]:[0]:[0]:[48]:[02:1c:a7:ef:4d:dc]:[32]:[10.11.12.3]
                    10.0.0.8                           32768 i
*> [3]:[0]:[32]:[10.0.0.8]
                    10.0.0.8                           32768 i

Displayed 24 prefixes (24 paths)
root@cumulus-1:/home/cumulus#
```

#### ce1-x

````
admin@vmx01# run show route logical-system ce1-1

inet.0: 17 destinations, 22 routes (17 active, 0 holddown, 0 hidden)
+ = Active Route, - = Last Active, * = Both

10.1.0.11/32       *[Direct/0] 05:46:20
                    > via lo0.11
10.1.0.21/32       *[OSPF/10] 01:00:03, metric 3
                    > to 40.11.12.101 via ge-0/0/6.400
10.11.12.0/24      *[Direct/0] 05:46:20
                    > via ge-0/0/6.100
10.11.12.1/32      *[Local/0] 05:46:20
                      Local via ge-0/0/6.100
                    [OSPF/150] 01:00:03, metric 0, tag 0
                    > to 40.11.12.101 via ge-0/0/6.400
10.11.12.2/32      *[OSPF/150] 01:00:03, metric 0, tag 0
                    > to 40.11.12.101 via ge-0/0/6.400
10.11.12.4/32      *[OSPF/150] 01:00:03, metric 0, tag 0
                    > to 40.11.12.101 via ge-0/0/6.400
40.11.12.0/24      *[Direct/0] 01:01:41
                    > via ge-0/0/6.400
40.11.12.1/32      *[Local/0] 01:01:41
                      Local via ge-0/0/6.400
                    [OSPF/150] 01:00:03, metric 0, tag 0
                    > to 40.11.12.101 via ge-0/0/6.400
40.11.12.2/32      *[OSPF/150] 01:00:03, metric 0, tag 0
                    > to 40.11.12.101 via ge-0/0/6.400
50.11.12.0/24      *[Direct/0] 05:46:20
                    > via ge-0/0/6.500
                    [OSPF/150] 00:22:49, metric 0, tag 0
                    > to 40.11.12.101 via ge-0/0/6.400
50.11.12.1/32      *[Local/0] 05:46:20
                      Local via ge-0/0/6.500
                    [OSPF/150] 01:00:03, metric 0, tag 0
                    > to 40.11.12.101 via ge-0/0/6.400
51.11.12.2/32      *[OSPF/150] 01:00:03, metric 0, tag 0
                    > to 40.11.12.101 via ge-0/0/6.400
60.11.12.0/24      *[OSPF/10] 01:00:03, metric 3
                    > to 40.11.12.101 via ge-0/0/6.400
60.11.12.2/32      *[OSPF/150] 01:00:03, metric 0, tag 0
                    > to 40.11.12.101 via ge-0/0/6.400
70.11.12.0/24      *[Direct/0] 05:15:01
                    > via ge-0/0/6.700
                    [OSPF/10] 01:00:03, metric 2
                    > to 40.11.12.101 via ge-0/0/6.400
70.11.12.1/32      *[Local/0] 05:15:01
                      Local via ge-0/0/6.700
224.0.0.5/32       *[OSPF/10] 05:46:20, metric 1
                      MultiRecv

inet6.0: 1 destinations, 1 routes (1 active, 0 holddown, 0 hidden)
+ = Active Route, - = Last Active, * = Both

ff02::2/128        *[INET6/0] 05:46:20
                      MultiRecv

[edit]
admin@vmx01# run show route logical-system ce1-2

inet.0: 3 destinations, 3 routes (3 active, 0 holddown, 0 hidden)
+ = Active Route, - = Last Active, * = Both

0.0.0.0/0          *[Static/5] 08:01:06
                    > to 30.11.12.101 via ge-0/0/6.300
30.11.12.0/24      *[Direct/0] 08:01:06
                    > via ge-0/0/6.300
30.11.12.1/32      *[Local/0] 08:01:06
                      Local via ge-0/0/6.300

inet6.0: 1 destinations, 1 routes (1 active, 0 holddown, 0 hidden)
+ = Active Route, - = Last Active, * = Both

ff02::2/128        *[INET6/0] 08:01:06
                      MultiRecv
````

#### ce2-x

````
admin@vmx02# run show route logical-system ce2-1

inet.0: 19 destinations, 22 routes (19 active, 0 holddown, 0 hidden)
+ = Active Route, - = Last Active, * = Both

0.0.0.0/2          *[Direct/0] 02:00:05
                    > via ge-0/0/6.500
10.1.0.11/32       *[OSPF/10] 01:00:36, metric 3
                    > to 60.11.12.102 via ge-0/0/6.600
10.1.0.21/32       *[Direct/0] 07:34:49
                    > via lo0.21
10.11.12.0/24      *[Direct/0] 08:02:52
                    > via ge-0/0/6.100
10.11.12.1/32      *[OSPF/150] 05:15:23, metric 0, tag 0
                    > to 60.11.12.102 via ge-0/0/6.600
10.11.12.2/32      *[Local/0] 08:02:52
                      Local via ge-0/0/6.100
                    [OSPF/150] 05:15:32, metric 0, tag 0
                    > to 60.11.12.102 via ge-0/0/6.600
10.11.12.4/32      *[OSPF/150] 01:39:09, metric 0, tag 0
                    > to 60.11.12.102 via ge-0/0/6.600
40.11.12.0/24      *[OSPF/10] 01:00:36, metric 3
                    > to 60.11.12.102 via ge-0/0/6.600
40.11.12.1/32      *[OSPF/150] 01:02:13, metric 0, tag 0
                    > to 60.11.12.102 via ge-0/0/6.600
40.11.12.2/32      *[OSPF/150] 05:12:55, metric 0, tag 0
                    > to 60.11.12.102 via ge-0/0/6.600
50.11.12.0/24      *[OSPF/150] 05:13:36, metric 0, tag 0
                    > to 60.11.12.102 via ge-0/0/6.600
50.11.12.1/32      *[OSPF/150] 05:15:23, metric 0, tag 0
                    > to 60.11.12.102 via ge-0/0/6.600
50.11.12.2/32      *[Local/0] 02:00:05
                      Local via ge-0/0/6.500
51.11.12.2/32      *[OSPF/150] 05:15:23, metric 0, tag 0
                    > to 60.11.12.102 via ge-0/0/6.600
60.11.12.0/24      *[Direct/0] 05:16:12
                    > via ge-0/0/6.600
60.11.12.2/32      *[Local/0] 05:16:12
                      Local via ge-0/0/6.600
                    [OSPF/150] 05:15:31, metric 0, tag 0
                    > to 60.11.12.102 via ge-0/0/6.600
70.11.12.0/24      *[Direct/0] 05:16:12
                    > via ge-0/0/6.700
                    [OSPF/10] 05:15:32, metric 2
                    > to 60.11.12.102 via ge-0/0/6.600
70.11.12.2/32      *[Local/0] 05:16:12
                      Local via ge-0/0/6.700
224.0.0.5/32       *[OSPF/10] 07:34:49, metric 1
                      MultiRecv

inet6.0: 1 destinations, 1 routes (1 active, 0 holddown, 0 hidden)
+ = Active Route, - = Last Active, * = Both

ff02::2/128        *[INET6/0] 08:02:52
                      MultiRecv

[edit]
admin@vmx02# run show route logical-system ce2-2

inet.0: 3 destinations, 3 routes (3 active, 0 holddown, 0 hidden)
+ = Active Route, - = Last Active, * = Both

0.0.0.0/0          *[Static/5] 1d 00:18:55
                    > to 31.11.12.102 via ge-0/0/6.310
31.11.12.0/24      *[Direct/0] 1d 00:27:34
                    > via ge-0/0/6.310
31.11.12.2/32      *[Local/0] 1d 00:27:34
                      Local via ge-0/0/6.310

inet6.0: 1 destinations, 1 routes (1 active, 0 holddown, 0 hidden)
+ = Active Route, - = Last Active, * = Both

ff02::2/128        *[INET6/0] 3d 00:08:28
                      MultiRecv

[edit]
admin@vmx02#
````


#### ce3

````
root@u1:/home/ubuntu# ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 02:df:82:68:db:af brd ff:ff:ff:ff:ff:ff
    inet 100.64.1.23/24 brd 100.64.1.255 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::df:82ff:fe68:dbaf/64 scope link
       valid_lft forever preferred_lft forever
3: eth1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 02:1c:a7:ef:4d:dc brd ff:ff:ff:ff:ff:ff
    inet6 fe80::1c:a7ff:feef:4ddc/64 scope link
       valid_lft forever preferred_lft forever
4: eth2: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default qlen 1000
    link/ether 02:96:c0:7b:f8:8f brd ff:ff:ff:ff:ff:ff
5: eth1.100@eth1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
    link/ether 02:1c:a7:ef:4d:dc brd ff:ff:ff:ff:ff:ff
    inet 10.11.12.3/24 brd 10.11.12.255 scope global eth1.100
       valid_lft forever preferred_lft forever
    inet6 fe80::1c:a7ff:feef:4ddc/64 scope link
       valid_lft forever preferred_lft forever
6: eth1.500@eth1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
    link/ether 02:1c:a7:ef:4d:dc brd ff:ff:ff:ff:ff:ff
    inet 50.11.12.3/24 brd 50.11.12.255 scope global eth1.500
       valid_lft forever preferred_lft forever
    inet6 fe80::1c:a7ff:feef:4ddc/64 scope link
       valid_lft forever preferred_lft forever
root@u1:/home/ubuntu# ip r
default via 100.64.1.1 dev eth0
10.11.12.0/24 dev eth1.100  proto kernel  scope link  src 10.11.12.3
40.11.12.0/24 via 10.11.12.101 dev eth1.100
50.11.12.0/24 dev eth1.500  proto kernel  scope link  src 50.11.12.3
60.11.12.0/24 via 10.11.12.101 dev eth1.100
100.64.1.0/24 dev eth0  proto kernel  scope link  src 100.64.1.23
````

#### ce4

````
root@u2:/home/ubuntu# ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 02:40:60:13:50:2a brd ff:ff:ff:ff:ff:ff
    inet 100.64.1.22/24 brd 100.64.1.255 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::40:60ff:fe13:502a/64 scope link
       valid_lft forever preferred_lft forever
3: eth1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 02:79:90:c0:1e:0f brd ff:ff:ff:ff:ff:ff
    inet6 fe80::79:90ff:fec0:1e0f/64 scope link
       valid_lft forever preferred_lft forever
4: eth1.500@eth1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
    link/ether 02:79:90:c0:1e:0f brd ff:ff:ff:ff:ff:ff
    inet 50.11.12.4/24 brd 50.11.12.255 scope global eth1.500
       valid_lft forever preferred_lft forever
    inet6 fe80::79:90ff:fec0:1e0f/64 scope link
       valid_lft forever preferred_lft forever
5: eth1.100@eth1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
    link/ether 02:79:90:c0:1e:0f brd ff:ff:ff:ff:ff:ff
    inet 10.11.12.4/24 brd 10.11.12.255 scope global eth1.100
       valid_lft forever preferred_lft forever
    inet6 fe80::79:90ff:fec0:1e0f/64 scope link
       valid_lft forever preferred_lft forever
root@u2:/home/ubuntu#
root@u2:/home/ubuntu#
root@u2:/home/ubuntu#
root@u2:/home/ubuntu# ip r
default via 100.64.1.1 dev eth0
10.11.12.0/24 dev eth1.100  proto kernel  scope link  src 10.11.12.4
40.11.12.0/24 via 10.11.12.101 dev eth1.100
50.11.12.0/24 dev eth1.500  proto kernel  scope link  src 50.11.12.4
60.11.12.0/24 via 10.11.12.101 dev eth1.100
100.64.1.0/24 dev eth0  proto kernel  scope link  src 100.64.1.22
````
