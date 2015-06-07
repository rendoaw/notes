One of my job description in my current company is to do IP network simulation and creating a guidance about how the protocol works in multi vendor environment.

I was looking for how is the behavior of IPv6 dual topology for Cisco and Juniper, and suddenly i found a thread from Nanog mailing list which said Junos has been supporting multi address family for OSPFv3 since version 9.5. Click here for more detail.

Multiple address-family or we called it as Realm, is based on the following draft
draft-ietf-ospf-af-alt-06.txt.

In short, multiple address-family on OSPFv3 means we can just use OSPFv3 for both IPv4 and IPv6. Please note that OSPFv3 IPv4 address-family is not compatible with normal OSPF operation (at least with we have now, maybe in the future there is another extension to support it), so don't expect that you can create OSPF neighborship for IPv4 subnet between OSPF router and OSPFv3 router.

Taken from the RFC draft itself:
   OSPFv3 has been defined to support the base IPv6 unicast Address
   Family (AF).  There is a requirement to advertise other AFs in OSPFv3
   including multicast IPv6, unicast IPv4, and multicast IPv4.  This
   document supports these other AFs in OSPFv3 by mapping each to a
   separate Instance ID and OSPFv3 instance.


So here is my quick experiment, i just wondering how it works, maybe in the future i will try to do some tweaking on this feature.


My Topology is simple, 3 router connected each other:
```
jpe6 --- ce8 ---- jpe7
 |                |
 ------------------
```

Configurations from each router:
```
[edit logical-systems]
rendo@olive# show jpe6 protocols ospf3 
realm ipv4-unicast {
    area 0.0.0.0 {
        interface all;
    }
}
export bgpv6;
area 0.0.2.154 {
    interface em1.968;
    interface lo0.96;
}


[edit logical-systems]
rendo@olive# show jpe7 protocols ospf3   
realm ipv4-unicast {
    area 0.0.0.0 {
        interface all;
    }
}
export bgpv6;
area 0.0.2.154 {
    interface lo0.97;
    interface em1.978;
}


[edit logical-systems]
rendo@olive# show ce8 protocols ospf3    
realm ipv4-unicast {
    area 0.0.0.0 {
        interface all;
    }
}
area 0.0.2.154 {
    interface em2.968;
    interface em2.978;
    interface lo0.98;
}

```


Test 1: jpe6, jpe7, ce8 run both normal ospf3 and ospf3 realm ipv4-unicast
```
[edit logical-systems]
rendo@olive# run show ospf3 neighbor logical-system ce8 detail      
ID               Interface              State     Pri   Dead
11.0.9.6         em2.968                Full      128     36
  Neighbor-address fe80::a00:2703:c836:1a84
  Area 0.0.2.154, opt 0x13, OSPF3-Intf-Index 1
  DR-ID 13.0.1.8, BDR-ID 11.0.9.6
  Up 00:01:09, adjacent 00:00:21
11.0.9.7         em2.978                Full      128     35
  Neighbor-address fe80::a00:2703:d236:1a84
  Area 0.0.2.154, opt 0x13, OSPF3-Intf-Index 2
  DR-ID 13.0.1.8, BDR-ID 11.0.9.7
  Up 00:01:10, adjacent 00:00:30

[edit logical-systems]
rendo@olive# run show ospf3 neighbor logical-system ce8 detail realm ipv4-unicast
ID               Interface              State     Pri   Dead
11.0.9.6         em2.968                Full      128     32
  Neighbor-address fe80::a00:2703:c836:1a84
  Area 0.0.0.0, opt 0x112, OSPF3-Intf-Index 9
  DR-ID 13.0.1.8, BDR-ID 11.0.9.6
  Up 00:01:15, adjacent 00:00:30
11.0.9.7         em2.978                Full      128     32
  Neighbor-address fe80::a00:2703:d236:1a84
  Area 0.0.0.0, opt 0x112, OSPF3-Intf-Index 8
  DR-ID 13.0.1.8, BDR-ID 11.0.9.7
  Up 00:01:15, adjacent 00:00:25
```


Test 2: IPv6 disabled on JPE6 interface towards CE8.
jpe6 is not listed as ce8 neighbor for any family
```
[edit logical-systems]
rendo@olive# run show ospf3 neighbor logical-system ce8 realm ipv4-unicast   
ID               Interface              State     Pri   Dead
11.0.9.7         em2.978                Full      128     31
  Neighbor-address fe80::a00:2703:d236:1a84

[edit logical-systems]
rendo@olive# run show ospf3 neighbor logical-system ce8                      
ID               Interface              State     Pri   Dead
11.0.9.7         em2.978                Full      128     36
  Neighbor-address fe80::a00:2703:d236:1a84

[edit logical-systems]
rendo@olive#
```


Test 3: jpe6 ipv6 interface is activated but ospf3 area for ipv6 is disabled.
jpe6 is listed as ce8 neighbor only for ipv4-unicast family
```
[edit logical-systems]
rendo@olive# run show ospf3 neighbor logical-system ce8                      
ID               Interface              State     Pri   Dead
11.0.9.7         em2.978                Full      128     35
  Neighbor-address fe80::a00:2703:d236:1a84

[edit logical-systems]
rendo@olive# run show ospf3 neighbor logical-system ce8 realm ipv4-unicast   
ID               Interface              State     Pri   Dead
11.0.9.6         em2.968                Full      128     33
  Neighbor-address fe80::a00:2703:c836:1a84
11.0.9.7         em2.978                Full      128     33
  Neighbor-address fe80::a00:2703:d236:1a84

[edit logical-systems]
rendo@olive#
```

