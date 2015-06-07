references:
http://www.greenie.net/ipv6/openvpn.html
http://silmor.de/64
http://openvpn.net/index.php/open-source/faq/77-server/287-is-ipv6-support-plannedin-the-works.html
http://techtots.blogspot.com/2010/01/openvpn-with-pammysql-usernamepassword.html

OpenVPN 2.0 only support IPv6 in TAP mode. It is simply because TAP mode acts as virtual ethernet, so any layer 3 protocol should run over it without any problem
On OpenVPN 2.2RC, Point-to-point IPv6 tunnels are supported on OSes which have IPv6 TUN driver support (this includes Linux and the BSDs).
Full IPv6 support is already available in "allmerged" branch in Git, and will be included in OpenVPN 2.3 release
TAP mode is the simplest way to setup openvpn for IPv6 but it uses a single /64 network for single client. Basically only 2 address are used and the remaining are "wasted". Since i have only a single /64 subnet and i want to provide tunnel for some people, then this is not an option for me.
TUN mode for IPv6 required OpenVPN 2.3 for both server and client but TUN mode for IPv6 behaves like --topology subnet for ipv4
other limitations can be found here


Telkom OpenVPN tunnel mentioned in my previous blog entry is using TAP mode, but the one that i want to setup here is TUN mode, mainly because of i only have a single /64 subnet for every tunnel user.

I downloaded the package from http://build.openvpn.net/downloads/ since both my server and my laptop are using Ubuntu.
I also found out that i can't have ipv6 tunnel only, and i still need to setup ipv4 tunnel, so i just add "server x.x.x.x y.y.y.y" statement without any push config.

Here are the complete server and client config, at this moment it is tested for linux client, and i will test the windows client using Gert Döring patch later.

```
Server config:
local a.b.c.d 
port xx 
proto tcp 
dev tun  
ca /etc/openvpn/easy-rsa/keys/ca.crt 
cert /etc/openvpn/easy-rsa/keys/server.crt 
key /etc/openvpn/easy-rsa/keys/server.key  
dh /etc/openvpn/easy-rsa/keys/dh1024.pem  

server-ipv6 abcd:abc:1f05:1e02::/64 
server 10.99.254.0 255.255.255.0 
tun-ipv6  push "route-ipv6 ::/0"  
client-config-dir /etc/openvpn/static-config 
ifconfig-pool-persist /var/log/openvpn/openvpn.tcp.if  
client-to-client 
;duplicate-cn 
keepalive 10 120 
comp-lzo 
persist-key 
persist-tun  
status /var/log/openvpn/openvpn.tcp.status 
log-append /var/log/openvpn/openvpn.tcp.log 
verb 5  

plugin /usr/lib/openvpn/openvpn-auth-pam.so mysql
client-cert-not-required username-as-common-name
writepid /var/log/openvpn/openvpn.tcp.pid

Client config:
dev tun 
proto tcp 
remote a.b.c.d xyz 
resolv-retry infinite 
nobind 
persist-key 
persist-tun 
ca ca.crt 
comp-lzo 
verb 3 
auth-user-pass
```
