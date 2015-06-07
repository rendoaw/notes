Nortel ASN
```
ip
arp
back
static-route address 0.0.0.0 mask 0.0.0.0 next-hop-address 219.21.2.165
back

…deleted…

bgp router-id 219.21.2.166
local-as 65521
multi-hop enabled
peer local 219.21.2.166 remote 219.19.232.65 as 33333
next-hop-self enabled
back
announce polname dist-static
action announce
match
protocol-source static
back
modify
back
back
back
```


Cisco IOS
```
router bgp 33333
neighbor 219.21.2.166 remote-as 65521
neighbor 219.21.2.166 description BGP peer to Backup Upstream
neighbor 219.21.2.166 ebgp-multihop 255
neighbor 219.21.2.166 soft-reconfiguration inbound
neighbor 219.21.2.166 route-map accept-default-only in
neighbor 219.21.2.166 route-map NONE out
neighbor 219.20.127.4 remote-as 22222
neighbor 219.20.127.4 description BGP peer to ISP
neighbor 219.20.127.4 ebgp-multihop 255
neighbor 219.20.127.4 remove-private-AS
neighbor 219.20.127.4 soft-reconfiguration inbound
neighbor 219.20.127.4 route-map accept-default-only-preferred in
neighbor 219.20.127.4 route-map EXPORT-TO-ISP out

access-list 199 permit ip host 0.0.0.0 host 0.0.0.0
access-list 199 deny ip any any

route-map accept-default-only permit 10
match ip address 199
set ip next-hop 10.101.102.1
set local-preference 50
!
route-map accept-default-only-preferred permit 10
match ip address 199
set local-preference 200
!
```

