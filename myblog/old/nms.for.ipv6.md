As most of you know, last week, (June 8 to be precise) is the world IPv6 day, was a global-scale test flight of IPv6 sponsored by the Internet Society.

Personally i do expect that IPv6 network has the same quality (or better) compared with IPv4 network that we have now and to achieve this we need a similar management tools to monitor IPv6 network. This time, i would like to talk again about some part of IPv6 NMS, the similar content that i presented during the Telkom Indonesia WIDEX2011 event.

I want to highlight some issues related with NMS for IPv6 especially for online monitoring system because without online monitoring we don't know how many and what kind of IPv6 traffic that we have. 

1. IPv6 address representation
In contrast with other network based software which don't really care about layer 3 stack, NMS software is very impacted with the introduction of IPv6. IPv4 has a single standard format, 4 column delimited by dot and each column contains numeric value within 0-255. The case is very different with IPv6. IPv6 has multiple representation as stated in RFC5952. Some of the examples are:
```
Normal form:
– ABCD:EF01:2345:6789:ABCD:EF01:2345:6789
Grouping of 16 bits of zeros.
- 2001:DB8::8:800:200C:417A = 2001:DB8:0:0:8:800:200C:417A a unicast address
- FF01::101 = FF01:0:0:0:0:0:0:101 a multicast address
- ::1 = 0:0:0:0:0:0:0:1 the loopback address
- :: = 0:0:0:0:0:0:0:0 the unspecified address
Mixed environment of IPv4 and IPv6 nodes:
– 0:0:0:0:0:0:13.1.68.3 = ::13.1.68.3
– 0:0:0:0:0:FFFF:129.144.52.38 = ::FFFF:129.144.52.38
Text Representation of Address Prefixes:
– 12AB:0000:0000:CD30:0000:0000:0000:0000/60
– 12AB::CD30:0:0:0:0/60
```

2. SNMP for IPv6
Current SNMP MIB for IPv4 monitoring can not handle IPv6 address to be put as OID index. The initial solution was creating new set of MIB to cover IPv6 statistic as listed below:
IPV6-MIB, RFC2465
IPV6-ICMP-MIB, RFC2466
IPV6-TCP-MIB, RFC2452
IPV6-UDP-MIB, RFC2454
but, later, this approach was considered as complicated because we need to maintain 2 sets of MIB. The new solution is by updating the IPv4 MIB to have new indexes for IPv6 information. The new solution is explained in the below RFC:
Updated IP-MIB, RFC4293, Obsoletes: RFC2011, RFC2465, RFC2466
Updated TCP-MIB, RFC4022, Obsoletes: RFC2452, RFC2012
Updated UDP MIB, RFC4113, Obsoletes: RFC2454, RFC2013
Updated IP Forwarding MIB, RFC4292, Obsoletes: RFC2096
The problem is not finished here because seems that different vendor has different implementation. Some router vendors still use the initial solution and some others are migrating to the new solution. I believe we  need more time to wait until all router vendor implement the same standard.
Here are some examples how IPv6 MIB looks like:
```
.1.3.6.1.2.1.55.1.8.1.2.16.37.0.0.0.0.0.0.0.0.0.0.0.0.0.1.0 = INTEGER: 128 bits
37(10) = 25(16), 1(10) = 1(10)
means:
interface index = 16
ipv6AddrPfxLength (.1.3.6.1.2.1.55.1.8.1.2) = 128 bits --> most likely loopback interface

.1.3.6.1.2.1.55.1.12.1.3.183.37.0.0.0.0.25.0.0.0.0.0.0.0.0.0.1 = INTEGER: local(4)
37(10) = 25(16), 1(10) = 1(10), 25(10) = 19(16)
means:
interface index = 183
IPv6 addr = 2500:0000:0019:0000:0000:0000:0000:0001 or 2500:0:19::1
ipv6NetToMediaType (1.3.6.1.2.1.55.1.12.1.3) = local interface
```


3. Netflow
Netflow is still the popular way to know the real packet passing our router. Similar like SNMP, current netflow v5 implementation has a fixed fields which can not contains IPv6 address format. At this moment, netflow v9 is the only version can support IPv6 data, thanks to netflow v9 dynamic packet format. Good news, this afternoon, my friend just upgraded one of his Cisco 7600 with new IOS that support IPv6 unicast netflow reporting, so i hope i can get  IPv6 netflow from real internet traffic soon :)


to be continued ....

