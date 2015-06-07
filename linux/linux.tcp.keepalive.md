```
echo 3 > /proc/sys/net/ipv4/tcp_keepalive_probes
echo 10 > /proc/sys/net/ipv4/tcp_keepalive_intvl
echo 60 > /proc/sys/net/ipv4/tcp_keepalive_time

cat /proc/sys/net/ipv4/tcp_keepalive_probes
cat /proc/sys/net/ipv4/tcp_keepalive_intvl
cat /proc/sys/net/ipv4/tcp_keepalive_time

sysctl -w net.ipv4.tcp_keepalive_time=60 net.ipv4.tcp_keepalive_probes=3 net.ipv4.tcp_keepalive_intvl=10
```