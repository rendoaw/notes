Sample cases:
- source traffic from 10.10.1.0/24 will be translated to 202.202.202.2/28
- source traffic from 10.10.2.0/24 will be translated to 202.202.202.3/28
- source traffic from 10.10.1.0/24 to 202.0.0.0/8 will be translated to 202.202.202.4/28
- all http traffic will be directed to http proxy @ 10.10.10.10 port 8080
- one-to-one mapping (bidirectional nat) traffic from 10.10.1.1/24 to any replaced with 202.202.202.5/28
- all traffic to 202.202.202.2 port 81 will be redirected to 10.10.1.2 port 80

assume external interface is fxp0 and internal interface is fxp1 and the current ip address of external interface is 202.202.202.2/28

first put the ip address in fxp0 as alias ip:
```
ifconfig fxp0 inet 202.202.202.3 netmask 255.255.255.255 alias
ifconfig fxp0 inet 202.202.202.4 netmask 255.255.255.255 alias
ifconfig fxp0 inet 202.202.202.5 netmask 255.255.255.255 alias
```

then, the rules:
```
bimap fxp0 10.10.1.1/32 -> 202.202.202.5/32

#SNAT
map fxp0 from 10.10.1.0/24 to 202.0.0.0/8 -> 202.202.202.4/32 portmap tcp/udp auto
map fxp0 10.10.1.0/24 -> 202.202.202.2/32 portmap tcp/udp auto
map fxp0 10.10.2.0/24 -> 202.202.202.3/32 portmap tcp/udp auto

#DNAT
rdr fxp1 0/0 port 80 -> 10.10.10.10 port 8080 tcp
rdr fxp0 202.202.202.2/32 port 81 -> 10.10.1.2 port 80 tcp
```

