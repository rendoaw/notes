
## Setup

Follow instruction from: https://github.com/facebook/openr

## config 

```
root@linux-91:/home/ubuntu# cat /etc/sysconfig/openr
DRYRUN=false
REDISTRIBUTE_IFACES=lo
IFACE_PREFIXES=eth,lo,ens,veth,br,cali
VERBOSITY=1
PREFIXES="2001:db8::/32"
ENABLE_V4=true
ENABLE_HEALTH_CHECKER=true
ENABLE_PREFIX_ALLOC=true
SEED_PREFIX="2001:db8::/64"
ALLOC_PREFIX_LEN=80
SET_LOOPBACK_ADDR=true
OVERRIDE_LOOPBACK_ADDR=true
ENABLE_NETLINK_FIB_HANDLER=true
```

## Summary
hostname as node-id
only advertise loopback by default
static prefix must be manually injected via controller, e.g: breeze


## Output

### linux

```
root@linux-91:/home/ubuntu# ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet 10.0.0.91/32 scope global lo
       valid_lft forever preferred_lft forever
    inet6 2001:db8::5de7:0:0:1/128 scope global
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: ens4: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 52:55:01:00:91:00 brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.91/24 brd 192.168.1.255 scope global ens4
       valid_lft forever preferred_lft forever
    inet 169.254.1.91/24 scope global ens4
       valid_lft forever preferred_lft forever
    inet6 fe80::5055:1ff:fe00:9100/64 scope link
       valid_lft forever preferred_lft forever
3: ens5: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 52:55:01:00:91:01 brd ff:ff:ff:ff:ff:ff
    inet 172.19.1.1/24 scope global ens5
       valid_lft forever preferred_lft forever
    inet6 fe80::5055:1ff:fe00:9101/64 scope link
       valid_lft forever preferred_lft forever
537: br2: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN group default qlen 1000
    link/ether 00:00:00:00:00:00 brd ff:ff:ff:ff:ff:ff
    inet 10.191.1.1/24 scope global br2
       valid_lft forever preferred_lft forever
    inet6 fe80::68b2:d1ff:fefb:ca8d/64 scope link
       valid_lft forever preferred_lft forever
549: veth8e17a78@if548: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master docker0 state UP group default
    link/ether 02:de:53:71:ab:c8 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet6 fe80::de:53ff:fe71:abc8/64 scope link
       valid_lft forever preferred_lft forever
551: veth780aa59@if550: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master docker0 state UP group default
    link/ether ee:ac:ec:3e:55:8c brd ff:ff:ff:ff:ff:ff link-netnsid 1
    inet6 fe80::ecac:ecff:fe3e:558c/64 scope link
       valid_lft forever preferred_lft forever
root@linux-91:/home/ubuntu#
```

```
root@linux-91:/home/ubuntu# ip r
default via 192.168.1.1 dev ens4
10.0.0.92 via 192.168.1.92 dev ens4  proto 99
10.191.1.0/24 dev br2  proto kernel  scope link  src 10.191.1.1 linkdown
blackhole 10.191.101.128/26  proto bird
169.254.1.0/24 dev ens4  proto kernel  scope link  src 169.254.1.91
172.17.0.0/16 dev docker0  proto kernel  scope link  src 172.17.0.1
172.19.1.0/24 dev ens5  proto kernel  scope link  src 172.19.1.1
192.168.1.0/24 dev ens4  proto kernel  scope link  src 192.168.1.91
root@linux-91:/home/ubuntu# ip -6 r
unreachable 2001:db8::5de7:0:0:1 dev lo  proto kernel  metric 256  error -101 pref medium
2001:db8::61b9:0:0:1 via fe80::5055:1ff:fe00:9200 dev ens4  proto 99  metric 1024  pref medium
2001:db8:0:0:61b9::/80 via fe80::5055:1ff:fe00:9200 dev ens4  proto 99  metric 1024  pref medium
fd99:168:92::/48 via fe80::5055:1ff:fe00:9200 dev ens4  proto 99  metric 1024  pref medium
fe80::/64 dev ens4  proto kernel  metric 256  pref medium
fe80::/64 dev ens5  proto kernel  metric 256  pref medium
fe80::/64 dev docker0  proto kernel  metric 256  pref medium
fe80::/64 dev br2  proto kernel  metric 256 linkdown  pref medium
fe80::/64 dev veth8e17a78  proto kernel  metric 256  pref medium
fe80::/64 dev veth780aa59  proto kernel  metric 256  pref medium
```

```
root@linux-91:/home/ubuntu# breeze decision routes

> 10.0.0.92/32
via 192.168.1.92@ens4 metric 5

> 2001:db8:0:0:61b9::/80
via fe80::5055:1ff:fe00:9200@ens4 metric 5

> 2001:db8::61b9:0:0:1/128
via fe80::5055:1ff:fe00:9200@ens4 metric 5

> fd99:168:92::/48
via fe80::5055:1ff:fe00:9200@ens4 metric 5


root@linux-91:/home/ubuntu# breeze fib list

> 10.0.0.92/32
via 192.168.1.92@ens4

> 2001:db8:0:0:61b9::/80
via fe80::5055:1ff:fe00:9200@ens4

> 2001:db8::61b9:0:0:1/128
via fe80::5055:1ff:fe00:9200@ens4

> fd99:168:92::/48
via fe80::5055:1ff:fe00:9200@ens4
```



```
root@linux-92:~# ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet 10.0.0.92/32 scope global lo
       valid_lft forever preferred_lft forever
    inet6 2001:db8::61b9:0:0:1/128 scope global
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: ens4: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 52:55:01:00:92:00 brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.92/24 brd 192.168.1.255 scope global ens4
       valid_lft forever preferred_lft forever
    inet 169.254.1.92/24 scope global ens4
       valid_lft forever preferred_lft forever
    inet6 fe80::5055:1ff:fe00:9200/64 scope link
       valid_lft forever preferred_lft forever
3: ens5: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default qlen 1000
    link/ether 52:55:01:00:92:01 brd ff:ff:ff:ff:ff:ff
4: ens6: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default qlen 1000
    link/ether 52:55:01:00:92:02 brd ff:ff:ff:ff:ff:ff
5: ens7: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default qlen 1000
    link/ether 52:55:01:00:92:03 brd ff:ff:ff:ff:ff:ff
6: ens8: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default qlen 1000
    link/ether 52:55:01:00:92:04 brd ff:ff:ff:ff:ff:ff
7: ens9: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default qlen 1000
    link/ether 52:55:01:00:92:05 brd ff:ff:ff:ff:ff:ff
8: ens10: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default qlen 1000
    link/ether 52:55:01:00:92:06 brd ff:ff:ff:ff:ff:ff
9: ens11: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default qlen 1000
    link/ether 52:55:01:00:92:07 brd ff:ff:ff:ff:ff:ff
10: ens12: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default qlen 1000
    link/ether 52:55:01:00:92:08 brd ff:ff:ff:ff:ff:ff
11: ens13: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default qlen 1000
    link/ether 52:55:01:00:92:09 brd ff:ff:ff:ff:ff:ff
12: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN group default
    link/ether 02:42:5b:81:e0:3c brd ff:ff:ff:ff:ff:ff
    inet 172.17.0.1/16 scope global docker0
       valid_lft forever preferred_lft forever
14: veth_11a@if13: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
    link/ether 02:de:00:16:41:9c brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 172.19.21.1/24 scope global veth_11a
       valid_lft forever preferred_lft forever
    inet6 fd99:168:92:1::1/64 scope global
       valid_lft forever preferred_lft forever
    inet6 fe80::de:ff:fe16:419c/64 scope link
       valid_lft forever preferred_lft forever
root@linux-92:~#
root@linux-92:~#
root@linux-92:~#
root@linux-92:~#
root@linux-92:~# ip r
default via 192.168.1.1 dev ens4
10.0.0.91 via 192.168.1.91 dev ens4  proto 99
10.191.1.0/24 via 192.168.1.91 dev ens4  proto 99
169.254.1.0/24 dev ens4  proto kernel  scope link  src 169.254.1.92
172.17.0.0/16 dev docker0  proto kernel  scope link  src 172.17.0.1 linkdown
172.19.21.0/24 dev veth_11a  proto kernel  scope link  src 172.19.21.1
192.168.1.0/24 dev ens4  proto kernel  scope link  src 192.168.1.92
root@linux-92:~#
root@linux-92:~#
root@linux-92:~# ip -6 r
2001:db8::5de7:0:0:1 via fe80::5055:1ff:fe00:9100 dev ens4  proto 99  metric 1024  pref medium
2001:db8:0:0:5de7::/80 via fe80::5055:1ff:fe00:9100 dev ens4  proto 99  metric 1024  pref medium
unreachable 2001:db8::61b9:0:0:1 dev lo  proto kernel  metric 256  error -101 pref medium
fd99:168:92:1::/64 dev veth_11a  proto kernel  metric 256  pref medium
fe80::/64 dev ens4  proto kernel  metric 256  pref medium
fe80::/64 dev veth_11a  proto kernel  metric 256  pref medium
root@linux-92:~#
root@linux-92:~#
root@linux-92:~# breeze lm links

Interface    Status    Overloaded    Metric Override    ifIndex    Addresses
-----------  --------  ------------  -----------------  ---------  ------------------------
ens4         Up                                         2          192.168.1.92
                                                                   169.254.1.92
                                                                   fe80::5055:1ff:fe00:9200
lo           Up                                         1          127.0.0.1
                                                                   10.0.0.92
veth_11a     Up                                         14         172.19.21.1


root@linux-92:~# breeze prefixmgr advertise fd99:168:92::/48
Advertised 1 prefixes with type BREEZE
root@linux-92:~#
```



```
ip netns add ns11
ip link add veth_11a type veth peer name veth_11b
ip link set veth_11b netns ns11
ip netns exec ns11 ip a add 172.19.21.2/24 dev veth_11b
ip netns exec ns11 ip -6 a add fd99:168:92:1::2/64 dev veth_11b
ip netns exec ns11 ip link set dev veth_11b up
ip netns exec ns11 ip route add default via 172.19.21.1
ip netns exec ns11 ip -6 route add default via fd99:168:92:1::1
ip netns exec ns11 ip link set dev lo up

ip a add 172.19.21.1/24 dev veth_11a
ip -6 a add fd99:168:92:1::1/64 dev veth_11a
ip link set dev veth_11a up
```

```
root@linux-91:/home/ubuntu# traceroute6 fd99:168:92:1::2
traceroute to fd99:168:92:1::2 (fd99:168:92:1::2) from 2001:db8::5de7:0:0:1, 30 hops max, 24 byte packets
 1  2001:db8::61b9:0:0:1 (2001:db8::61b9:0:0:1)  0.4 ms  0.258 ms  0.231 ms
 2  fd99:168:92:1::2 (fd99:168:92:1::2)  0.425 ms  0.352 ms  0.231 ms
root@linux-91:/home/ubuntu#
```


```
I1120 02:36:42.071877 16034 NetlinkSystemHandler.cpp:178] Re-syncing Netlink DB
I1120 02:36:42.072667 16034 NetlinkSystemHandler.cpp:180] Completed re-syncing Netlink DB from Netlink Subscriber
I1120 02:36:44.997175 16075 LinkMonitor.cpp:297] LinkMonitor: Spark message received...
I1120 02:36:44.997421 16075 LinkMonitor.cpp:357] Metric value changed for neighbor linux-92 to 5
I1120 02:36:45.997601 16075 LinkMonitor.cpp:617] Link Monitor: throttle timer has expired, accumulated 0 peer addition requests
I1120 02:36:46.009270 16076 Decision.cpp:1163] Decision: processing 1 accumulated updates.
I1120 02:36:46.009696 16076 Decision.cpp:1187] Decision: computing new paths.
I1120 02:36:46.010396 16076 Decision.cpp:761] Decision::buildMultiPaths took 0ms.
I1120 02:36:46.011060 16077 Fib.cpp:144] Fib: publication received ...
I1120 02:36:46.011493 16077 Fib.cpp:371] Syncing latest routeDb with fib-agent ...
I1120 02:36:46.012552 16051 NetlinkFibHandler.cpp:170] Syncing FIB with provided routes. Client: OPENR
I1120 02:36:46.014243 16077 Fib.cpp:531] OpenR convergence performance. Duration=17
I1120 02:36:46.014274 16077 Fib.cpp:534]   node: linux-91, event: ADJ_DB_UPDATED, duration: 0ms, unix-timestamp: 1511145405997
I1120 02:36:46.014307 16077 Fib.cpp:534]   node: linux-91, event: DECISION_RECEIVED, duration: 2ms, unix-timestamp: 1511145405999
I1120 02:36:46.014335 16077 Fib.cpp:534]   node: linux-91, event: DECISION_DEBOUNCE, duration: 10ms, unix-timestamp: 1511145406009
I1120 02:36:46.014360 16077 Fib.cpp:534]   node: linux-91, event: DECISION_SPF, duration: 1ms, unix-timestamp: 1511145406010
I1120 02:36:46.014386 16077 Fib.cpp:534]   node: linux-91, event: FIB_ROUTE_DB_RECVD, duration: 1ms, unix-timestamp: 1511145406011
I1120 02:36:46.014439 16077 Fib.cpp:534]   node: linux-91, event: FIB_DEBOUNCE, duration: 0ms, unix-timestamp: 1511145406011
I1120 02:36:46.014467 16077 Fib.cpp:534]   node: linux-91, event: OPENR_FIB_ROUTES_PROGRAMMED, duration: 3ms, unix-timestamp: 1511145406014
I1120 02:36:47.233602 16075 LinkMonitor.cpp:472] InterfaceDb Sync is successful
I1120 02:36:52.197803 16044 KvStore.cpp:735] Sending full sync request to peer linux-92 using id linux-92::TCP::CMD
I1120 02:36:52.199282 16044 KvStore.cpp:981] Sync response received from linux-92::TCP::CMD with 10 key value pairs
I1120 02:36:57.237124 16075 LinkMonitor.cpp:472] InterfaceDb Sync is successful
I1120 02:37:02.076499 16034 NetlinkSystemHandler.cpp:178] Re-syncing Netlink DB
I1120 02:37:02.077419 16034 NetlinkSystemHandler.cpp:180] Completed re-syncing Netlink DB from Netlink Subscriber
I1120 02:37:07.241330 16075 LinkMonitor.cpp:472] InterfaceDb Sync is successful
I1120 02:37:17.244269 16075 LinkMonitor.cpp:472] InterfaceDb Sync is successful
I1120 02:37:22.080621 16034 NetlinkSystemHandler.cpp:178] Re-syncing Netlink DB
I1120 02:37:22.081759 16034 NetlinkSystemHandler.cpp:180] Completed re-syncing Netlink DB from Netlink Subscriber
I1120 02:37:27.247716 16075 LinkMonitor.cpp:472] InterfaceDb Sync is successful
I1120 02:37:37.250882 16075 LinkMonitor.cpp:472] InterfaceDb Sync is successful
I1120 02:37:40.201248 16044 KvStore.cpp:735] Sending full sync request to peer linux-92 using id linux-92::TCP::CMD
I1120 02:37:40.202425 16044 KvStore.cpp:981] Sync response received from linux-92::TCP::CMD with 10 key value pairs
I1120 02:37:42.081481 16034 NetlinkSystemHandler.cpp:178] Re-syncing Netlink DB
I1120 02:37:42.082267 16034 NetlinkSystemHandler.cpp:180] Completed re-syncing Netlink DB from Netlink Subscriber
I1120 02:37:47.252861 16066 ThreadManager.tcc:374] ThreadManager::add called with numa == true, but not a NumaThreadManager
I1120 02:37:47.254672 16075 LinkMonitor.cpp:472] InterfaceDb Sync is successful
I1120 02:37:57.258896 16075 LinkMonitor.cpp:472] InterfaceDb Sync is successful
I1120 02:38:01.628082 16076 Decision.cpp:1163] Decision: processing 1 accumulated updates.
I1120 02:38:01.628291 16076 Decision.cpp:1187] Decision: computing new paths.
I1120 02:38:01.628695 16076 Decision.cpp:761] Decision::buildMultiPaths took 0ms.
I1120 02:38:01.629214 16077 Fib.cpp:144] Fib: publication received ...
I1120 02:38:01.629426 16077 Fib.cpp:371] Syncing latest routeDb with fib-agent ...
I1120 02:38:01.629998 16051 NetlinkFibHandler.cpp:170] Syncing FIB with provided routes. Client: OPENR
I1120 02:38:01.631062 16077 Fib.cpp:531] OpenR convergence performance. Duration=20
I1120 02:38:01.631083 16077 Fib.cpp:534]   node: linux-92, event: ADJ_DB_UPDATED, duration: 0ms, unix-timestamp: 1511145481611
I1120 02:38:01.631090 16077 Fib.cpp:534]   node: linux-91, event: DECISION_RECEIVED, duration: 7ms, unix-timestamp: 1511145481618
I1120 02:38:01.631094 16077 Fib.cpp:534]   node: linux-91, event: DECISION_DEBOUNCE, duration: 10ms, unix-timestamp: 1511145481628
I1120 02:38:01.631098 16077 Fib.cpp:534]   node: linux-91, event: DECISION_SPF, duration: 0ms, unix-timestamp: 1511145481628
I1120 02:38:01.631103 16077 Fib.cpp:534]   node: linux-91, event: FIB_ROUTE_DB_RECVD, duration: 1ms, unix-timestamp: 1511145481629
I1120 02:38:01.631108 16077 Fib.cpp:534]   node: linux-91, event: FIB_DEBOUNCE, duration: 0ms, unix-timestamp: 1511145481629
I1120 02:38:01.631112 16077 Fib.cpp:534]   node: linux-91, event: OPENR_FIB_ROUTES_PROGRAMMED, duration: 2ms, unix-timestamp: 1511145481631
I1120 02:38:02.082427 16034 NetlinkSystemHandler.cpp:178] Re-syncing Netlink DB
I1120 02:38:02.083264 16034 NetlinkSystemHandler.cpp:180] Completed re-syncing Netlink DB from Netlink Subscriber
I1120 02:38:07.263193 16075 LinkMonitor.cpp:472] InterfaceDb Sync is successful
I1120 02:38:14.438765 16075 LinkMonitor.cpp:297] LinkMonitor: Spark message received...
I1120 02:38:14.439009 16075 LinkMonitor.cpp:357] Metric value changed for neighbor linux-92 to 5
I1120 02:38:15.439275 16075 LinkMonitor.cpp:617] Link Monitor: throttle timer has expired, accumulated 0 peer addition requests
I1120 02:38:15.449618 16076 Decision.cpp:1163] Decision: processing 1 accumulated updates.
I1120 02:38:15.449749 16076 Decision.cpp:1187] Decision: computing new paths.
I1120 02:38:15.450202 16076 Decision.cpp:761] Decision::buildMultiPaths took 0ms.
I1120 02:38:15.450620 16077 Fib.cpp:144] Fib: publication received ...
I1120 02:38:15.450821 16077 Fib.cpp:371] Syncing latest routeDb with fib-agent ...
I1120 02:38:15.451531 16051 NetlinkFibHandler.cpp:170] Syncing FIB with provided routes. Client: OPENR
I1120 02:38:15.452546 16077 Fib.cpp:531] OpenR convergence performance. Duration=13
I1120 02:38:15.452572 16077 Fib.cpp:534]   node: linux-91, event: ADJ_DB_UPDATED, duration: 0ms, unix-timestamp: 1511145495439
I1120 02:38:15.452600 16077 Fib.cpp:534]   node: linux-91, event: DECISION_RECEIVED, duration: 1ms, unix-timestamp: 1511145495440
I1120 02:38:15.452621 16077 Fib.cpp:534]   node: linux-91, event: DECISION_DEBOUNCE, duration: 9ms, unix-timestamp: 1511145495449
I1120 02:38:15.452639 16077 Fib.cpp:534]   node: linux-91, event: DECISION_SPF, duration: 1ms, unix-timestamp: 1511145495450
I1120 02:38:15.452656 16077 Fib.cpp:534]   node: linux-91, event: FIB_ROUTE_DB_RECVD, duration: 0ms, unix-timestamp: 1511145495450
I1120 02:38:15.452674 16077 Fib.cpp:534]   node: linux-91, event: FIB_DEBOUNCE, duration: 0ms, unix-timestamp: 1511145495450
I1120 02:38:15.452692 16077 Fib.cpp:534]   node: linux-91, event: OPENR_FIB_ROUTES_PROGRAMMED, duration: 2ms, unix-timestamp: 1511145495452
I1120 02:38:17.265949 16075 LinkMonitor.cpp:472] InterfaceDb Sync is successful


I1120 02:38:22.086410 16034 NetlinkSystemHandler.cpp:178] Re-syncing Netlink DB
I1120 02:38:22.087219 16034 NetlinkSystemHandler.cpp:180] Completed re-syncing Netlink DB from Netlink Subscriber
```
