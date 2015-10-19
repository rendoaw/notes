
## Configuration

### PE

```
rwibawa@vmx-13-11# show interfaces ge-0/0/0 unit 941
vlan-id 941;
family inet {
    address 67.176.0.161/30;
}
family inet6 {
    address 2400:67:176:6::1/126;
}

rwibawa@vmx-13-11# show protocols bgp group as766
type external;
family inet {
    unicast;
}
family inet6 {
    unicast;
}
peer-as 766;
neighbor 67.176.0.162;
```

### CE

```
rwibawa@VR# show interfaces lo0.941
family inet {
    address 76.6.255.11/32;
}
family inet6 {
    address 2476:6:255::11/128;
}

[edit]
rwibawa@VR# show interfaces ge-0/0/0.941
vlan-id 941;
family inet {
    address 67.176.0.162/30;
}
family inet6 {
    address 2400:67:176:6::2/126;
}

rwibawa@VR# show protocols bgp
export rw-advertise-direct-all;
local-as 766;
group to-R1 {
    type external;
    family inet {
        unicast;
    }
    family inet6 {
        unicast;
    }
    peer-as 16689.7041;
    neighbor 67.176.0.161;
}

rwibawa@VR# top show policy-options policy-statement rw-advertise-direct-all
term 1 {
    from protocol direct;
    then accept;
}
```



## Initial result

* IPv6 prefix from the CE listed as hidden

```
rwibawa@vmx-13-11# run show route receive-protocol bgp 67.176.0.162 hidden extensive
...

inet6.0: 30 destinations, 33 routes (29 active, 0 holddown, 2 hidden)
  2400:67:176:6::/126 (2 entries, 1 announced)
     Nexthop: ::ffff:67.176.0.162
     AS path: 766 I
     Hidden reason: protocol nexthop is not on the interface

  2476:6:255::11/128 (1 entry, 0 announced)
     Nexthop: ::ffff:67.176.0.162
     AS path: 766 I
     Hidden reason: protocol nexthop is not on the interface

...
```


## Problem

* IPv6 prefix is hidden because BGP peering is using IPv4. In this case, for any inet6 prefix, JunOS automatically map the next-hop to ::ffff:x.x.x.x IPv4-Mapped IPv6 Address. 
* Since the interface is actually using different format, regardless normal IPv6 format or ::x.x.x.x IPv4 mapped format, JunOS will consider the next-hop IP is unreachable.

## Solution

* configure accept-remote-nexthop
* change next-hop with the correct neighbor IPv6 address with BGP import policy
* in addition to that, we also need to make sure that PE advertise correct next-hop for IPv6 prefix. We use export policy to change this.

    ```
    rwibawa@vmx-13-11# show protocols bgp group as766
    type external;
    accept-remote-nexthop;
    import as766-import;
    family inet {
        unicast;
    }
    family inet6 {
        unicast;
    }
    export [ as766-export reject ];
    peer-as 766;
    neighbor 67.176.0.162;

    
    rwibawa@vmx-13-11# show policy-options policy-statement as766-import
    term 1 {
        from next-hop ::ffff:67.176.0.162;
        then {
            next-hop 2400:67:176:6::2;
            accept;
        }
    }    
    
    rwibawa@vmx-13-11# show policy-options policy-statement as766-export
    term 1 {
        from {
            protocol direct;
            rib inet6.0;
        }
        then {
            next-hop 2400:67:176:6::1;
            accept;
        }
    }
    term 2 {
        from protocol direct;
        then accept;
    }    
    ```

## Verification

* make sure no hidden route anymore

    ```
    rwibawa@vmx-13-11# run show route receive-protocol bgp 67.176.0.162 hidden table inet6.0

    inet6.0: 30 destinations, 33 routes (30 active, 0 holddown, 0 hidden)


    rwibawa@vmx-13-11# run show route receive-protocol bgp 67.176.0.162 table inet6

    inet6.0: 30 destinations, 33 routes (30 active, 0 holddown, 0 hidden)
    Prefix                  Nexthop              MED     Lclpref    AS path
    2400:67:176:6::/126     ::ffff:67.176.0.162                     766 I
    * 2476:6:255::11/128      ::ffff:67.176.0.162                     766 I

    ```

* make sure PE send correct next-hop

    ```
    rwibawa@vmx-13-11# run show route advertising-protocol bgp 67.176.0.162 table inet6.0

    inet6.0: 30 destinations, 33 routes (30 active, 0 holddown, 0 hidden)
    Prefix                  Nexthop              MED     Lclpref    AS path
    * ::67.176.0.156/126      2400:67:176:6::1                        I
    2400:67:176:0:12::/126
    *                         2400:67:176:6::1                        I
    2400:67:176:0:13::/126
    *                         2400:67:176:6::1                        I
    * 2400:67:176:6::/126     2400:67:176:6::1                        I
    2400:67:176:255::1/128
    *                         2400:67:176:6::1                        I
    ```

## Alternative solution

* You can avoid the problem above by configuring explicit IPv6 BGP neighbor. In this case, we will have 2 BGP sessions to the same CE, 1 peering for IPv4 and the other peering for IPv6.




