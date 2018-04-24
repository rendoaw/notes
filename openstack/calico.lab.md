openstack flavor create --public m1.tiny --id auto --ram 256 --disk 0 --vcpus 1 --rxtx-factor 1
sudo nova-manage cell_v2 discover_hosts


dnsmasq --no-hosts \
    --no-resolv \
    --strict-order \
    --except-interface=lo \
    --pid-file=/var/lib/neutron/dhcp/345ab0d1-44e4-43bb-939d-0c39aa8e1d93/pid \
    --dhcp-hostsfile=/var/lib/neutron/dhcp/345ab0d1-44e4-43bb-939d-0c39aa8e1d93/host \
    --addn-hosts=/var/lib/neutron/dhcp/345ab0d1-44e4-43bb-939d-0c39aa8e1d93/addn_hosts \
    --dhcp-optsfile=/var/lib/neutron/dhcp/345ab0d1-44e4-43bb-939d-0c39aa8e1d93/opts \
    --dhcp-leasefile=/var/lib/neutron/dhcp/345ab0d1-44e4-43bb-939d-0c39aa8e1d93/leases \
    --dhcp-match=set:ipxe,175 \
    --bind-dynamic \
    --interface=ns-345ab0d1-44 \
    --dhcp-range=set:tag0,10.10.0.0,static,255.255.0.0,86400s \
    --dhcp-option-force=option:mtu,1500 \
    --dhcp-lease-max=65536 \
    --conf-file= \
    --domain=openstacklocal \
    --enable-ra \
    --interface=tap6746bfa3-a5 \
    --bridge-interface=ns-345ab0d1-44,tap6746bfa3-a5
 

[root@node1 centos]# more /var/lib/neutron/dhcp/345ab0d1-44e4-43bb-939d-0c39aa8e1d93/host
fa:16:3e:a9:5b:5c,host-10-10-0-10.openstacklocal,10.10.0.10
[root@node1 centos]#
[root@node1 centos]# more /var/lib/neutron/dhcp/345ab0d1-44e4-43bb-939d-0c39aa8e1d93/addn_hosts
10.10.0.10	host-10-10-0-10.openstacklocal host-10-10-0-10
[root@node1 centos]#
[root@node1 centos]# more /var/lib/neutron/dhcp/345ab0d1-44e4-43bb-939d-0c39aa8e1d93/opts
tag:tag0,option:router,10.10.0.1
[root@node1 centos]#
[root@node1 centos]# more /var/lib/neutron/dhcp/345ab0d1-44e4-43bb-939d-0c39aa8e1d93/leases
1524669247 fa:16:3e:a9:5b:5c 10.10.0.10 host-10-10-0-10 01:fa:16:3e:a9:5b:5c
[root@node1 centos]#



[root@controller ~]# openstack server list
+--------------------------------------+--------------------+--------+---------------------------+---------------------+---------+
| ID                                   | Name               | Status | Networks                  | Image               | Flavor  |
+--------------------------------------+--------------------+--------+---------------------------+---------------------+---------+
| abde4a7d-d4b0-4ca9-bb31-a05e7d9297df | training-instance2 | ACTIVE | training-net-2=10.20.0.5  | cirros-0.3.2-x86_64 | m1.tiny |
| e75f847d-cee2-4653-ada5-c40f3eaa6125 | training-instance1 | ACTIVE | training-net-1=10.10.0.10 | cirros-0.3.2-x86_64 | m1.tiny |
+--------------------------------------+--------------------+--------+---------------------------+---------------------+---------+
[root@controller ~]#
[root@controller ~]# openstack server show abde4a7d-d4b0-4ca9-bb31-a05e7d9297df
+-------------------------------------+------------------------------------------------------------+
| Field                               | Value                                                      |
+-------------------------------------+------------------------------------------------------------+
| OS-DCF:diskConfig                   | MANUAL                                                     |
| OS-EXT-AZ:availability_zone         | nova                                                       |
| OS-EXT-SRV-ATTR:host                | node2                                                      |
| OS-EXT-SRV-ATTR:hypervisor_hostname | node2                                                      |
| OS-EXT-SRV-ATTR:instance_name       | instance-00000002                                          |
| OS-EXT-STS:power_state              | Running                                                    |
| OS-EXT-STS:task_state               | None                                                       |
| OS-EXT-STS:vm_state                 | active                                                     |
| OS-SRV-USG:launched_at              | 2018-04-24T15:25:07.000000                                 |
| OS-SRV-USG:terminated_at            | None                                                       |
| accessIPv4                          |                                                            |
| accessIPv6                          |                                                            |
| addresses                           | training-net-2=10.20.0.5                                   |
| config_drive                        |                                                            |
| created                             | 2018-04-24T15:24:59Z                                       |
| flavor                              | m1.tiny (d2ebd592-2572-4c5e-9300-7d9f1e376de0)             |
| hostId                              | 63944f5af87ec2ae9dc8daae18f4a8e6cb1ecfbcc433286eac9d4537   |
| id                                  | abde4a7d-d4b0-4ca9-bb31-a05e7d9297df                       |
| image                               | cirros-0.3.2-x86_64 (7e5a6441-7e34-4a0c-9d7c-c12f04fb53ea) |
| key_name                            | None                                                       |
| name                                | training-instance2                                         |
| progress                            | 0                                                          |
| project_id                          | d1b0e9f0a0124664905b1987c15385ed                           |
| properties                          |                                                            |
| security_groups                     | name='default'                                             |
| status                              | ACTIVE                                                     |
| updated                             | 2018-04-24T15:25:07Z                                       |
| user_id                             | 325bbcae7a2e444f814c8daba59abc31                           |
| volumes_attached                    |                                                            |
+-------------------------------------+------------------------------------------------------------+
[root@controller ~]#
[root@controller ~]# openstack server show e75f847d-cee2-4653-ada5-c40f3eaa6125
+-------------------------------------+------------------------------------------------------------+
| Field                               | Value                                                      |
+-------------------------------------+------------------------------------------------------------+
| OS-DCF:diskConfig                   | MANUAL                                                     |
| OS-EXT-AZ:availability_zone         | nova                                                       |
| OS-EXT-SRV-ATTR:host                | node1                                                      |
| OS-EXT-SRV-ATTR:hypervisor_hostname | node1                                                      |
| OS-EXT-SRV-ATTR:instance_name       | instance-00000001                                          |
| OS-EXT-STS:power_state              | Running                                                    |
| OS-EXT-STS:task_state               | None                                                       |
| OS-EXT-STS:vm_state                 | active                                                     |
| OS-SRV-USG:launched_at              | 2018-04-24T15:13:57.000000                                 |
| OS-SRV-USG:terminated_at            | None                                                       |
| accessIPv4                          |                                                            |
| accessIPv6                          |                                                            |
| addresses                           | training-net-1=10.10.0.10                                  |
| config_drive                        |                                                            |
| created                             | 2018-04-24T15:13:48Z                                       |
| flavor                              | m1.tiny (d2ebd592-2572-4c5e-9300-7d9f1e376de0)             |
| hostId                              | 21f3a12bd63f9fed2b3fca2613986570f063596e7ca2d7ff3f602388   |
| id                                  | e75f847d-cee2-4653-ada5-c40f3eaa6125                       |
| image                               | cirros-0.3.2-x86_64 (7e5a6441-7e34-4a0c-9d7c-c12f04fb53ea) |
| key_name                            | None                                                       |
| name                                | training-instance1                                         |
| progress                            | 0                                                          |
| project_id                          | d1b0e9f0a0124664905b1987c15385ed                           |
| properties                          |                                                            |
| security_groups                     | name='default'                                             |
| status                              | ACTIVE                                                     |
| updated                             | 2018-04-24T15:13:57Z                                       |
| user_id                             | 325bbcae7a2e444f814c8daba59abc31                           |
| volumes_attached                    |                                                            |
+-------------------------------------+------------------------------------------------------------+
[root@controller ~]#


[root@node1 centos]# ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 9001 qdisc mq state UP qlen 1000
    link/ether 06:3f:0b:b2:18:50 brd ff:ff:ff:ff:ff:ff
    inet 172.49.20.231/24 brd 172.49.20.255 scope global dynamic eth0
       valid_lft 3124sec preferred_lft 3124sec
    inet6 fe80::43f:bff:feb2:1850/64 scope link
       valid_lft forever preferred_lft forever
3: dummy0: <BROADCAST,NOARP> mtu 1500 qdisc noop state DOWN qlen 1000
    link/ether 8a:41:5a:91:8b:ac brd ff:ff:ff:ff:ff:ff
4: ns-345ab0d1-44: <BROADCAST,NOARP,UP,LOWER_UP> mtu 1500 qdisc noqueue state UNKNOWN qlen 1000
    link/ether 02:00:00:00:00:00 brd ff:ff:ff:ff:ff:ff
    inet 10.10.0.1/16 brd 10.10.255.255 scope global ns-345ab0d1-44
       valid_lft forever preferred_lft forever
    inet6 fe80::ff:fe00:0/64 scope link
       valid_lft forever preferred_lft forever
5: tap6746bfa3-a5: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP qlen 1000
    link/ether fe:16:3e:a9:5b:5c brd ff:ff:ff:ff:ff:ff
    inet6 fe80::fc16:3eff:fea9:5b5c/64 scope link
       valid_lft forever preferred_lft forever
[root@node1 centos]#
[root@node1 centos]#
[root@node1 centos]# ip r
default via 172.49.20.1 dev eth0
10.10.0.10 dev tap6746bfa3-a5 scope link
10.20.0.5 via 172.49.20.232 dev eth0 proto bird
172.49.20.0/24 dev eth0 proto kernel scope link src 172.49.20.231
[root@node1 centos]#



[root@node1 centos]# ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 9001 qdisc mq state UP qlen 1000
    link/ether 06:3f:0b:b2:18:50 brd ff:ff:ff:ff:ff:ff
    inet 172.49.20.231/24 brd 172.49.20.255 scope global dynamic eth0
       valid_lft 2806sec preferred_lft 2806sec
    inet6 fe80::43f:bff:feb2:1850/64 scope link
       valid_lft forever preferred_lft forever
3: dummy0: <BROADCAST,NOARP> mtu 1500 qdisc noop state DOWN qlen 1000
    link/ether 8a:41:5a:91:8b:ac brd ff:ff:ff:ff:ff:ff
4: ns-345ab0d1-44: <BROADCAST,NOARP,UP,LOWER_UP> mtu 1500 qdisc noqueue state UNKNOWN qlen 1000
    link/ether 02:00:00:00:00:00 brd ff:ff:ff:ff:ff:ff
    inet 10.10.0.1/16 brd 10.10.255.255 scope global ns-345ab0d1-44
       valid_lft forever preferred_lft forever
    inet6 fe80::ff:fe00:0/64 scope link
       valid_lft forever preferred_lft forever
5: tap6746bfa3-a5: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP qlen 1000
    link/ether fe:16:3e:a9:5b:5c brd ff:ff:ff:ff:ff:ff
    inet6 fe80::fc16:3eff:fea9:5b5c/64 scope link
       valid_lft forever preferred_lft forever
6: ns-45117d3d-ac: <BROADCAST,NOARP,UP,LOWER_UP> mtu 1500 qdisc noqueue state UNKNOWN qlen 1000
    link/ether 02:00:00:00:00:00 brd ff:ff:ff:ff:ff:ff
    inet 10.20.0.1/16 brd 10.20.255.255 scope global ns-45117d3d-ac
       valid_lft forever preferred_lft forever
    inet6 fe80::ff:fe00:0/64 scope link
       valid_lft forever preferred_lft forever
7: tap49002d09-c4: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP qlen 1000
    link/ether fe:16:3e:2d:dc:5e brd ff:ff:ff:ff:ff:ff
    inet6 fe80::fc16:3eff:fe2d:dc5e/64 scope link
       valid_lft forever preferred_lft forever
8: tap71e30081-58: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP qlen 1000
    link/ether fe:16:3e:89:7b:57 brd ff:ff:ff:ff:ff:ff
    inet6 fe80::fc16:3eff:fe89:7b57/64 scope link
       valid_lft forever preferred_lft forever
9: tape3076591-36: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP qlen 1000
    link/ether fe:16:3e:d9:fa:91 brd ff:ff:ff:ff:ff:ff
    inet6 fe80::fc16:3eff:fed9:fa91/64 scope link
       valid_lft forever preferred_lft forever


[root@controller ~]# for i in `openstack server list | grep ACTIVE | awk '{print $2}'` ; do openstack server show $i | egrep "instance_name|hypervisor_hostname|addresses"; done
| OS-EXT-SRV-ATTR:hypervisor_hostname | node2                                                      |
| OS-EXT-SRV-ATTR:instance_name       | instance-00000008                                          |
| addresses                           | training-net-1=10.10.0.6                                   |
| OS-EXT-SRV-ATTR:hypervisor_hostname | node1                                                      |
| OS-EXT-SRV-ATTR:instance_name       | instance-00000007                                          |
| addresses                           | training-net-1=10.10.0.4                                   |
| OS-EXT-SRV-ATTR:hypervisor_hostname | node2                                                      |
| OS-EXT-SRV-ATTR:instance_name       | instance-00000006                                          |
| addresses                           | training-net-1=10.10.0.5                                   |
| OS-EXT-SRV-ATTR:hypervisor_hostname | node1                                                      |
| OS-EXT-SRV-ATTR:instance_name       | instance-00000005                                          |
| addresses                           | training-net-2=10.20.0.2                                   |
| OS-EXT-SRV-ATTR:hypervisor_hostname | node2                                                      |
| OS-EXT-SRV-ATTR:instance_name       | instance-00000004                                          |
| addresses                           | training-net-2=10.20.0.13                                  |
| OS-EXT-SRV-ATTR:hypervisor_hostname | node1                                                      |
| OS-EXT-SRV-ATTR:instance_name       | instance-00000003                                          |
| addresses                           | training-net-2=10.20.0.7                                   |
| OS-EXT-SRV-ATTR:hypervisor_hostname | node2                                                      |
| OS-EXT-SRV-ATTR:instance_name       | instance-00000002                                          |
| addresses                           | training-net-2=10.20.0.5                                   |
| OS-EXT-SRV-ATTR:hypervisor_hostname | node1                                                      |
| OS-EXT-SRV-ATTR:instance_name       | instance-00000001                                          |
| addresses                           | training-net-1=10.10.0.10                                  |


[root@node1 centos]# sysctl -a | grep -i arp | grep -v "= 0"
dev.parport.default.spintime = 500
dev.parport.default.timeslice = 200
net.ipv4.conf.tap49002d09-c4.proxy_arp = 1
net.ipv4.conf.tap6746bfa3-a5.proxy_arp = 1
net.ipv4.conf.tap71e30081-58.proxy_arp = 1
net.ipv4.conf.tape3076591-36.proxy_arp = 1






$ arp -a -n
? (10.10.0.4) at fe:16:3e:a9:5b:5c [ether]  on eth0
? (10.10.0.5) at fe:16:3e:a9:5b:5c [ether]  on eth0
? (10.10.0.1) at fe:16:3e:a9:5b:5c [ether]  on eth0
? (10.10.0.6) at fe:16:3e:a9:5b:5c [ether]  on eth0
$

$ ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 16436 qdisc noqueue
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast qlen 1000
    link/ether fa:16:3e:a9:5b:5c brd ff:ff:ff:ff:ff:ff
    inet 10.10.0.10/16 brd 10.10.255.255 scope global eth0
    inet6 fe80::f816:3eff:fea9:5b5c/64 scope link
       valid_lft forever preferred_lft forever
$  ip r
default via 10.10.0.1 dev eth0
10.10.0.0/16 dev eth0  src 10.10.0.10
$

