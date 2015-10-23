
# Playing with JunOS CoS classifier and rewrite


## Preparation

### Router
* MX240
* JunOS 14.2

### Base CoS Config

rwibawa@skynet_29# show class-of-service
classifiers {
    dscp rw-dscp {
        import default;
        forwarding-class rw_be {
            loss-priority low code-points 111000;
            loss-priority high code-points 110000;
        }
    }
}
forwarding-classes {
    class rw_be queue-num 0;
    class rw_ef queue-num 1;
    class rw_af queue-num 2;
    class rw_nc queue-num 3;
}
interfaces {
    ge-1/0/1 {
        unit 0 {
            classifiers {
                dscp rw-dscp;
            }
        }
    }
}


### Simple firewall filter to count transit traffic on next-hop router R2 and next-next-hop R3

```
firewall {
    family mpls {
        filter log_traffic_mpls {
            term 1 {
                from {
                    exp 7;
                }
                then {
                    count exp_ef;
                    accept;
                }
            }
            term 2 {
                from {
                    exp 0;
                }
                then {
                    count exp_be;
                    accept;
                }
            }
            term default {
                then {
                    count exp_other;
                    accept;
                }
            }
        }
    }
    filter log_traffic {
        term 1 {
            from {
                dscp ef;
                protocol icmp;
            }
            then {
                count ef;
                accept;
            }
        }
        term 2 {
            from {
                dscp be;
                protocol icmp;
            }
            then {
                count be;
                accept;
            }
        }
        term 3 {
            from {
                dscp cs7;
                protocol icmp;
            }
            then {
                count cs7;
                accept;
            }
        }
        term default {
            then {
                count other;
                accept;
            }
        }
    }
}
```


### Ping Command

```
rwibawa@ce01# run ping 94.0.0.2 tos 224 count 3
```


## Test scenario

### Scenario 1: custom dscp classifier, no mpls

* see base config section above
* dscp classfier rw-dscp @ R1 (ingress PE) to map dscp 111000 (56) and 110000 (48) to forwarding-class be
* apply rw-dscp at R1 CE-facing interface
* no rewrite everywhere
* end to end traffic is using pure IP, no MPLS
* run the ping command above
* Packet received at remote CE

    ```
    17:54:38.858950  In IP (tos 0x0, ttl  60, id 57623, offset 0, flags [none], proto: ICMP (1), length: 84) 94.0.0.1 > 94.0.0.2: ICMP echo request, id 10225, seq 0, length 64

    ```

* counter at R2

    ```
    rwibawa@skynet_29_02> show firewall counter filter log_traffic be

    Filter: log_traffic
    Counters:
    Name                                                Bytes              Packets
    be                                                    588                    7
    ```

* result
    * At R1, rw-dscp classifier put ping traffic to BE forwarding class
    * when it goes out, there is no rewrite, R1 forward the packet with ToS header intact
        * firewall filter in R2 confirms it
        * sniffed traffic in remote CE confirm it



### Scenario 2: custom dscp classifier, with MPLS in the backbone

* exactly the same as scenario 1, except:
    * use MPLS in the backbone, between R1 upto R4
* run the ping command above
* Packet received at remote CE

    ```
    23:31:10.611610  In IP (tos 0xe0, ttl  60, id 35830, offset 0, flags [none], proto: ICMP (1), length: 84) 94.0.0.1 > 94.0.0.2: ICMP echo request, id 29180, seq 0, length 64
    ```

* counter at R2

    ```
    rwibawa@skynet_29_02> show firewall counter filter log_traffic_mpls exp_ef

    Filter: log_traffic_mpls
    Counters:
    Name                                                Bytes              Packets
    exp_ef                                                264                    3
    ```

* result
    * At R1, rw-dscp classifier put ping traffic to BE forwarding class
    * when it goes out, there is no rewrite, R1 forward the packet with ToS header intact
        * firewall filter in R2 confirms it
    * on R2 (R1 next hop router), the packet seemms still using EF exp bit
        * sniffed traffic in remote CE confirm it
        * this is strange, because, according the following, if exp bit rewrite rule is actually applied automatically, then the EXP bit on R2 should be BE, not EF.

            ```
            https://www.juniper.net/documentation/en_US/junos12.3/topics/usage-guidelines/cos-applying-default-rewrite-rules.html

            By default, rewrite rules are not usually applied to interfaces. The exceptions are MPLS interfaces: all MPLS-enabled interfaces use the default EXP rewrite rule, even if not configured.
            ```
    
        * Let's come back to this at the end of this post


### Scenario 3: custom dscp classifier, default dscp rewrite, with MPLS in the backbone

* exactly the same as scenario 2, except:
    * use dscp default rewriter on R1 outgoing interface (backbone facing)

        ```
        rwibawa@skynet_29# show class-of-service interfaces ge-1/0/2
        unit 0 {
            rewrite-rules {
                dscp default;
            }
        }
        ```

* similar as scenario 2, MPLS is used in the backbone
* run the ping command above
* Packet received at remote CE

    ```
    23:34:14.342180  In IP (tos 0xe0, ttl  60, id 41901, offset 0, flags [none], proto: ICMP (1), length: 84) 94.0.0.1 > 94.0.0.2: ICMP echo request, id 51708, seq 0, length 64
    ```

* counter at R2

    ```
    rwibawa@skynet_29_02> show firewall counter filter log_traffic_mpls exp_ef

    Filter: log_traffic_mpls
    Counters:
    Name                                                Bytes              Packets
    exp_ef                                                264                    3
    ```

* result
    * At R1, rw-dscp classifier put ping traffic to BE forwarding class
    * when it goes out, there is dscp default rewrite, R1 forward the packet with dscp, supposedly to be 0
    * on remote CE, the packet is received with original ToS header
        * firewall filter in R2 confirms it
    * on R2 (R1 next hop router), the packet seemms still using EF exp bit, similar as scenario 2 result, default EXP rewrite seems not applied.
        * sniffed traffic in remote CE confirm it
    * Aside of unexpected EXP bit, it is expected that dscp rewrite should not have any impact, since the packet is now forwarded as MPLS labeled packet.



### Scenario 4: custom dscp classifier, default dscp rewrite, NO MPLS 

* similar to scenario 3, but now we are not using MPLS anymore. back to pure IP end to end.
* run the ping command above
* Packet received at remote CE

    ```
    23:37:12.914851  In IP (tos 0x0, ttl  60, id 47830, offset 0, flags [none], proto: ICMP (1), length: 84) 94.0.0.1 > 94.0.0.2: ICMP echo request, id 13053, seq 0, length 64
    ```

* counter at R2

    ```
    rwibawa@skynet_29_02> show firewall counter filter log_traffic be

    Filter: log_traffic
    Counters:
    Name                                                Bytes              Packets
    be                                                    252                    3
    ```

* result
    * everything is expected. 
    * At R1, rw-dscp classifier put ping traffic to BE forwarding class
    * when it goes out, there is dscp default rewrite, R1 forward the packet with dscp 0
    * on remote CE, the packet is received with dscp 0.


### Scenario 5: custom dscp classifier, default EXP rewrite, with MPLS in the backbone

* Similar to Scenario 2, but now, we explicitly configure default EXP rewrite on R1 outgoing interface.
* MPLS is used in the backbone

* Packet received at remote CE

    ```
    03:20:33.987790  In IP (tos 0xe0, ttl  60, id 29928, offset 0, flags [none], proto: ICMP (1), length: 84) 94.0.0.1 > 94.0.0.2: ICMP echo request, id 17416, seq 0, length 64
    ```

* Counter at R2

    ```
    rwibawa@skynet_29_02> show firewall counter filter log_traffic_mpls exp_be

    Filter: log_traffic_mpls
    Counters:
    Name                                                Bytes              Packets
    exp_be                                                264                    3
    ```

* Counter at R3 (next-next-hop)

    ```
    rwibawa@skynet_29_03> show firewall counter filter log_traffic_mpls exp_be

    Filter: log_traffic_mpls
    Counters:
    Name                                                Bytes              Packets
    exp_be                                                264                    3
    ```

* counter at R4 (egress PE)

    ```
    rwibawa@skynet_29_04> show firewall counter filter log_traffic cs7

    Filter: log_traffic
    Counters:
    Name                                                Bytes              Packets
    cs7
    ```

* result
    * everything is expected. 
    * At R1, rw-dscp classifier put ping traffic to BE forwarding class
    * when it goes out, there is EXP default rewrite, R1 forward the packet with exp 0
    * both R2 and R3 (they are P in this scenario), received the packet with EXP bit 0 (BE)
    * R3 is doing PHP, send native IPv4 packet to R4
    * R4 received the IPv4 packet with the original DSCP
    * on remote CE, the packet is received with original DSCP.


### Scenario 6: no BA classifier, no rewrite, firewall filter to reset DSCP

* no BA classifier
* no rewrite
* use firewall filter to reset dscp from CE

```
rwibawa@skynet_29_01# show firewall
filter dhcp_0 {
    term 1 {
        then {
            accept;
            dscp 0;
        }
    }
}

[edit]
rwibawa@skynet_29_01# show interfaces ge-1/0/1
unit 0 {
    family inet {
        filter {
            input dhcp_0;
        }
        address 94.1.1.1/24;
    }
}
```

* received traffic at remote CE

    ```
    In IP (tos 0x0, ttl  60, id 47830, offset 0, flags [none], proto: ICMP (1), length: 84) 94.0.0.1 > 94.0.0.2: ICMP echo request, id 13053, seq 0, length 64
    ```

* counter at R2

    ```
    rwibawa@skynet_29_02> show firewall counter filter log_traffic_mpls exp_be

    Filter: log_traffic_mpls
    Counters:
    Name                                                Bytes              Packets
    exp_be    
    ```

* result

    * firewall filter can be used to clear any marking from CE
    * only set dscp 0 is supported. Setting to any other value is not supported by firewall filter



## Revisit scenario 2: depeer look on EXP bit rewrite

* we want to double check why default EXP rewrite is not applied automcatically.

* re-do scenario 2, but know also double check the following

    * egress queue on R1

	```
	rwibawa@skynet_29_01> show interfaces ge-1/0/2 detail | find "Egress queues"
	  Egress queues: 8 supported, 4 in use
	  Queue counters:       Queued packets  Transmitted packets      Dropped packets
	    0                            36471                36471                    0
	    1                                0                    0                    0
	    2                                0                    0                    0
	    3                            32712                32712                    0
	
	rwibawa@skynet_29_01> show interfaces ge-1/0/2 detail | find "Egress queues"
	  Egress queues: 8 supported, 4 in use
	  Queue counters:       Queued packets  Transmitted packets      Dropped packets
	    0                            37471                37471                    0
	    1                                0                    0                    0
	    2                                0                    0                    0
	    3                            32716                32716                    0
	```

    * seems traffic is correctly placed in BE queue in R1. This means dscp classifier works

    * lets add exp classifier into R2, to force EXP 7 from R1 to go to forwarding class BE at R2

        ```
        rwibawa@skynet_29# show class-of-service classifiers exp rw-exp
        import default;
        forwarding-class rw_be {
            loss-priority high code-points [ 111 110 ];
        }
        ```

    * lets use same ping but with count 1000 rapid

    * lets check egress queue on R2

        ```
        rwibawa@skynet_29_02> show interfaces ge-1/0/4 detail | find "Egress queues"
        Egress queues: 8 supported, 4 in use
        Queue counters:       Queued packets  Transmitted packets      Dropped packets
            0                            22344                22344                    0
            1                            10260                10260                    0
            2                               31                   31                    0
            3                            38946                38946                    0

        rwibawa@skynet_29_02> show interfaces ge-1/0/4 detail | find "Egress queues"
        Egress queues: 8 supported, 4 in use
        Queue counters:       Queued packets  Transmitted packets      Dropped packets
            0                            23346                23346                    0
            1                            10260                10260                    0
            2                               31                   31                    0
            3                            38952                38952                    0
        ```

    * queue 0 increase around 1000 packets, which means exp classifier at R2 is working

    * lets check egress queue on R3. Maybe default EXP rewrite automatically applied only if MPLS to MPLS forwarding.

        ```
        rwibawa@skynet_29_03> show interfaces ge-1/0/6 detail | find "Egress queues"
        Egress queues: 8 supported, 4 in use
        Queue counters:       Queued packets  Transmitted packets      Dropped packets
            0                            22515                22515                    0
            1                            10260                10260                    0
            2                               31                   31                    0
            3                            39978                39978                    0

        rwibawa@skynet_29_03> show interfaces ge-1/0/6 detail | find "Egress queues"
        Egress queues: 8 supported, 4 in use
        Queue counters:       Queued packets  Transmitted packets      Dropped packets
            0                            22515                22515                    0
            1                            10260                10260                    0
            2                               31                   31                    0
            3                            40981                40981                    0
        ```

    * hmm, it is queue 3 that increased around 1000 packets. This means, although R2 re-classify the incoming EXP bit to BE forwarding class, R2 is not doing any EXP rewrite based on forwarding class.
    * this is why R3 still see it as EXP 7 and put it into queue 3.
    * So, the conclusion is, seems default EXP rewrite is not applied automatically on MPLS interface.
        * after searching around, most likely the reason, there are some changes on 14.2 image that we used.
        * if we compare these 2 document version:

            * https://www.juniper.net/documentation/en_US/junos12.3/topics/usage-guidelines/cos-applying-default-rewrite-rules.html

            * https://www.juniper.net/documentation/en_US/junos14.2/topics/usage-guidelines/cos-applying-default-rewrite-rules.html

                ```
                By default, rewrite rules are not usually applied to interfaces. If you want to apply a rewrite rule, you can either design your own rule and apply it to an interface, or you can apply a default rewrite rule.
    
	            Note: The lone exception is that non-MPC MPLS-enabled interfaces use the default EXP rewrite rule, even if not configured.
                ```

            * So, since we are using MPC-based interface, exp rewrite rule is not automatically applied anymore. And we have to explicitly apply it as we did in Scenario 5.

            * Note: This is the hardware that we have

                ```
                rwibawa@skynet_29_01# run show chassis hardware
                Hardware inventory:
                Item             Version                   Description
                Chassis                                    MX240
                Midplane         REV 07                    MX240 Backplane
                FPM Board        REV 06                    Front Panel Display
                PEM 0            Rev 05                    PS 1.2-1.7kW; 100-240V AC in
                Routing Engine 0 REV 01                    RE-S-1800x4
                CB 0             REV 10                    Enhanced MX SCB 2
                FPC 1            REV 11                    MPC2E NG PQ & Flex Q
                CPU            REV 12                    RMPC PMB
                MIC 0          REV 18                    3D 40x 1GE(LAN) RJ45
                    PIC 0                                  10x 1GE(LAN) RJ45
                    PIC 1                                  10x 1GE(LAN) RJ45
                    PIC 2                                  10x 1GE(LAN) RJ45
                    PIC 3                                  10x 1GE(LAN) RJ45
                Fan Tray 0       REV 01                    Enhanced Fan Tray
                ```


