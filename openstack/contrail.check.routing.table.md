# Checking Contrail vrouter routing table

* Find vxlan ID from Contrail web UI
    * find your virtual network
    * check the vxlan attribute
    * for example, the vxlan ID is 38

* check vxlan table to find the nexthop ID
    
    ```
    root@brg-ct1-compute2:/opt/contrail/utils# vxlan --get 38
    VXLAN Table

    VNID    NextHop
    ----------------
        38    547
    ```

* the command above tell us that vxlan 38 has next-hop ID = 547

* check next hop table to find the vrf associated with this virtual network

    ```
    root@brg-ct1-compute2:/opt/contrail/utils# nh --get 547
    Id:547        Type:Vrf_Translate  Fmly: AF_INET  Flags:Valid, Vxlan,   Rid:0  Ref_cnt:2 Vrf:24
                Vrf:24
    ```

* the command above tell us that vxlan 38 with nexthop 547 belongs to vrf 24

* find the linux tap interface associated with this virtual network, useful if we want to do tcpdump on a specific vnet

    ```
    root@brg-ct1-compute2:/opt/contrail/utils# vif --list | grep -b2 Vrf:24
    17191-vif0/72     OS: tapfd0eb363-b0
    17222-            Type:Virtual HWaddr:00:00:5e:00:01:00 IPaddr:0
    17281:            Vrf:24 Flags:L2 MTU:9160 Ref:4
    17324-            RX packets:169  bytes:26160 errors:0
    17373-            TX packets:131  bytes:15370 errors:0
    ```

* the command above tell us that vrf24 has interface tapfd0eb363-b0
    * if we want to sniff the traffic on this vrf in this compute node, we can simply do tcpdump on tapfd0eb363-b0 interface

* check the routing table
    * the example below is taken from virtual network with forwarding mode = layer 2, in this case --family bridge must be used
    
        ```
        root@brg-ct1-compute2:/opt/contrail/utils# rt --dump 24
        Vrouter inet4 routing table 0/24/unicast
        Flags: L=Label Valid, P=Proxy ARP, T=Trap ARP, F=Flood ARP

        Destination	      PPL        Flags        Label         Nexthop    Stitched MAC(Index)


        root@brg-ct1-compute2:/opt/contrail/utils# rt --dump 24 --family bridge
        Kernel L2 Bridge table 0/24

        Flags: L=Label Valid, Df=DHCP flood

        Index     DestMac                          Flags       Label/VNID      Nexthop
        19128     ff:ff:ff:ff:ff:ff                 LDf               38        605
        32880     c:c4:7a:57:e:40                    Df                -          3
        203288     2:fd:e:b3:63:b0                    Df                -        587
        228256     2:4a:ec:30:b3:37                  LDf               66        121
        250296     0:0:5e:0:1:0                       Df                -          3
        ```

    * what we can learn from result above
        * to reach destination with mac = 2:fd:e:b3:63:b0, use next hop 587
        * to reach destination with mac = 2:4a:ec:30:b3:37, use next hop 121 with mpls label 66 


* check the actual outgoing next-hop

    ```
    root@brg-ct1-compute2:/opt/contrail/utils# nh --get 587
    Id:587        Type:Encap     Fmly:AF_BRIDGE  Flags:Valid,   Rid:0  Ref_cnt:4 Vrf:24
                EncapFmly:0806 Oif:72 Len:14 Data:02 fd 0e b3 63 b0 00 00 5e 00 01 00 08 00

    root@brg-ct1-compute2:/opt/contrail/utils# nh --get 121
    Id:121        Type:Tunnel    Fmly: AF_INET  Flags:Valid, MPLSoGRE,   Rid:0  Ref_cnt:141 Vrf:0
                Oif:0 Len:14 Flags Valid, MPLSoGRE,  Data:0c c4 7a 57 14 f0 0c c4 7a 57 0e 40 08 00
                Vrf:0  Sip:172.25.155.35  Dip:172.25.155.34
    ```

* what we can learn from result above
    * to reach destination with mac = 2:fd:e:b3:63:b0, use next hop 587
        * this next-hop is local interface with interface ID = 72
        * see the vif --list above

    * to reach destination with mac = 2:4a:ec:30:b3:37, use next hop 121 with mpls label 66 
        * the destination is located on different compute node which is 172.25.155.34
        * to send the packet to the destination on the remote compute node, use MPLS over GRE with mpls label = 66

* NOTE:
    * all the collected information above are local per compute node. If you have multiple VM connected to the same virtual network but hosted on different compute nodes, each compute node will have its own local vif, local next-hop id, local vrf id


