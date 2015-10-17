# JunOS - Duplicated IPv6 Link Local 

## Problem
* One side of ISIS link lists the neighbor with "!" mark
* The other side shows "Addresses, Flags: Is-Preferred Duplicate"


## Symptomp

### at neighbor router

    ```
    lab@vmx-13-17# run show isis adjacency
    Interface             System         L State        Hold (secs) SNPA
    ge-0/0/3.0            vmx-13-18     ! 2 Up                    8  0:50:58:13:18:5
    ge-0/0/4.0            vmx-13-15      2  Up                   25  0:50:58:13:15:7


    lab@vmx-13-17# run show interfaces ge-0/0/3.0
    Logical interface ge-0/0/3.0 (Index 339) (SNMP ifIndex 555)
        Description: R8
        Flags: Up SNMP-Traps 0x4004000 Encapsulation: ENET2
        Input packets : 501571
        Output packets: 256001
        Protocol inet, MTU: 1500
        Flags: Sendbcast-pkt-to-re
        Addresses, Flags: Is-Preferred Is-Primary
            Destination: 89.100.0.0/30, Local: 89.100.0.1, Broadcast: 89.100.0.3
        Protocol iso, MTU: 1497
        Protocol inet6, MTU: 1500
        Flags: Is-Primary
        Addresses, Flags: Is-Preferred Is-Primary
            Destination: 2400:67:176:0:78::/126, Local: 2400:67:176:0:78::1
        Addresses, Flags: Is-Preferred
            Destination: fe80::/64, Local: fe80::205:86ff:fee6:1f01
        Protocol mpls, MTU: 1488, Maximum labels: 3
        Protocol multiservice, MTU: Unlimited


    ```

### at local router

* Flags: Protocol-Down
* Flags: Is-Preferred Duplicate

    ```

    lab@vmx-13-18# run show interfaces ge-0/0/1.0
    Logical interface ge-0/0/1.0 (Index 333) (SNMP ifIndex 552)
        Description: R7
        Flags: Up SNMP-Traps 0x4004000 Encapsulation: ENET2
        Input packets : 274249
        Output packets: 480226
        Protocol inet, MTU: 1500
        Flags: Sendbcast-pkt-to-re
        Addresses, Flags: Is-Preferred Is-Primary
            Destination: 89.100.0.0/30, Local: 89.100.0.2, Broadcast: 89.100.0.3
        Protocol iso, MTU: 1497
        Protocol inet6, MTU: 1500
        Flags: Protocol-Down, Down, Is-Primary
        Addresses, Flags: Is-Preferred Is-Primary
            Destination: 2400:67:176:0:78::/126, Local: 2400:67:176:0:78::2
            INET6 Address Flags: Tentative
        Addresses, Flags: Is-Preferred Duplicate
            Destination: fe80::/64, Local: fe80::205:86ff:fee6:1f01
            INET6 Address Flags: Duplicate
        Protocol mpls, MTU: 1488, Maximum labels: 3
        Protocol multiservice, MTU: Unlimited

    ```


## Analysis

## Solution

### at local router

    ```

    [edit]
    lab@vmx-13-18#

    [edit]
    lab@vmx-13-18# set interfaces ge-0/0/1.0 family inet6 address fe80::205:86ff:fee6:1f18/64

    [edit]
    lab@vmx-13-18# commit
    commit complete

    [edit]
    lab@vmx-13-18# set interfaces ge-0/0/1.0 disable

    [edit]
    lab@vmx-13-18# commit
    commit complete

    [edit]
    lab@vmx-13-18# delete interfaces ge-0/0/1.0 disable

    [edit]
    lab@vmx-13-18# commit
    commit complete

    ```


## Verification

### at neighbor router

    ```
    [edit]
    lab@vmx-13-17# run show isis adjacency
    Interface             System         L State        Hold (secs) SNPA
    ge-0/0/3.0            vmx-13-18      2  Up                    7  0:50:58:13:18:5
    ge-0/0/4.0            vmx-13-15      2  Up                   26  0:50:58:13:15:7
    ```



