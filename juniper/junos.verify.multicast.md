The purpose of this post is to provide overview how to verify multicast traffic in Juniper if we don't have the real multicast source and receiver.

Before i start, i want to remind you that it is easy to verify the multicast traffic in Cisco router, in general we can do the following:
* configure the last hop router (the router that one hop away from the multicast receiver host ) to statically join the desired group by using "ip igmp join-group group-address" command
* do ping from first hop router (the router that one hop away from the multicast source host)
* if the last hop router(s) are answering the ping request, then the multicast packet will be successfully transmitted from source to the receiver.


The case will be slightly different for Juniper.

It is a well-known that we can monitor traffic passing over Juniper interface except the packet destined to its local interface. This rule is also applied for multicast traffic with these additional condition:
* by default, the last hop router will only join the group as requested by multicast receiver host behind it bu the last hop router will not listen into it
* the multicast packet will just transiting into its interface and forwarding-engine, and not going to the routing-engine.
* In the case when the multicast receiver host is not available, last hop router can be configured to statically join the desired group by using "set protocols igmp interface XXX static group YYY" command. But again, it is just joining, not listening.
* Actually we can cheat Junos to make the last hop router listen to a multicast group by using "set protocol sap listen xxxx" command but this doesn't work for logical router. It seems if we enable sap on a logical router, actually it is enabled for the whole chassis.

Based on the behavior above, it is clear why we can't use Cisco's way to verify Juniper multicast traffic. 

Here are the diagram, step and example to verify juniper multicast traffic:


notes: J1 is the first hop router, J7 us the last hop router, J5 is the RP

do ping from first hop router with:
* TTL long enough to reach the last hop router (by default, junos set ttl for ping packet towards multicast address to 0)
* enable bypass-routing
* repeat the packet long enough for you to do verification
* use big packet size as long as it can produce > 1 kbps to be logged in the statistic (not sure the exact lowest limit, in cisco it is 4kbps)

example:
```
erenari@SRLAB1> ping 235.1.0.7 logical-router j1 bypass-routing count 1000000000 ttl 10 size 60000   
PING 235.1.0.7 (235.1.0.7): 60000 data bytes
Don't expect any return packet, it is normal 
On the last hop router, configure the static igmp
example: set protocols igmp interface fe-1/3/0.777 static group 235.1.0.7
check the multicast packet on last hop router, if everything works fine, we should get the result like the example below:

example 1: there are packets received for 235.1.0.7 with 11.0.12.1 as the source

erenari@SRLAB1> show multicast usage logical-router j7 detail    
Group           Sources Packets              Bytes
235.1.0.7       1       19117                14544260            
    Source: 11.0.12.1       /32 Packets: 19117 Bytes: 14544260

Prefix          /len Groups Packets              Bytes
11.0.12.1       /32  1      19117                14544260            
    Group: 235.1.0.7       Packets: 19117 Bytes: 14544260
```


example 2: detailed multicast route info with bandwidth statistic
```
erenari@SRLAB1> show multicast route detail logical-router j7    
Family: INET

Group: 235.1.0.7
    Source: 11.0.12.1/32 
    Upstream interface: fe-1/3/0.947
    Downstream interface list: 
        fe-1/3/0.777
    Session description: Unknown   
    Statistics: 61 kBps, 80 pps, 22195 packets
    Next-hop ID: 262267
    Upstream protocol: PIM

Family: INET6

erenari@SRLAB1> 
```




In addition to the above command, if you use PIM, you can always verify the PIM status. I provide some examples for PIM verification below:

example 3: Check RP status
```
erenari@SRLAB1> show pim rps logical-router j1   ----> j1 is the first hop router                                       
Instance: PIM.master
Address family INET
RP address               Type        Holdtime Timeout Groups Group prefixes
11.0.9.99                bootstrap        150     124      1 224.0.0.0/4

Address family INET6

erenari@SRLAB1> show pim rps logical-router j7 detail  ----> j7 is the first hop router
Instance: PIM.master
Address family INET

RP: 11.0.9.99
Learned from 11.0.47.4 via: bootstrap
Time Active: 2w1d 12:02:10
Holdtime: 150 with 112 remaining
Group Ranges:
        224.0.0.0/4, 112s remaining
Active groups using RP:
        235.1.0.7
        224.2.127.254

        total 2 groups active

Address family INET6
```



example 4: check bootstrap
```
erenari@SRLAB1> show pim bootstrap logical-router j7      
Instance: PIM.master

BSR                     Pri Local address           Pri State      Timeout
11.0.3.4                 20 11.0.9.7                  0 InEligible     128
None                      0 2400:0:1::7               0 InEligible       0
```


example 5: check PIM join status on the RP site 
```
erenari@SRLAB1> show pim join logical-router j5 detail  
Instance: PIM.master Family: INET

Group: 224.2.127.254
    Source: *
    RP: 11.0.9.99
    Flags: sparse,rptree,wildcard
    Upstream interface: Local              

Group: 235.1.0.7
    Source: *
    RP: 11.0.9.99
    Flags: sparse,rptree,wildcard
    Upstream interface: Local              

Group: 235.1.0.7
    Source: 11.0.12.1
    Flags: sparse
    Upstream interface: fe-1/3/0.945        

Instance: PIM.master Family: INET6
```
