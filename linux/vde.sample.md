
connect local interface eth2 to remote vde switch @192.168.1.100 over ssh
```
/usr/bin/vde_switch -unix /tmp/vde2 -t tap2  -d --dirmode 777 --mode 666 --mgmtmode 666 -T -c mgmt0 -n 4096
dpipe vde_plug /tmp/vde2 = ssh 192.168.1.100 /tmp/vde2

brctl addbr br101
brctl addif br101 eth2
brctl addif br101 tap2
ifconfig br101 up

sysctl -w net.ipv4.conf.all.forwarding=1
```








