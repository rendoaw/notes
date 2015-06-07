Sample config to establish GRE tunnel between Nortel ARN router series, Cisco 7500 series, and FreeBSD. 

Nortel ARN router configuration
```
tunnels
gre name to-cisco local-address 172.17.2.166
ip address 10.101.102.1 mask 255.255.255.252
back
remote-endpoint name cisco-1 address 172.24.232.65
back
back
gre name to-freebsd local-address 172.17.2.166
ip address 10.100.102.1 mask 255.255.255.252
back
remote-endpoint name freebsd-1 address 172.20.1.73
back
back
back
```


Cisco Configuration
```
interface Tunnel3
ip address 10.101.102.2 255.255.255.252
tunnel destination 172.17.2.166
tunnel mode gre ip
```


FreeBSD configuration
```
ifconfig gre0 create
ifconfig gre0 inet 10.100.102.2 10.100.102.1 netmask 255.255.255.252
ifconfig gre0 tunnel 172.20.1.73 172.17.2.166
```
