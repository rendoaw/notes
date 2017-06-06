# Example of BGP-LS in JunOS

## Sample config

```
[edit]
user@j1# show protocols bgp group G1
type internal;
local-address 11.105.199.1;
family traffic-engineering {
    unicast;
}
export TE;
neighbor 11.105.199.2;

[edit]
user@j1# show protocols mpls traffic-engineering
bgp-igp-both-ribs;
database {
    import {
        policy TE;
    }
}

[edit]
user@j1# show policy-options policy-statement TE
from family traffic-engineering;
then accept;
```


## Sample output

```
user@j1> show route table lsdist.0 detail | no-more

lsdist.0: 40 destinations, 40 routes (40 active, 0 holddown, 0 hidden)
NODE { AS:11 ISO:0110.0000.0101.00 ISIS-L2:0 }/1152 (1 entry, 1 announced)
        *IS-IS  Preference: 18
                Level: 2
                Next hop type: Fictitious, Next hop index: 0
                Address: 0x9526a04
                Next-hop reference count: 40
                State: <Active NotInstall>
                Local AS:    11
                Age: 1w3d 3:28:07
                Validation State: unverified
                Task: IS-IS
                Announcement bits (1): 0-BGP_RT_Background
                AS path: I
                IPv4 Router-ids:
                  11.0.0.101

NODE { AS:11 ISO:0110.0000.0101.02 ISIS-L2:0 }/1152 (1 entry, 1 announced)
        *IS-IS  Preference: 18
                Level: 2
                Next hop type: Fictitious, Next hop index: 0
                Address: 0x9526a04
                Next-hop reference count: 40
                State: <Active NotInstall>
                Local AS:    11
                Age: 1w3d 3:28:07
                Validation State: unverified
                Task: IS-IS
                Announcement bits (1): 0-BGP_RT_Background
                AS path: I

NODE { AS:11 ISO:0110.0000.0101.03 ISIS-L2:0 }/1152 (1 entry, 1 announced)
        *IS-IS  Preference: 18
                Level: 2
                Next hop type: Fictitious, Next hop index: 0
                Address: 0x9526a04
                Next-hop reference count: 40
                State: <Active NotInstall>
                Local AS:    11
                Age: 1w3d 3:28:07
                Validation State: unverified
                Task: IS-IS
                Announcement bits (1): 0-BGP_RT_Background
                AS path: I

NODE { AS:11 ISO:0110.0000.0102.00 ISIS-L2:0 }/1152 (1 entry, 1 announced)
        *IS-IS  Preference: 18
                Level: 2
                Next hop type: Fictitious, Next hop index: 0
                Address: 0x9526a04
                Next-hop reference count: 40
                State: <Active NotInstall>
                Local AS:    11
                Age: 1w3d 3:28:07
                Validation State: unverified
                Task: IS-IS
                Announcement bits (1): 0-BGP_RT_Background
                AS path: I
                IPv4 Router-ids:
                  11.0.0.102

NODE { AS:11 ISO:0110.0000.0102.02 ISIS-L2:0 }/1152 (1 entry, 1 announced)
        *IS-IS  Preference: 18
                Level: 2
                Next hop type: Fictitious, Next hop index: 0
                Address: 0x9526a04
                Next-hop reference count: 40
                State: <Active NotInstall>
                Local AS:    11
                Age: 1w3d 3:28:07
                Validation State: unverified
                Task: IS-IS
                Announcement bits (1): 0-BGP_RT_Background
                AS path: I

NODE { AS:11 ISO:0110.0000.0102.03 ISIS-L2:0 }/1152 (1 entry, 1 announced)
        *IS-IS  Preference: 18
                Level: 2
                Next hop type: Fictitious, Next hop index: 0
                Address: 0x9526a04
                Next-hop reference count: 40
                State: <Active NotInstall>
                Local AS:    11
                Age: 1w3d 3:28:07
                Validation State: unverified
                Task: IS-IS
                Announcement bits (1): 0-BGP_RT_Background
                AS path: I

NODE { AS:11 ISO:0110.0000.0103.00 ISIS-L2:0 }/1152 (1 entry, 1 announced)
        *IS-IS  Preference: 18
                Level: 2
                Next hop type: Fictitious, Next hop index: 0
                Address: 0x9526a04
                Next-hop reference count: 40
                State: <Active NotInstall>
                Local AS:    11
                Age: 1w3d 3:28:07
                Validation State: unverified
                Task: IS-IS
                Announcement bits (1): 0-BGP_RT_Background
                AS path: I
                IPv4 Router-ids:
                  11.0.0.103

NODE { AS:11 ISO:0110.0000.0104.00 ISIS-L2:0 }/1152 (1 entry, 1 announced)
        *IS-IS  Preference: 18
                Level: 2
                Next hop type: Fictitious, Next hop index: 0
                Address: 0x9526a04
                Next-hop reference count: 40
                State: <Active NotInstall>
                Local AS:    11
                Age: 1w3d 3:28:07
                Validation State: unverified
                Task: IS-IS
                Announcement bits (1): 0-BGP_RT_Background
                AS path: I
                IPv4 Router-ids:
                  11.0.0.104

NODE { AS:11 ISO:0110.0000.0105.00 ISIS-L2:0 }/1152 (1 entry, 1 announced)
        *IS-IS  Preference: 18
                Level: 2
                Next hop type: Fictitious, Next hop index: 0
                Address: 0x9526a04
                Next-hop reference count: 40
                State: <Active NotInstall>
                Local AS:    11
                Age: 1w3d 3:28:07
                Validation State: unverified
                Task: IS-IS
                Announcement bits (1): 0-BGP_RT_Background
                AS path: I
                IPv4 Router-ids:
                  11.0.0.105

NODE { AS:11 ISO:0110.0000.0106.00 ISIS-L2:0 }/1152 (1 entry, 1 announced)
        *IS-IS  Preference: 18
                Level: 2
                Next hop type: Fictitious, Next hop index: 0
                Address: 0x9526a04
                Next-hop reference count: 40
                State: <Active NotInstall>
                Local AS:    11
                Age: 1w3d 3:28:07
                Validation State: unverified
                Task: IS-IS
                Announcement bits (1): 0-BGP_RT_Background
                AS path: I
                IPv4 Router-ids:
                  11.0.0.106

NODE { AS:11 ISO:0110.0000.0107.00 ISIS-L2:0 }/1152 (1 entry, 1 announced)
        *IS-IS  Preference: 18
                Level: 2
                Next hop type: Fictitious, Next hop index: 0
                Address: 0x9526a04
                Next-hop reference count: 40
                State: <Active NotInstall>
                Local AS:    11
                Age: 1w3d 3:28:07
                Validation State: unverified
                Task: IS-IS
                Announcement bits (1): 0-BGP_RT_Background
                AS path: I
                IPv4 Router-ids:
                  11.0.0.107

LINK { Local { AS:11 ISO:0110.0000.0101.00 }.{ IPv4:11.101.105.1 } Remote { AS:11 ISO:0110.0000.0101.03 }.{ } ISIS-L2:0 }/1152 (1 entry, 1 announced)
        *IS-IS  Preference: 18
                Level: 2
                Next hop type: Fictitious, Next hop index: 0
                Address: 0x9526a04
                Next-hop reference count: 40
                State: <Active NotInstall>
                Local AS:    11
                Age: 1w3d 3:28:07
                Validation State: unverified
                Task: IS-IS
                Announcement bits (1): 0-BGP_RT_Background
                AS path: I
                Color: 0
                Maximum bandwidth: 40Gbps
                Reservable bandwidth: 40Gbps
                Unreserved bandwidth by priority:
                  0   39.8699Gbps
                  1   38.3699Gbps
                  2   38.3699Gbps
                  3   38.3699Gbps
                  4   38.3699Gbps
                  5   38.3699Gbps
                  6   38.3699Gbps
                  7   38.3699Gbps
                Metric: 10
                TE Metric: 10
                SRLG membership:
                  srlg-100(0x64)

LINK { Local { AS:11 ISO:0110.0000.0101.02 }.{ } Remote { AS:11 ISO:0110.0000.0101.00 }.{ } ISIS-L2:0 }/1152 (1 entry, 1 announced)
        *IS-IS  Preference: 18
                Level: 2
                Next hop type: Fictitious, Next hop index: 0
                Address: 0x9526a04
                Next-hop reference count: 40
                State: <Active NotInstall>
                Local AS:    11
                Age: 1w3d 3:28:07
                Validation State: unverified
                Task: IS-IS
                Announcement bits (1): 0-BGP_RT_Background
                AS path: I
                TE Metric: 0

LINK { Local { AS:11 ISO:0110.0000.0101.02 }.{ } Remote { AS:11 ISO:0110.0000.0102.00 }.{ } ISIS-L2:0 }/1152 (1 entry, 1 announced)
        *IS-IS  Preference: 18
                Level: 2
                Next hop type: Fictitious, Next hop index: 0
                Address: 0x9526a04
                Next-hop reference count: 40
                State: <Active NotInstall>
                Local AS:    11
                Age: 1w3d 3:28:07
                Validation State: unverified
                Task: IS-IS
                Announcement bits (1): 0-BGP_RT_Background
                AS path: I
                TE Metric: 0

LINK { Local { AS:11 ISO:0110.0000.0101.03 }.{ } Remote { AS:11 ISO:0110.0000.0101.00 }.{ } ISIS-L2:0 }/1152 (1 entry, 1 announced)
        *IS-IS  Preference: 18
                Level: 2
                Next hop type: Fictitious, Next hop index: 0
                Address: 0x9526a04
                Next-hop reference count: 40
                State: <Active NotInstall>
                Local AS:    11
                Age: 1w3d 3:28:07
                Validation State: unverified
                Task: IS-IS
                Announcement bits (1): 0-BGP_RT_Background
                AS path: I
                TE Metric: 0

LINK { Local { AS:11 ISO:0110.0000.0101.03 }.{ } Remote { AS:11 ISO:0110.0000.0105.00 }.{ } ISIS-L2:0 }/1152 (1 entry, 1 announced)
        *IS-IS  Preference: 18
                Level: 2
                Next hop type: Fictitious, Next hop index: 0
                Address: 0x9526a04
                Next-hop reference count: 40
                State: <Active NotInstall>
                Local AS:    11
                Age: 1w3d 3:28:07
                Validation State: unverified
                Task: IS-IS
                Announcement bits (1): 0-BGP_RT_Background
                AS path: I
                TE Metric: 0

LINK { Local { AS:11 ISO:0110.0000.0102.00 }.{ IPv4:11.102.105.1 } Remote { AS:11 ISO:0110.0000.0102.02 }.{ } ISIS-L2:0 }/1152 (1 entry, 1 announced)
        *IS-IS  Preference: 18
                Level: 2
                Next hop type: Fictitious, Next hop index: 0
                Address: 0x9526a04
                Next-hop reference count: 40
                State: <Active NotInstall>
                Local AS:    11
                Age: 1w3d 3:28:07
                Validation State: unverified
                Task: IS-IS
                Announcement bits (1): 0-BGP_RT_Background
                AS path: I
                Color: 0
                Maximum bandwidth: 10Gbps
                Reservable bandwidth: 10Gbps
                Unreserved bandwidth by priority:
                  0   9.5998Gbps
                  1   9.5998Gbps
                  2   9.5998Gbps
                  3   9.5998Gbps
                  4   9.5998Gbps
                  5   9.5998Gbps
                  6   9.5998Gbps
                  7   9.5998Gbps
                Metric: 10
                TE Metric: 10
                SRLG membership:
                  srlg-100(0x64)

LINK { Local { AS:11 ISO:0110.0000.0102.00 }.{ IPv4:11.102.106.1 } Remote { AS:11 ISO:0110.0000.0102.03 }.{ } ISIS-L2:0 }/1152 (1 entry, 1 announced)
        *IS-IS  Preference: 18
                Level: 2
                Next hop type: Fictitious, Next hop index: 0
                Address: 0x9526a04
                Next-hop reference count: 40
                State: <Active NotInstall>
                Local AS:    11
                Age: 1w3d 3:28:07
                Validation State: unverified
                Task: IS-IS
                Announcement bits (1): 0-BGP_RT_Background
                AS path: I
                Color: 0
                Maximum bandwidth: 40Gbps
                Reservable bandwidth: 40Gbps
                Unreserved bandwidth by priority:
                  0   39.9Gbps
                  1   39.9Gbps
                  2   39.9Gbps
                  3   39.9Gbps
                  4   39.9Gbps
                  5   39.9Gbps
                  6   39.9Gbps
                  7   39.9Gbps
                Metric: 50
                TE Metric: 50

LINK { Local { AS:11 ISO:0110.0000.0102.02 }.{ } Remote { AS:11 ISO:0110.0000.0102.00 }.{ } ISIS-L2:0 }/1152 (1 entry, 1 announced)
        *IS-IS  Preference: 18
                Level: 2
                Next hop type: Fictitious, Next hop index: 0
                Address: 0x9526a04
                Next-hop reference count: 40
                State: <Active NotInstall>
                Local AS:    11
                Age: 1w3d 3:28:07
                Validation State: unverified
                Task: IS-IS
                Announcement bits (1): 0-BGP_RT_Background
                AS path: I
                TE Metric: 0

LINK { Local { AS:11 ISO:0110.0000.0102.02 }.{ } Remote { AS:11 ISO:0110.0000.0105.00 }.{ } ISIS-L2:0 }/1152 (1 entry, 1 announced)
        *IS-IS  Preference: 18
                Level: 2
                Next hop type: Fictitious, Next hop index: 0
                Address: 0x9526a04
                Next-hop reference count: 40
                State: <Active NotInstall>
                Local AS:    11
                Age: 1w3d 3:28:07
                Validation State: unverified
                Task: IS-IS
                Announcement bits (1): 0-BGP_RT_Background
                AS path: I
                TE Metric: 0

LINK { Local { AS:11 ISO:0110.0000.0102.03 }.{ } Remote { AS:11 ISO:0110.0000.0102.00 }.{ } ISIS-L2:0 }/1152 (1 entry, 1 announced)
        *IS-IS  Preference: 18
                Level: 2
                Next hop type: Fictitious, Next hop index: 0
                Address: 0x9526a04
                Next-hop reference count: 40
                State: <Active NotInstall>
                Local AS:    11
                Age: 1w3d 3:28:07
                Validation State: unverified
                Task: IS-IS
                Announcement bits (1): 0-BGP_RT_Background
                AS path: I
                TE Metric: 0

LINK { Local { AS:11 ISO:0110.0000.0102.03 }.{ } Remote { AS:11 ISO:0110.0000.0106.00 }.{ } ISIS-L2:0 }/1152 (1 entry, 1 announced)
        *IS-IS  Preference: 18
                Level: 2
                Next hop type: Fictitious, Next hop index: 0
                Address: 0x9526a04
                Next-hop reference count: 40
                State: <Active NotInstall>
                Local AS:    11
                Age: 1w3d 3:28:07
                Validation State: unverified
                Task: IS-IS
                Announcement bits (1): 0-BGP_RT_Background
                AS path: I
                TE Metric: 0

LINK { Local { AS:11 ISO:0110.0000.0103.00 }.{ IPv4:11.103.107.1 } Remote { AS:11 ISO:0110.0000.0107.00 }.{ IPv4:11.103.107.2 } ISIS-L2:0 }/1152 (1 entry, 1 announced)
        *IS-IS  Preference: 18
                Level: 2
                Next hop type: Fictitious, Next hop index: 0
                Address: 0x9526a04
                Next-hop reference count: 40
                State: <Active NotInstall>
                Local AS:    11
                Age: 1w3d 3:28:07
                Validation State: unverified
                Task: IS-IS
                Announcement bits (1): 0-BGP_RT_Background
                AS path: I
                Color: 0
                Maximum bandwidth: 40Gbps
                Reservable bandwidth: 40Gbps
                Unreserved bandwidth by priority:
                  0   39.97Gbps
                  1   39.97Gbps
                  2   39.97Gbps
                  3   38.47Gbps
                  4   38.47Gbps
                  5   38.47Gbps
                  6   38.47Gbps
                  7   38.47Gbps
                Metric: 10
                TE Metric: 10

LINK { Local { AS:11 ISO:0110.0000.0104.00 }.{ IPv4:11.104.106.1 } Remote { AS:11 ISO:0110.0000.0106.00 }.{ IPv4:11.104.106.2 } ISIS-L2:0 }/1152 (1 entry, 1 announced)
        *IS-IS  Preference: 18
                Level: 2
                Next hop type: Fictitious, Next hop index: 0
                Address: 0x9526a04
                Next-hop reference count: 40
                State: <Active NotInstall>
                Local AS:    11
                Age: 1w3d 3:28:07
                Validation State: unverified
                Task: IS-IS
                Announcement bits (1): 0-BGP_RT_Background
                AS path: I
                Color: 0
                Maximum bandwidth: 40Gbps
                Reservable bandwidth: 40Gbps
                Unreserved bandwidth by priority:
                  0   40Gbps
                  1   40Gbps
                  2   40Gbps
                  3   40Gbps
                  4   40Gbps
                  5   40Gbps
                  6   40Gbps
                  7   40Gbps
                Metric: 50
                TE Metric: 50

LINK { Local { AS:11 ISO:0110.0000.0104.00 }.{ IPv4:11.104.107.1 } Remote { AS:11 ISO:0110.0000.0107.00 }.{ IPv4:11.104.107.2 } ISIS-L2:0 }/1152 (1 entry, 1 announced)
        *IS-IS  Preference: 18
                Level: 2
                Next hop type: Fictitious, Next hop index: 0
                Address: 0x9526a04
                Next-hop reference count: 40
                State: <Active NotInstall>
                Local AS:    11
                Age: 1w3d 3:28:07
                Validation State: unverified
                Task: IS-IS
                Announcement bits (1): 0-BGP_RT_Background
                AS path: I
                Color: 0
                Maximum bandwidth: 10Gbps
                Reservable bandwidth: 10Gbps
                Unreserved bandwidth by priority:
                  0   9.9Gbps
                  1   9.9Gbps
                  2   9.9Gbps
                  3   9.9Gbps
                  4   9.9Gbps
                  5   9.9Gbps
                  6   9.9Gbps
                  7   9.9Gbps
                Metric: 11
                TE Metric: 11
                SRLG membership:
                  srlg-407(0x197)

LINK { Local { AS:11 ISO:0110.0000.0104.00 }.{ IPv4:11.114.117.1 } Remote { AS:11 ISO:0110.0000.0107.00 }.{ IPv4:11.114.117.2 } ISIS-L2:0 }/1152 (1 entry, 1 announced)
        *IS-IS  Preference: 18
                Level: 2
                Next hop type: Fictitious, Next hop index: 0
                Address: 0x9526a04
                Next-hop reference count: 40
                State: <Active NotInstall>
                Local AS:    11
                Age: 1w3d 3:28:07
                Validation State: unverified
                Task: IS-IS
                Announcement bits (1): 0-BGP_RT_Background
                AS path: I
                Color: 0
                Maximum bandwidth: 10Gbps
                Reservable bandwidth: 10Gbps
                Unreserved bandwidth by priority:
                  0   10Gbps
                  1   10Gbps
                  2   10Gbps
                  3   10Gbps
                  4   10Gbps
                  5   10Gbps
                  6   10Gbps
                  7   10Gbps
                Metric: 20
                TE Metric: 20
                SRLG membership:
                  srlg-407(0x197)

LINK { Local { AS:11 ISO:0110.0000.0105.00 }.{ IPv4:11.101.105.2 } Remote { AS:11 ISO:0110.0000.0101.03 }.{ } ISIS-L2:0 }/1152 (1 entry, 1 announced)
        *IS-IS  Preference: 18
                Level: 2
                Next hop type: Fictitious, Next hop index: 0
                Address: 0x9526a04
                Next-hop reference count: 40
                State: <Active NotInstall>
                Local AS:    11
                Age: 1w3d 3:28:07
                Validation State: unverified
                Task: IS-IS
                Announcement bits (1): 0-BGP_RT_Background
                AS path: I
                Color: 0
                Maximum bandwidth: 40Gbps
                Reservable bandwidth: 40Gbps
                Unreserved bandwidth by priority:
                  0   39.57Gbps
                  1   39.57Gbps
                  2   39.57Gbps
                  3   39.07Gbps
                  4   39.07Gbps
                  5   39.07Gbps
                  6   39.07Gbps
                  7   39.07Gbps
                Metric: 10
                TE Metric: 10

LINK { Local { AS:11 ISO:0110.0000.0105.00 }.{ IPv4:11.102.105.2 } Remote { AS:11 ISO:0110.0000.0102.02 }.{ } ISIS-L2:0 }/1152 (1 entry, 1 announced)
        *IS-IS  Preference: 18
                Level: 2
                Next hop type: Fictitious, Next hop index: 0
                Address: 0x9526a04
                Next-hop reference count: 40
                State: <Active NotInstall>
                Local AS:    11
                Age: 1w3d 3:28:07
                Validation State: unverified
                Task: IS-IS
                Announcement bits (1): 0-BGP_RT_Background
                AS path: I
                Color: 0
                Maximum bandwidth: 10Gbps
                Reservable bandwidth: 10Gbps
                Unreserved bandwidth by priority:
                  0   9.9Gbps
                  1   9.4Gbps
                  2   9.4Gbps
                  3   8.9Gbps
                  4   8.9Gbps
                  5   8.9Gbps
                  6   8.9Gbps
                  7   8.9Gbps
                Metric: 10
                TE Metric: 10

LINK { Local { AS:11 ISO:0110.0000.0105.00 }.{ IPv4:11.105.106.1 } Remote { AS:11 ISO:0110.0000.0106.00 }.{ IPv4:11.105.106.2 } ISIS-L2:0 }/1152 (1 entry, 1 announced)
        *IS-IS  Preference: 18
                Level: 2
                Next hop type: Fictitious, Next hop index: 0
                Address: 0x9526a04
                Next-hop reference count: 40
                State: <Active NotInstall>
                Local AS:    11
                Age: 1w3d 3:28:07
                Validation State: unverified
                Task: IS-IS
                Announcement bits (1): 0-BGP_RT_Background
                AS path: I
                Color: 0
                Maximum bandwidth: 10Gbps
                Reservable bandwidth: 10Gbps
                Unreserved bandwidth by priority:
                  0   10Gbps
                  1   10Gbps
                  2   10Gbps
                  3   10Gbps
                  4   10Gbps
                  5   10Gbps
                  6   10Gbps
                  7   10Gbps
                Metric: 10
                TE Metric: 10

LINK { Local { AS:11 ISO:0110.0000.0105.00 }.{ IPv4:11.105.107.1 } Remote { AS:11 ISO:0110.0000.0107.00 }.{ IPv4:11.105.107.2 } ISIS-L2:0 }/1152 (1 entry, 1 announced)
        *IS-IS  Preference: 18
                Level: 2
                Next hop type: Fictitious, Next hop index: 0
                Address: 0x9526a04
                Next-hop reference count: 40
                State: <Active NotInstall>
                Local AS:    11
                Age: 1w3d 3:28:07
                Validation State: unverified
                Task: IS-IS
                Announcement bits (1): 0-BGP_RT_Background
                AS path: I
                Color: 0
                Maximum bandwidth: 10Gbps
                Reservable bandwidth: 10Gbps
                Unreserved bandwidth by priority:
                  0   9.5697Gbps
                  1   8.5697Gbps
                  2   8.5697Gbps
                  3   8.5697Gbps
                  4   8.5697Gbps
                  5   8.5697Gbps
                  6   8.5697Gbps
                  7   8.5697Gbps
                Metric: 10
                TE Metric: 10

LINK { Local { AS:11 ISO:0110.0000.0105.00 }.{ IPv4:111.1.11.2 } Remote { AS:11 ISO:0010.0000.0004.00 }.{ IPv4:111.1.11.1 } ISIS-L2:0 }/1152 (1 entry, 1 announced)
        *IS-IS  Preference: 18
                Level: 2
                Next hop type: Fictitious, Next hop index: 0
                Address: 0x9526a04
                Next-hop reference count: 40
                State: <Active NotInstall>
                Local AS:    11
                Age: 1w3d 3:28:07
                Validation State: unverified
                Task: IS-IS
                Announcement bits (1): 0-BGP_RT_Background
                AS path: I
                Color: 0
                Maximum bandwidth: 10Gbps
                Reservable bandwidth: 10Gbps
                Unreserved bandwidth by priority:
                  0   10Gbps
                  1   10Gbps
                  2   10Gbps
                  3   10Gbps
                  4   10Gbps
                  5   10Gbps
                  6   10Gbps
                  7   10Gbps
                Metric: 10
                TE Metric: 10

LINK { Local { AS:11 ISO:0110.0000.0106.00 }.{ IPv4:11.102.106.2 } Remote { AS:11 ISO:0110.0000.0102.03 }.{ } ISIS-L2:0 }/1152 (1 entry, 1 announced)
        *IS-IS  Preference: 18
                Level: 2
                Next hop type: Fictitious, Next hop index: 0
                Address: 0x9526a04
                Next-hop reference count: 40
                State: <Active NotInstall>
                Local AS:    11
                Age: 1w3d 3:28:07
                Validation State: unverified
                Task: IS-IS
                Announcement bits (1): 0-BGP_RT_Background
                AS path: I
                Color: 0
                Maximum bandwidth: 40Gbps
                Reservable bandwidth: 40Gbps
                Unreserved bandwidth by priority:
                  0   40Gbps
                  1   40Gbps
                  2   40Gbps
                  3   40Gbps
                  4   40Gbps
                  5   40Gbps
                  6   40Gbps
                  7   40Gbps
                Metric: 50
                TE Metric: 50

LINK { Local { AS:11 ISO:0110.0000.0106.00 }.{ IPv4:11.104.106.2 } Remote { AS:11 ISO:0110.0000.0104.00 }.{ IPv4:11.104.106.1 } ISIS-L2:0 }/1152 (1 entry, 1 announced)
        *IS-IS  Preference: 18
                Level: 2
                Next hop type: Fictitious, Next hop index: 0
                Address: 0x9526a04
                Next-hop reference count: 40
                State: <Active NotInstall>
                Local AS:    11
                Age: 1w3d 3:28:07
                Validation State: unverified
                Task: IS-IS
                Announcement bits (1): 0-BGP_RT_Background
                AS path: I
                Color: 0
                Maximum bandwidth: 40Gbps
                Reservable bandwidth: 40Gbps
                Unreserved bandwidth by priority:
                  0   39.9Gbps
                  1   39.9Gbps
                  2   39.9Gbps
                  3   39.9Gbps
                  4   39.9Gbps
                  5   39.9Gbps
                  6   39.9Gbps
                  7   39.9Gbps
                Metric: 50
                TE Metric: 50

LINK { Local { AS:11 ISO:0110.0000.0106.00 }.{ IPv4:11.105.106.2 } Remote { AS:11 ISO:0110.0000.0105.00 }.{ IPv4:11.105.106.1 } ISIS-L2:0 }/1152 (1 entry, 1 announced)
        *IS-IS  Preference: 18
                Level: 2
                Next hop type: Fictitious, Next hop index: 0
                Address: 0x9526a04
                Next-hop reference count: 40
                State: <Active NotInstall>
                Local AS:    11
                Age: 1w3d 3:28:07
                Validation State: unverified
                Task: IS-IS
                Announcement bits (1): 0-BGP_RT_Background
                AS path: I
                Color: 0
                Maximum bandwidth: 10Gbps
                Reservable bandwidth: 10Gbps
                Unreserved bandwidth by priority:
                  0   10Gbps
                  1   10Gbps
                  2   10Gbps
                  3   10Gbps
                  4   10Gbps
                  5   10Gbps
                  6   10Gbps
                  7   10Gbps
                Metric: 10
                TE Metric: 10

LINK { Local { AS:11 ISO:0110.0000.0106.00 }.{ IPv4:11.106.107.1 } Remote { AS:11 ISO:0110.0000.0107.00 }.{ IPv4:11.106.107.2 } ISIS-L2:0 }/1152 (1 entry, 1 announced)
        *IS-IS  Preference: 18
                Level: 2
                Next hop type: Fictitious, Next hop index: 0
                Address: 0x9526a04
                Next-hop reference count: 40
                State: <Active NotInstall>
                Local AS:    11
                Age: 1w3d 3:28:07
                Validation State: unverified
                Task: IS-IS
                Announcement bits (1): 0-BGP_RT_Background
                AS path: I
                Color: 0
                Maximum bandwidth: 10Gbps
                Reservable bandwidth: 10Gbps
                Unreserved bandwidth by priority:
                  0   10Gbps
                  1   10Gbps
                  2   10Gbps
                  3   10Gbps
                  4   10Gbps
                  5   10Gbps
                  6   10Gbps
                  7   10Gbps
                Metric: 30
                TE Metric: 30

LINK { Local { AS:11 ISO:0110.0000.0107.00 }.{ IPv4:11.103.107.2 } Remote { AS:11 ISO:0110.0000.0103.00 }.{ IPv4:11.103.107.1 } ISIS-L2:0 }/1152 (1 entry, 1 announced)
        *IS-IS  Preference: 18
                Level: 2
                Next hop type: Fictitious, Next hop index: 0
                Address: 0x9526a04
                Next-hop reference count: 40
                State: <Active NotInstall>
                Local AS:    11
                Age: 1w3d 3:28:07
                Validation State: unverified
                Task: IS-IS
                Announcement bits (1): 0-BGP_RT_Background
                AS path: I
                Color: 0
                Maximum bandwidth: 40Gbps
                Reservable bandwidth: 40Gbps
                Unreserved bandwidth by priority:
                  0   39.47Gbps
                  1   38.97Gbps
                  2   38.97Gbps
                  3   38.97Gbps
                  4   38.97Gbps
                  5   38.97Gbps
                  6   38.97Gbps
                  7   38.97Gbps
                Metric: 10
                TE Metric: 10

LINK { Local { AS:11 ISO:0110.0000.0107.00 }.{ IPv4:11.104.107.2 } Remote { AS:11 ISO:0110.0000.0104.00 }.{ IPv4:11.104.107.1 } ISIS-L2:0 }/1152 (1 entry, 1 announced)
        *IS-IS  Preference: 18
                Level: 2
                Next hop type: Fictitious, Next hop index: 0
                Address: 0x9526a04
                Next-hop reference count: 40
                State: <Active NotInstall>
                Local AS:    11
                Age: 1w3d 3:28:07
                Validation State: unverified
                Task: IS-IS
                Announcement bits (1): 0-BGP_RT_Background
                AS path: I
                Color: 0
                Maximum bandwidth: 10Gbps
                Reservable bandwidth: 10Gbps
                Unreserved bandwidth by priority:
                  0   9.6Gbps
                  1   9.6Gbps
                  2   9.6Gbps
                  3   9.1Gbps
                  4   9.1Gbps
                  5   9.1Gbps
                  6   9.1Gbps
                  7   9.1Gbps
                Metric: 10
                TE Metric: 10
                SRLG membership:
                  srlg-407(0x197)

LINK { Local { AS:11 ISO:0110.0000.0107.00 }.{ IPv4:11.105.107.2 } Remote { AS:11 ISO:0110.0000.0105.00 }.{ IPv4:11.105.107.1 } ISIS-L2:0 }/1152 (1 entry, 1 announced)
        *IS-IS  Preference: 18
                Level: 2
                Next hop type: Fictitious, Next hop index: 0
                Address: 0x9526a04
                Next-hop reference count: 40
                State: <Active NotInstall>
                Local AS:    11
                Age: 1w3d 3:28:07
                Validation State: unverified
                Task: IS-IS
                Announcement bits (1): 0-BGP_RT_Background
                AS path: I
                Color: 0
                Maximum bandwidth: 10Gbps
                Reservable bandwidth: 10Gbps
                Unreserved bandwidth by priority:
                  0   9.97Gbps
                  1   9.97Gbps
                  2   9.97Gbps
                  3   8.97Gbps
                  4   8.97Gbps
                  5   8.97Gbps
                  6   8.97Gbps
                  7   8.97Gbps
                Metric: 10
                TE Metric: 10

LINK { Local { AS:11 ISO:0110.0000.0107.00 }.{ IPv4:11.106.107.2 } Remote { AS:11 ISO:0110.0000.0106.00 }.{ IPv4:11.106.107.1 } ISIS-L2:0 }/1152 (1 entry, 1 announced)
        *IS-IS  Preference: 18
                Level: 2
                Next hop type: Fictitious, Next hop index: 0
                Address: 0x9526a04
                Next-hop reference count: 40
                State: <Active NotInstall>
                Local AS:    11
                Age: 1w3d 3:28:07
                Validation State: unverified
                Task: IS-IS
                Announcement bits (1): 0-BGP_RT_Background
                AS path: I
                Color: 0
                Maximum bandwidth: 10Gbps
                Reservable bandwidth: 10Gbps
                Unreserved bandwidth by priority:
                  0   10Gbps
                  1   10Gbps
                  2   10Gbps
                  3   10Gbps
                  4   10Gbps
                  5   10Gbps
                  6   10Gbps
                  7   10Gbps
                Metric: 30
                TE Metric: 30

LINK { Local { AS:11 ISO:0110.0000.0107.00 }.{ IPv4:11.114.117.2 } Remote { AS:11 ISO:0110.0000.0104.00 }.{ IPv4:11.114.117.1 } ISIS-L2:0 }/1152 (1 entry, 1 announced)
        *IS-IS  Preference: 18
                Level: 2
                Next hop type: Fictitious, Next hop index: 0
                Address: 0x9526a04
                Next-hop reference count: 40
                State: <Active NotInstall>
                Local AS:    11
                Age: 1w3d 3:28:07
                Validation State: unverified
                Task: IS-IS
                Announcement bits (1): 0-BGP_RT_Background
                AS path: I
                Color: 0
                Maximum bandwidth: 10Gbps
                Reservable bandwidth: 10Gbps
                Unreserved bandwidth by priority:
                  0   10Gbps
                  1   9.5Gbps
                  2   9.5Gbps
                  3   9.5Gbps
                  4   9.5Gbps
                  5   9.5Gbps
                  6   9.5Gbps
                  7   9.5Gbps
                Metric: 10
                TE Metric: 10
                SRLG membership:
                  srlg-407(0x197)

user@j1>
```
