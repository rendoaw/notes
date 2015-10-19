
## Problem

by default JunOS will block the traffic going to ::ffff:a.b.c.d ipv4 mapped IPv6 address. It is applied for both sending, terminating and transit traffic.
reference: https://www.juniper.net/documentation/en_US/junos14.2/topics/task/configuration/ipv6-ipv4-mapped-addresses-processing-enabling.html

example:

```
rwibawa@vmx-13-12# run ping ::ffff:76.5.255.11 source 2400:67:176:255::2
PING6(56=40+8+8 bytes) ::ffff:67.176.0.25 --> ::ffff:76.5.255.11
^C
--- ::ffff:76.5.255.11 ping6 statistics ---
3 packets transmitted, 0 packets received, 100% packet loss
```

### Solution
* configure "allow-v4mapped-packets" on all router from the source to the destination

```

[edit]
rwibawa@vmx-13-12# set system allow-v4mapped-packets

[edit]
rwibawa@vmx-13-12# commit
commit complete

[edit]
rwibawa@vmx-13-12# run ping ::ffff:76.5.255.11 source 2400:67:176:255::2
PING6(56=40+8+8 bytes) ::ffff:67.176.0.25 --> ::ffff:76.5.255.11
16 bytes from ::ffff:76.5.255.11, icmp_seq=0 hlim=63 time=5.483 ms
16 bytes from ::ffff:76.5.255.11, icmp_seq=1 hlim=63 time=3.389 ms
^C
--- ::ffff:76.5.255.11 ping6 statistics ---
2 packets transmitted, 2 packets received, 0% packet loss
round-trip min/avg/max/std-dev = 3.389/4.436/5.483/1.047 ms

```

* if you are using 6PE, we need to enable this knob on each router that actually processing IPv6 packet. No need to enable the knob on the LSR that doing lookup based on the label. You need to do the same as example above on all intermediate router.
