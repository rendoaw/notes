# Example of Remote Trigger Blackhole (RTBH), destination-based and source-based

## Quick overview

### Destination based RTBH
* the network that being attacked send the __attacked/victim__ IP to the upstream provider, upstream provider will block the traffic to the __attacked/victim__ IP on all entry point.
* Sample scenario:
    * customer C detect that one of their IP/prefix, let say, a.b.c.d is being attacked by attacker A.
    * by using BGP, customer C advertise a.b.c.d prefix with specific community to its upstream provider P.
    * provider P PE router that facing customer C (let say PE1) receives this prefix and re-advertise to all router in provider P network, still using BGP
    * all BGP speaker in provider P network receive this special prefix and then set the next-hop for this prefix to discard.
        * alrenatively, if provider P has DDoS anaylyzer, they can redirect all traffic going to this prefix to the analyzer.

### Source based RTBH
* the network that being attacked send the __attacker__ IP to the upstream provider, upstream provider will block the traffic __from__ attacker IP on all entry point.
* Sample scenario:
    * customer C detect that one of their IP/prefix, let say, a.b.c.d is being attacked by attacker A.
    * customer C know the attacker IP is w.x.y.z
    * by using BGP, customer C advertise w.x.y.z prefix with specific community to its upstream provider P.
    * provider P PE router that facing customer C (let say PE1) receives this prefix and re-advertise to all router in provider P network, still using BGP
    * all BGP speaker in provider P network receive this special prefix and then set the next-hop for this prefix to discard.
    * all BGP speaker in provider P also implement unicast RPF check on its external AS facing interface
    * since the next-hop is set to discard, any packet from w.x.y.z will fail RPF check and will be blocked


## Configuration

### Topology

```
Customer ----- PE11 ----- { MPLS network } ----- PE17 ----- internet

```

### Destination based RTBH

* customer as the victim
* victim IP is 76.6.255.111
* advertise victim IP to provider with agreed community

    ```
    rwibawa@DC6# show policy-options policy-statement dc6-rtbh 
    term rtbh-destination {
        from {
            route-filter 76.6.255.111/32 exact;
        }
        then {
            community set bh;
            accept;
        }
    }
    
    rwibawa@DC6# show policy-options community bh    
    members 23456:666;    
    ```

* Provider PE1 router received the victim IP

    ```
    rwibawa@vmx-13-11# run show route receive-protocol bgp 67.176.0.162 table inet.0 detail 76.6.255.111/32 
    
    inet.0: 22191 destinations, 22194 routes (22191 active, 0 holddown, 0 hidden)
    * 76.6.255.111/32 (1 entry, 1 announced)
         Accepted
         Nexthop: 67.176.0.162
         AS path: 766 I
         Communities: 23456:666
    ```

* Provider PE1 advertises the victim IP to any other BGP speaker, and optionally tag it with no-export to make sure this special prefix stay within AS.

    ```
    rwibawa@vmx-13-11# run show route advertising-protocol bgp 67.176.255.103 76.6.255.111/32 extensive                  
    
    inet.0: 22191 destinations, 22194 routes (22191 active, 0 holddown, 0 hidden)
    * 76.6.255.111/32 (1 entry, 1 announced)
     BGP group IBGP type Internal
         Nexthop: Self
         Flags: Nexthop Change
         Localpref: 100
         AS path: [16689.7041] 766 I
         Communities: 23456:666 no-export
    
    
    rwibawa@vmx-13-11# show protocols bgp group as766 import 
    import [ as766-import wr-reject-defaultroute wr-reject-rfc1918 wr-accept-and-tag-peer ];
    
    
    rwibawa@vmx-13-11# show policy-options policy-statement wr-accept-and-tag-peer 
    term 1 {
        from community wr-rtbh;
        then {
            community add no-export;
            accept;
        }
    }
    term 2 {
        then {
            community add wr-peer;
            accept;
        }
    }
    
    rwibawa@vmx-13-11# show policy-options community no-export     
    members no-export;

    rwibawa@vmx-13-11# show policy-options community wr-rtbh      
    members 23456:666;
    ```
    
* all other BGP speaker set next-hop discard for victim IP destination

    ```
    rwibawa@vmx-13-17# run show route 76.6.255.111/32 detail 
    
    inet.0: 22188 destinations, 22201 routes (22188 active, 0 holddown, 0 hidden)
    76.6.255.111/32 (1 entry, 1 announced)
            *BGP    Preference: 170/-101
                    Next hop type: Discard  ---------------------> set NH = discard
                    Address: 0x94120c4
                    Next-hop reference count: 16
                    State: <Active Int Ext>
                    Local AS: 1093737345 Peer AS: 1093737345
                    Age: 5:16 
                    Validation State: unverified 
                    Task: BGP_1093737345.67.176.255.103+179
                    Announcement bits (2): 0-KRT 13-Resolve tree 4 
                    AS path: 766 I (Originator)
                    Cluster list:  67.176.255.103
                    Originator ID: 67.176.255.1
                    Communities: 23456:666 no-export
                    Accepted
                    Localpref: 100
                    Router ID: 67.176.255.103
    
    rwibawa@vmx-13-17# show protocols bgp group IBGP import 
    import wr-rtbh-set-nh-discard;
    
    [edit]
    rwibawa@vmx-13-17# show policy-options policy-statement wr-rtbh-set-nh-discard 
    term 1 {
        from community wr-rtbh;
        then {
            next-hop discard;
            next policy;
        }
    }
    
    [edit]
    rwibawa@vmx-13-17# show policy-options community wr-rtbh                          
    members 23456:666;
    ```
        
* if PE1 has any other external network facing interface, PE1 also need to set next-hop discard for the victim IP route as well.

* Now, since this ise a destniation based routing blackhole, any packet with destination = victim IP will be discard at any provider entry point. It also include any legitimate traffic from any other source.

* OK, what if customer just want to block the attacker IP? Then we need to use source-based RTBH in the next section.


### Source based RTBH

* same as above, customer victim IP is 76.6.255.111
* customer find out the attacker/DDoS source IP is 71.23.48.1
* customer create a dummy static route and advertise the attacker IP with agreed community

    ```
    rwibawa@DC6# show policy-options policy-statement dc6-rtbh    
    term rtbh-source {
        from {
            route-filter 71.23.48.1/32 exact;
        }
        then {
            community set bh;
            accept;
        }
    }
    
    rwibawa@DC6# show policy-options community bh   
    members 23456:666;
    ```

* Provider PE1 router received the victim IP

    ```
    rwibawa@vmx-13-11# run show route receive-protocol bgp 67.176.0.162 table inet.0 detail 71.23.48.1/32       
    
    inet.0: 22191 destinations, 22194 routes (22191 active, 0 holddown, 0 hidden)
    * 71.23.48.1/32 (1 entry, 1 announced)
         Accepted
         Nexthop: 67.176.0.162
         AS path: 766 I
         Communities: 23456:666
    ```

* Similar as destination based RTBH, Provider PE1 advertises the victim IP to any other BGP speaker, and optionally tag it with no-export to make sure this special prefix stay within AS.

* similar as destination based RTBH, all other BGP speakers set next-hop discard for victim IP destination

    ```
    rwibawa@vmx-13-17# run show route 71.23.48.1/32 detail      
    
    inet.0: 22188 destinations, 22201 routes (22188 active, 0 holddown, 0 hidden)
    71.23.48.1/32 (1 entry, 1 announced)
            *BGP    Preference: 170/-101
                    Next hop type: Discard  -----------------> set NH = discard
                    Address: 0x94120c4
                    Next-hop reference count: 16
                    State: <Active Int Ext>
                    Local AS: 1093737345 Peer AS: 1093737345
                    Age: 15:39 
                    Validation State: unverified 
                    Task: BGP_1093737345.67.176.255.103+179
                    Announcement bits (2): 0-KRT 13-Resolve tree 4 
                    AS path: 766 I (Originator)
                    Cluster list:  67.176.255.103
                    Originator ID: 67.176.255.1
                    Communities: 23456:666 no-export
                    Accepted
                    Localpref: 100
                    Router ID: 67.176.255.103
    ```

* Unicast RPF is enabled on external AS facing interface

    ```
    rwibawa@vmx-13-17# show interfaces ge-0/0/0.16 
    vlan-id 16;
    family inet {
        rpf-check {
            mode loose;
        }
        address 67.176.0.49/30;
    }
    ```
    
* enable rpf loose discard 
    
    * this feature is supported since 12.1
    * reference: http://www.juniper.net/techpubs/en_US/junos12.1/topics/usage-guidelines/interfaces-configuring-unicast-rpf.html
    
        ```
        rwibawa@vmx-13-17# show forwarding-options 
        rpf-loose-mode-discard {
            family {
                inet;
            }
        }
        ```

* That's it. In theory, if the packet coming from interface with uRPF check enabled and there is a route to the source IP with next-hop = discard, and rpf discard is enabled, JunOS will discard the packet.

* Wait, is there any way to verify this? Yes. By using firewall filter. Let's create the filter policy and modify the interface rpf config little bit.

    ```
    rwibawa@vmx-13-17# show firewall filter count-rpf 
    term 1 {
        then {
            count rpf;
            log;
            syslog;
            reject;
        }
    }
    
    
    rwibawa@vmx-13-17# show interfaces ge-0/0/0.16 
    vlan-id 16;
    family inet {
        rpf-check {
            fail-filter count-rpf;  ----> add this
            mode loose;
        }
        address 67.176.0.49/30;
    }
    ```

* let's check the log/counter

    ```
    rwibawa@vmx-13-17# run show firewall counter filter count-rpf rpf                 
    
    Filter: count-rpf                                              
    Counters:
    Name                                                Bytes              Packets
    rpf                                                108192                 1288
    
    
    rwibawa@vmx-13-17# run show firewall log interface ge-0/0/0.16    
    Log :
    Time      Filter    Action Interface     Protocol        Src Addr                         Dest Addr
    00:23:50  pfe       R      ge-0/0/0.16   ICMP            71.23.48.1                       76.6.255.11
    00:23:49  pfe       R      ge-0/0/0.16   ICMP            71.23.48.1                       76.6.255.11
    00:23:48  pfe       R      ge-0/0/0.16   ICMP            71.23.48.1                       76.6.255.11
    ```

* if you still need to make sure, as usual, you can tcpdump/sniff the traffic on the victim side.


## Destination vs Source based RTBH

* Destination based RTBH
    * based on victim IP
    * all packet destinated to victim IP will be blocked/discarded.
    * victim IP will be isolated completely from external network.
    * it is very common implementation.

* Source based RTBH
    * based on attacker IP
    * all packet from attacker IP to any destination will be blocked/discarded.
    * should be only applied to very trusted customer otherwise many thing can go wrong, e.g:
        * both customer A and B are using P as their provider
        * customer A is very paranoid. 
        * Person X want to connect to customer B server IP, but trying to connect to A by mistake (typo on IP address)
        * customer A assumes this is an attack
        * by using source-based RTBH, customer A ask the provider P to block person X source IP.
        * Person P never able to connect to customer B anymore
        
