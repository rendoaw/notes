
# ubuntu

```
modprobe 8021q
apt-get install vlan
vconfig add eth1 500
ifconfig eth1 up
ifconfig eth1.500 inet 50.11.12.4 netmask 255.255.255.0 up
```
