# Cisco IOS-XR Config Example for PCEP and BGP-LS

## Notes
* if lsp-delegation is enabled globally under mpls traffic-eng -> pce section, looks like all configured LSP will become delegated LSP
* LSP delegation can be enabled per LSP


## PCEP 

### Configuration

* To configure tunnel source address. Without this, PCE initiated/delegated  LSP will not up

    ```
    ipv4 unnumbered mpls traffic-eng Loopback0
    ```

* PCEP configuration

    ```
    mpls traffic-eng
      pce
        peer source ipv4 13.0.0.2
        peer ipv4 1.1.1.178
          precedence 20
        ! 
        stateful-client
          instantiation
          delegation    --> optional. If set, all LSP become delegated
          report
        !
      !
      auto-tunnel pcc
      tunnel-id min 1000 max 5000
      !
    !
    ```

* check PCE server status

    ```
    RP/0/0/CPU0:xr-13-02#show mpls traffic-eng pce peer all
    Sat Jul 18 01:36:41.365 UTC

    PCE Address 1.1.1.178
    State Up
    PCEP has been up for: 00:00:07
    Precedence 20
    Learned through:
    Static Config
    Sending KA every 30 s
    Time out peer if no KA received for 120 s
    Tolerance: Minimum KA 10 s

    Stateful
    Update capability
    Instantiation capability


    KA messages rxed 242 txed 238
    PCEReq messages rxed 0, txed 0
    PCERep messages rxed 0, txed 0
    PCEErr messages rxed 0, txed 0
    Last error received:  None
    Last error sent:  None
    PCE OPEN messages: rxed 5, txed 5
    PCERpt messages rxed 0, txed 16
    PCEUpd messages rxed 0, txed 0
    PCEInit messages rxed 2, txed 0
    PCEP session ID: local 4, remote 0

    Average reply time from peer: 0 ms
    Minimum reply time from peer: 0 ms
    Maximum reply time from peer: 0 ms
    0 requests timed out with this peer
    ```


### PCC Controller LSP/Normal LSP

* By default, IOS-XR doesn't send RRO to PCE server unless "record-route" is explicitly configured

    ```
    interface tunnel-te0
     ipv4 unnumbered Loopback0
     destination 13.0.0.4
     record-route
     path-option 10 dynamic
    !
    ```


### Delegated LSP

* The following LSP is delegated to PCE server. Make sure both path option and pce delegation are set properly.

```
interface tunnel-te1
 ipv4 unnumbered Loopback0
 destination 13.0.0.4
 record-route
 path-option 10 dynamic pce
 pce
  delegation
!
```

* The following LSP will prefer path received from external controller and if external controller is not available, it will fallback to router own calculated dynamic path 

```
interface tunnel-te3
 ipv4 unnumbered Loopback0
 destination 13.0.0.4
 record-route
 path-option 10 dynamic pce
 path-option 20 dynamic
 pce
  delegation
 !
!
```

* this is what looks like when external controller is available

```
    RP/0/0/CPU0:xr-13-02#show mpls traffic-eng tunnels name tunnel-te3 detail
    Sat Jul 18 01:16:56.716 UTC


    Name: tunnel-te3  Destination: 13.0.0.4  Ifhandle:0x680
    Signalled-Name: xr-13-02_t3
    Status:
        Admin:    up Oper:   up   Path:  valid   Signalling: connected

        path option 10, (verbatim) type explicit (autopcc_te3) (Basis for Setup, path weight 20)
        Protected-by PO index: 20
        G-PID: 0x0800 (derived from egress interface properties)
        Bandwidth Requested: 0 kbps  CT0
        Creation Time: Sat Jul 18 01:16:31 2015 (00:00:25 ago)
    Config Parameters:
        Bandwidth:        0 kbps (CT0) Priority:  7  7 Affinity: 0x0/0xffff
        Metric Type: TE (default)
        Hop-limit: disabled
        Cost-limit: disabled
        AutoRoute: disabled  LockDown: disabled   Policy class: not set
        Forward class: 0 (default)
        Forwarding-Adjacency: disabled
        Loadshare:          0 equal loadshares
        Auto-bw: disabled
        Fast Reroute: Disabled, Protection Desired: None
        Path Protection: Not Enabled
        BFD Fast Detection: Disabled
        Reoptimization after affinity failure: Enabled
        Soft Preemption: Disabled
    PCE Delegation:
        Symbolic name: xr-13-02_t3
        PCEP ID: 4
        Delegated to: 1.1.1.178
    SNMP Index: 15
    History:
        Tunnel has been up for: 00:00:24 (since Sat Jul 18 01:16:32 UTC 2015)
        Current LSP:
        Uptime: 00:00:24 (since Sat Jul 18 01:16:32 UTC 2015)
    Current LSP Info:
        Instance: 2, Signaling Area: PCE controlled
        Uptime: 00:00:24 (since Sat Jul 18 01:16:32 UTC 2015)
        Outgoing Interface: GigabitEthernet0/0/0/0.302, Outgoing Label: 24020
        Router-IDs: local      13.0.0.2
                    downstream 13.0.0.3
        Soft Preemption: None
        SRLGs: not collected
        Path Info:
        Outgoing:
            Explicit Route:
            Strict, 13.2.3.1
            Strict, 13.3.4.1
            Strict, 13.0.0.4

        Record Route: Empty
        Tspec: avg rate=0 kbits, burst=1000 bytes, peak rate=0 kbits
        Session Attributes: Local Prot: Not Set, Node Prot: Not Set, BW Prot: Not Set
                            Soft Preemption Desired: Not Set
        Resv Info:
        Record Route:
            IPv4 13.2.3.1, flags 0x0
            IPv4 13.3.4.1, flags 0x0
        Fspec: avg rate=0 kbits, burst=1000 bytes, peak rate=0 kbits
    Displayed 1 (of 3) heads, 0 (of 4) midpoints, 0 (of 0) tails
    Displayed 1 up, 0 down, 0 recovering, 0 recovered heads
    RP/0/0/CPU0:xr-13-02#

```

* this is what looks like if controller IS NOT available. The path will only change if the path that previously received from external controller is no longer valid.

```
    RP/0/0/CPU0:xr-13-02#show mpls traffic-eng tunnels name tunnel-te3 detail
    Sat Jul 18 01:34:49.923 UTC


    Name: tunnel-te3  Destination: 13.0.0.4  Ifhandle:0x680
    Signalled-Name: xr-13-02_t3
    Status:
        Admin:    up Oper:   up   Path:  valid   Signalling: connected

        path option 20,  type dynamic  (Basis for Setup, path weight 30)
        Last Signalled Error : Sat Jul 18 01:34:45 2015
        Info: [3] PathErr(24,5)-(routing, no route to dest) at 13.2.3.1
        path option 10,  type dynamic pce
        G-PID: 0x0800 (derived from egress interface properties)
        Bandwidth Requested: 0 kbps  CT0
        Creation Time: Sat Jul 18 01:16:31 2015 (00:18:19 ago)
    Config Parameters:
        Bandwidth:        0 kbps (CT0) Priority:  7  7 Affinity: 0x0/0xffff
        Metric Type: TE (default)
        Hop-limit: disabled
        Cost-limit: disabled
        AutoRoute: disabled  LockDown: disabled   Policy class: not set
        Forward class: 0 (default)
        Forwarding-Adjacency: disabled
        Loadshare:          0 equal loadshares
        Auto-bw: disabled
        Fast Reroute: Disabled, Protection Desired: None
        Path Protection: Not Enabled
        BFD Fast Detection: Disabled
        Reoptimization after affinity failure: Enabled
        Soft Preemption: Disabled
    SNMP Index: 15
    History:
        Tunnel has been up for: 00:00:05 (since Sat Jul 18 01:34:45 UTC 2015)
        Current LSP:
        Uptime: 00:00:05 (since Sat Jul 18 01:34:45 UTC 2015)
        Prior LSP:
        ID: 3 Path Option: 20
        Removal Trigger: path error
    Current LSP Info:
        Instance: 4, Signaling Area: IS-IS DEFAULT level-2
        Uptime: 00:00:05 (since Sat Jul 18 01:34:45 UTC 2015)
        Outgoing Interface: GigabitEthernet0/0/0/0.302, Outgoing Label: 24020
        Router-IDs: local      13.0.0.2
                    downstream 13.0.0.3
        Soft Preemption: None
        SRLGs: not collected
        Path Info:
        Outgoing:
            Explicit Route:
            Strict, 13.2.3.1
            Strict, 13.3.5.1
            Strict, 13.4.5.0
            Strict, 13.0.0.4

        Record Route: Empty
        Tspec: avg rate=0 kbits, burst=1000 bytes, peak rate=0 kbits
        Session Attributes: Local Prot: Not Set, Node Prot: Not Set, BW Prot: Not Set
                            Soft Preemption Desired: Not Set
        Resv Info:
        Record Route:
            IPv4 13.2.3.1, flags 0x0
            IPv4 13.3.5.1, flags 0x0
            IPv4 13.4.5.0, flags 0x0
        Fspec: avg rate=0 kbits, burst=1000 bytes, peak rate=0 kbits
    Displayed 1 (of 3) heads, 0 (of 3) midpoints, 0 (of 0) tails
    Displayed 1 up, 0 down, 0 recovering, 0 recovered heads
    RP/0/0/CPU0:xr-13-02#
```


### PCE Initiated LSP

* The following LSP is created from external controller. Notice that IOS-XR normalizes the tunnel name and keep the actual tunnel name as Signalled Name. 

```
RP/0/0/CPU0:xr-13-02#show mpls traffic-eng tunnels name tunnel-te1000 detail
Sat Jul 18 01:21:30.667 UTC


Name: tunnel-te1000  Destination: 13.0.0.4  Ifhandle:0x780 (auto-tunnel pcc)
  Signalled-Name: xr2-test
  Status:
    Admin:    up Oper:   up   Path:  valid   Signalling: connected

    path option 10, (verbatim) type explicit (autopcc_te1000) (Basis for Setup, path weight 0)
      Protected-by PO index: 20
    G-PID: 0x0800 (derived from egress interface properties)
    Bandwidth Requested: 0 kbps  CT0
    Creation Time: Sat Jul 18 01:21:05 2015 (00:00:25 ago)
  Config Parameters:
    Bandwidth:        0 kbps (CT0) Priority:  7  7 Affinity: 0x0/0xffff
    Metric Type: TE (default)
    Hop-limit: disabled
    Cost-limit: disabled
    AutoRoute: disabled  LockDown: disabled   Policy class: not set
    Forward class: 0 (default)
    Forwarding-Adjacency: disabled
    Loadshare:          0 equal loadshares
    Auto-bw: disabled
    Fast Reroute: Disabled, Protection Desired: None
    Path Protection: Not Enabled
    BFD Fast Detection: Disabled
    Reoptimization after affinity failure: Enabled
    Soft Preemption: Disabled
  Auto PCC:
    Symbolic name: xr2-test
    PCEP ID: 1001
    Delegated to: 1.1.1.178
    Created by: 1.1.1.178
  SNMP Index: 16
  History:
    Tunnel has been up for: 00:00:25 (since Sat Jul 18 01:21:05 UTC 2015)
    Current LSP:
      Uptime: 00:00:25 (since Sat Jul 18 01:21:05 UTC 2015)
  Current LSP Info:
    Instance: 2, Signaling Area: PCE controlled
    Uptime: 00:00:25 (since Sat Jul 18 01:21:05 UTC 2015)
    Outgoing Interface: GigabitEthernet0/0/0/0.302, Outgoing Label: 24022
    Router-IDs: local      13.0.0.2
                downstream 13.0.0.3
    Soft Preemption: None
    SRLGs: not collected
    Path Info:
      Outgoing:
        Explicit Route:
          Strict, 13.2.3.1
          Strict, 13.3.4.1

      Record Route: Disabled
      Tspec: avg rate=0 kbits, burst=1000 bytes, peak rate=0 kbits
      Session Attributes: Local Prot: Not Set, Node Prot: Not Set, BW Prot: Not Set
                          Soft Preemption Desired: Not Set
    Resv Info: None
      Record Route: Disabled
      Fspec: avg rate=0 kbits, burst=1000 bytes, peak rate=0 kbits
Displayed 1 (of 4) heads, 0 (of 4) midpoints, 0 (of 0) tails
Displayed 1 up, 0 down, 0 recovering, 0 recovered heads
RP/0/0/CPU0:xr-13-02#
```


## BGP-LS

```
router isis DEFAULT
 is-type level-2-only
 net 49.1300.0130.0000.0001.00
 distribute bgp-ls
 address-family ipv4 unicast
  metric-style wide
  mpls traffic-eng level-2-only
  mpls traffic-eng router-id Loopback0
 !
 interface Loopback0
  passive
  address-family ipv4 unicast
  !
 !
 interface GigabitEthernet0/0/0/0.301
  point-to-point
  address-family ipv4 unicast
  !
 !
 interface GigabitEthernet0/0/0/0.304
  point-to-point
  address-family ipv4 unicast
   metric 1000
  !
 !
 interface GigabitEthernet0/0/0/0.308
  point-to-point
  address-family ipv4 unicast
  !
 !
 interface GigabitEthernet0/0/0/1
  address-family ipv4 unicast
  !
 !
!
router bgp 11
 address-family link-state link-state
 !
 neighbor 172.16.17.2
  remote-as 11
  local address 172.16.17.101
  session-open-mode both
  address-family link-state link-state
  !
 !
 neighbor 172.16.17.100
  remote-as 11
  local address 172.16.17.101
  session-open-mode both
  address-family link-state link-state
  !
 !
!
mpls traffic-eng
 interface GigabitEthernet0/0/0/1
 !
 interface GigabitEthernet0/0/0/0.301
 !
 interface GigabitEthernet0/0/0/0.304
 !
 interface GigabitEthernet0/0/0/0.308
 !
 pce
  peer source ipv4 1.1.1.101
  peer ipv4 1.1.1.1
   precedence 10
  !
  peer ipv4 1.1.1.178
   precedence 20
  !
  stateful-client
   instantiation
   report
  !
  speaker-entity-id xr1
 !
 auto-tunnel pcc
  tunnel-id min 1000 max 5000
 !
!
```
