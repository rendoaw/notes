```
Background
This page is created to log the Openstack + Cailco test finding.
As initial effort, the test is done on virtualized environment. All openstack controller and compute nodes are VM, therefore the openstack guest VM is considered as nested VM. 
Setup
Here is the high level initial test setup
ENG DataCenter Network Engr > Trying Openstack + Calico > image2017-3-23 8:58:24.png
Nodes:
1x controller
2x compute nodes
S/W
OS: Ubuntu 
OpenStack version: Mitaka
Calico version: 2.0
High level Steps
Install Openstack Mitaka on Ubuntu
Make sure it works with standard Neutron ML2 Linux Bridge + vxlan plugins
Replace Linux bridge + vxlan with Calico
Final Setup
Here is the test setup with 3 guest VMs created on 2 compute nodes and 2 virtual networks created using Calico.
ENG DataCenter Network Engr > Trying Openstack + Calico > image2017-3-23 9:10:38.png
Due to environment limitation, I don't have any control on the (virtual) switch that managed 1.70.62.x subnet (hypervisor subnet), so it has no idea of 10.65.x.x and 10.66.x.x subnet. Therefore, to allow VM to VM communication, i need to create a tunnel and route the VM to VM traffic over it. The updated diagram with the tunnel network shown below.
ENG DataCenter Network Engr > Trying Openstack + Calico > image2017-3-23 9:29:16.png
For simplicity, simply assume the L3 tunnel here is a normal L3 link between multiple computes.
Notes: It is not mandatory to use vxlan as L3 tunnel, I just do it for fun to test unicast-only vxlan setup on Linux. We can replace it with any other type of tunnel, GRE, IPIP, etc.

Findings
Lack of documentation on how to enable Calico on existing Openstack with existing neutron plugin, although once we find the way, the configuration is actually straight forward.
We can create multiple virtual network but they are by default can communicate each other. 
As shown in the diagram above, we have 2 virtual networks 10.65.0.0/245 and 10.66.0.0/24
Both virtual network are created on the same compute node global routing table
root@compute1:/home/ubuntu# ifconfig  | egrep "Link|inet addr"
...deleted..
eth0      Link encap:Ethernet  HWaddr fa:16:3e:26:12:d2     -------------> this is hypervisor IP
          inet addr:1.70.62.151  Bcast:1.70.62.255  Mask:255.255.255.128
ns-16fd98d0-15 Link encap:Ethernet  HWaddr 02:00:00:00:00:00     -------------> this is L3 gateway for virtual network 1
          inet addr:10.65.0.1  Bcast:10.65.0.255  Mask:255.255.255.0
          inet6 addr: fe80::ff:fe00:0/64 Scope:Link
ns-7c9ccb92-80 Link encap:Ethernet  HWaddr 02:00:00:00:00:00     -------------> this is L3 gateway for virtual network 2
          inet addr:10.66.0.1  Bcast:10.66.0.255  Mask:255.255.255.0
          inet6 addr: fe80::ff:fe00:0/64 Scope:Link
..deleted..

Guest VM IP from different compute is advertised by other compute through BGP. In this case, we have "Bird" routing daemon that simply redistribute static and directly connected route to BGP.
Calico create static route to each local VM IP via tap interface, and Bird redistribute it to BGP
root@compute1:/home/ubuntu# ip r
default via 1.70.62.129 dev eth0                                  -----------> hypervisor default gateway
1.70.62.128/25 dev eth0  proto kernel  scope link  src 1.70.62.151
2.1.1.0/24 dev vxlan21  proto kernel  scope link  src 2.1.1.1
10.65.0.2 dev tapc83075fb-53  scope link                           -----------> route to VM C1
10.65.0.3 via 2.1.1.2 dev vxlan21  proto bird                      -----------> route to VM C2 on other compute
10.66.0.2 dev tap5dbf00fb-5a  scope link                           -----------> route to VM D1
192.168.122.0/24 dev virbr0  proto kernel  scope link  src 192.168.122.1

If we check on the Bird itself, we will see more detail
bird> show route all
0.0.0.0/0          via 1.70.62.129 on eth0 [kernel1 2017-03-21] * (10)    -----------> hypervisor default gateway
        Type: inherit unicast univ
        Kernel.source: 3
        Kernel.metric: 0
10.65.0.3/32       via 2.1.1.2 on vxlan21 [N2 2017-03-21] * (100/0) [i]    -----------> route to VM C2 on other compute
        Type: BGP unicast univ
        BGP.origin: IGP
        BGP.as_path:
        BGP.next_hop: 2.1.1.2
        BGP.local_pref: 100
10.65.0.2/32       dev tapc83075fb-53 [kernel1 2017-03-21] * (10)          -----------> route to VM C1
        Type: inherit unicast univ
        Kernel.source: 3
        Kernel.metric: 0
2.1.1.0/24         dev vxlan21 [direct1 2017-03-21] * (240)
        Type: device unicast univ
10.66.0.2/32       dev tap5dbf00fb-5a [kernel1 2017-03-21] * (10)          -----------> route to VM D1
        Type: inherit unicast univ
        Kernel.source: 3
        Kernel.metric: 0
1.70.62.128/25     dev eth0 [direct1 2017-03-21] * (240)
        Type: device unicast univ
bird>



... to be continue ...

TO DO
The following resources suggest Calico supports overlap IP and/or tenant network separation, we need to find out how to enable this.
http://docs.projectcalico.org/v1.5/reference/advanced/overlap-ips
http://docs-archive.projectcalico.org/en/1.4.3/faq.html


Appendix A: Detailed Steps
Preparation
create calico virtual network. example:
root@controller:/var/log/nova# neutron net-create --shared --provider:network_type local calico2
neutron CLI is deprecated and will be removed in the future. Use openstack CLI instead.
Created a new network:
+---------------------------+--------------------------------------+
| Field                     | Value                                |
+---------------------------+--------------------------------------+
| admin_state_up            | True                                 |
| availability_zone_hints   |                                      |
| availability_zones        |                                      |
| created_at                | 2017-03-21T13:39:42                  |
| description               |                                      |
| id                        | 7c9ccb92-80ba-4b3f-a36d-2641d69e8df8 |
| ipv4_address_scope        |                                      |
| ipv6_address_scope        |                                      |
| mtu                       | 1500                                 |
| name                      | calico2                              |
| provider:network_type     | local                                |
| provider:physical_network |                                      |
| provider:segmentation_id  |                                      |
| router:external           | False                                |
| shared                    | True                                 |
| status                    | ACTIVE                               |
| subnets                   |                                      |
| tags                      |                                      |
| tenant_id                 | b53c80a64a384f3da9079809a95ea5ad     |
| updated_at                | 2017-03-21T13:39:42                  |
+---------------------------+--------------------------------------+

root@controller:/var/log/nova# neutron subnet-create --gateway 10.66.0.1 --enable-dhcp --ip-version 4 --name calico-v4 calico2 10.66.0.0/24
neutron CLI is deprecated and will be removed in the future. Use openstack CLI instead.
Created a new subnet:
+-------------------+----------------------------------------------+
| Field             | Value                                        |
+-------------------+----------------------------------------------+
| allocation_pools  | {"start": "10.66.0.2", "end": "10.66.0.254"} |
| cidr              | 10.66.0.0/24                                 |
| created_at        | 2017-03-21T13:39:54                          |
| description       |                                              |
| dns_nameservers   |                                              |
| enable_dhcp       | True                                         |
| gateway_ip        | 10.66.0.1                                    |
| host_routes       |                                              |
| id                | 5fdc6b1c-1636-4c43-884a-287a09b2bcd0         |
| ip_version        | 4                                            |
| ipv6_address_mode |                                              |
| ipv6_ra_mode      |                                              |
| name              | calico-v4                                    |
| network_id        | 7c9ccb92-80ba-4b3f-a36d-2641d69e8df8         |
| subnetpool_id     |                                              |
| tenant_id         | b53c80a64a384f3da9079809a95ea5ad             |
| updated_at        | 2017-03-21T13:39:54                          |
+-------------------+----------------------------------------------+


List existing virtual network
root@controller:/var/log/nova# openstack network list
WARNING: openstackclient.common.utils is deprecated and will be removed after Jun 2017. Please use osc_lib.utils. This warning is caused by an out-of-date import in /usr/lib/python2.7/dist-packages/heatclient/osc/plugin.py
+--------------------------------------+---------+--------------------------------------+
| ID                                   | Name    | Subnets                              |
+--------------------------------------+---------+--------------------------------------+
| 16fd98d0-157e-433f-aa89-bd9290d26dac | calico  | 09cbe211-5dd3-422a-8ea4-66c387a04e3a |
| 7c9ccb92-80ba-4b3f-a36d-2641d69e8df8 | calico2 | 5fdc6b1c-1636-4c43-884a-287a09b2bcd0 |
+--------------------------------------+---------+--------------------------------------+

Create VM that attached connected to calico virtual network
root@controller:/var/log/nova# openstack server create --flavor m1.nano --image cirros --nic net-id=7c9ccb92-80ba-4b3f-a36d-2641d69e8df8 --security-group default d1
WARNING: openstackclient.common.utils is deprecated and will be removed after Jun 2017. Please use osc_lib.utils. This warning is caused by an out-of-date import in /usr/lib/python2.7/dist-packages/heatclient/osc/plugin.py
+-------------------------------------+-----------------------------------------------+
| Field                               | Value                                         |
+-------------------------------------+-----------------------------------------------+
| OS-DCF:diskConfig                   | MANUAL                                        |
| OS-EXT-AZ:availability_zone         |                                               |
| OS-EXT-SRV-ATTR:host                | None                                          |
| OS-EXT-SRV-ATTR:hypervisor_hostname | None                                          |
| OS-EXT-SRV-ATTR:instance_name       | instance-00000009                             |
| OS-EXT-STS:power_state              | NOSTATE                                       |
| OS-EXT-STS:task_state               | scheduling                                    |
| OS-EXT-STS:vm_state                 | building                                      |
| OS-SRV-USG:launched_at              | None                                          |
| OS-SRV-USG:terminated_at            | None                                          |
| accessIPv4                          |                                               |
| accessIPv6                          |                                               |
| addresses                           |                                               |
| adminPass                           | p55QB6H7w7BF                                  |
| config_drive                        |                                               |
| created                             | 2017-03-21T13:42:38Z                          |
| flavor                              | m1.nano (0)                                   |
| hostId                              |                                               |
| id                                  | 40c43d23-4024-4ae1-8601-3d7d1f25ef71          |
| image                               | cirros (653a96e9-0c7f-4ea6-b863-0e8bf5274452) |
| key_name                            | None                                          |
| name                                | d1                                            |
| progress                            | 0                                             |
| project_id                          | b53c80a64a384f3da9079809a95ea5ad              |
| properties                          |                                               |
| security_groups                     | name='default'                                |
| status                              | BUILD                                         |
| updated                             | 2017-03-21T13:42:39Z                          |
| user_id                             | 6a8aa083a7a14b258cc56106ef120f37              |
| volumes_attached                    |                                               |
+-------------------------------------+-----------------------------------------------+


root@controller:/var/log/nova# openstack server show d1
WARNING: openstackclient.common.utils is deprecated and will be removed after Jun 2017. Please use osc_lib.utils. This warning is caused by an out-of-date import in /usr/lib/python2.7/dist-packages/heatclient/osc/plugin.py
+-------------------------------------+----------------------------------------------------------+
| Field                               | Value                                                    |
+-------------------------------------+----------------------------------------------------------+
| OS-DCF:diskConfig                   | MANUAL                                                   |
| OS-EXT-AZ:availability_zone         | nova                                                     |
| OS-EXT-SRV-ATTR:host                | compute1                                                 |
| OS-EXT-SRV-ATTR:hypervisor_hostname | compute1                                                 |
| OS-EXT-SRV-ATTR:instance_name       | instance-00000009                                        |
| OS-EXT-STS:power_state              | Running                                                  |
| OS-EXT-STS:task_state               | None                                                     |
| OS-EXT-STS:vm_state                 | active                                                   |
| OS-SRV-USG:launched_at              | 2017-03-21T13:42:44.000000                               |
| OS-SRV-USG:terminated_at            | None                                                     |
| accessIPv4                          |                                                          |
| accessIPv6                          |                                                          |
| addresses                           | calico2=10.66.0.2                                        |
| config_drive                        |                                                          |
| created                             | 2017-03-21T13:42:38Z                                     |
| flavor                              | m1.nano (0)                                              |
| hostId                              | 1257ec1c4a278c65cdb53e0bd8d7fe8f7eddfeca23fa1b9fe58d868e |
| id                                  | 40c43d23-4024-4ae1-8601-3d7d1f25ef71                     |
| image                               | cirros (653a96e9-0c7f-4ea6-b863-0e8bf5274452)            |
| key_name                            | None                                                     |
| name                                | d1                                                       |
| progress                            | 0                                                        |
| project_id                          | b53c80a64a384f3da9079809a95ea5ad                         |
| properties                          |                                                          |
| security_groups                     | name='default'                                           |
| status                              | ACTIVE                                                   |
| updated                             | 2017-03-21T13:42:44Z                                     |
| user_id                             | 6a8aa083a7a14b258cc56106ef120f37                         |
| volumes_attached                    |                                                          |
+-------------------------------------+----------------------------------------------------------+


List all VMs and find out the hypervisor
root@controller:/var/log/nova# openstack server list
+--------------------------------------+------+--------+-------------------+------------+
| ID                                   | Name | Status | Networks          | Image Name |
+--------------------------------------+------+--------+-------------------+------------+
| 40c43d23-4024-4ae1-8601-3d7d1f25ef71 | d1   | ACTIVE | calico2=10.66.0.2 | cirros     |
| 4335494c-09a7-40bd-ba38-e752bbd366ca | c2   | ACTIVE | calico=10.65.0.3  | cirros     |
| 86d68ee3-cc91-435d-a318-633400263c36 | c1   | ACTIVE | calico=10.65.0.2  | cirros     |
+--------------------------------------+------+--------+-------------------+------------+


root@controller:/var/log/nova# openstack server show d1 | grep hypervisor_hostname
| OS-EXT-SRV-ATTR:hypervisor_hostname | compute1                                                 |


root@controller:/var/log/nova# openstack server show c1 | grep hypervisor_hostname
| OS-EXT-SRV-ATTR:hypervisor_hostname | compute1                                                 |


root@controller:/var/log/nova# openstack server show c2 | grep hypervisor_hostname
| OS-EXT-SRV-ATTR:hypervisor_hostname | compute2                                                 |

Go to one of the VM and test the connectivity to other VMs

Connectivity to the VM on the same virtual network
root@compute2:/home/ubuntu# ssh cirros@10.65.0.3  ----> this is instance c2 on compute2
cirros@10.65.0.3's password:
$ ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 16436 qdisc noqueue
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast qlen 1000
    link/ether fa:16:3e:1b:20:43 brd ff:ff:ff:ff:ff:ff
    inet 10.65.0.3/24 brd 10.65.0.255 scope global eth0
    inet6 fe80::f816:3eff:fe1b:2043/64 scope link
       valid_lft forever preferred_lft forever


$ ip r
default via 10.65.0.1 dev eth0
10.65.0.0/24 dev eth0  src 10.65.0.3

$ ping -c 3 10.65.0.2                            -----> ping to c1 (same vnet, different compute)
PING 10.65.0.2 (10.65.0.2): 56 data bytes
64 bytes from 10.65.0.2: seq=0 ttl=62 time=1.842 ms
64 bytes from 10.65.0.2: seq=1 ttl=62 time=1.138 ms
64 bytes from 10.65.0.2: seq=2 ttl=62 time=1.222 ms
--- 10.65.0.2 ping statistics ---
3 packets transmitted, 3 packets received, 0% packet loss
round-trip min/avg/max = 1.138/1.400/1.842 ms

Connectivity to the VM on different virtual network
root@compute2:/home/ubuntu# ssh cirros@10.65.0.3  ----> this is instance c2 on compute2
cirros@10.65.0.3's password:


$ ping -c 3 10.66.0.2                            -----> ping to d1 (different vnet, different compute)
PING 10.66.0.2 (10.66.0.2): 56 data bytes
64 bytes from 10.66.0.2: seq=0 ttl=62 time=1.230 ms
64 bytes from 10.66.0.2: seq=1 ttl=62 time=1.267 ms
64 bytes from 10.66.0.2: seq=2 ttl=62 time=1.131 ms
--- 10.66.0.2 ping statistics ---
3 packets transmitted, 3 packets received, 0% packet loss
round-trip min/avg/max = 1.131/1.209/1.267 ms

Check BIRD routing table 
on compute 1
bird> show route all
0.0.0.0/0          via 1.70.62.129 on eth0 [kernel1 13:11:57] * (10)
        Type: inherit unicast univ
        Kernel.source: 3
        Kernel.metric: 0
10.65.0.3/32       via 2.1.1.2 on vxlan21 [N2 13:12:13] * (100/0) [i]  ----> this is instance c2 (remote)
        Type: BGP unicast univ
        BGP.origin: IGP
        BGP.as_path:
        BGP.next_hop: 2.1.1.2
        BGP.local_pref: 100
10.65.0.2/32       dev tapc83075fb-53 [kernel1 13:11:57] * (10)    ----> this is instance c1 (local)
        Type: inherit unicast univ
        Kernel.source: 3
        Kernel.metric: 0
2.1.1.0/24         dev vxlan21 [direct1 13:11:57] * (240)
        Type: device unicast univ
10.66.0.2/32       dev tap5dbf00fb-5a [kernel1 13:42:40] * (10)    ----> this is instance d1 (local)
        Type: inherit unicast univ
        Kernel.source: 3
        Kernel.metric: 0
1.70.62.128/25     dev eth0 [direct1 13:11:57] * (240)
        Type: device unicast univ
bird>

on compute 2
bird> show route all
0.0.0.0/0          via 1.70.62.129 on eth0 [kernel1 13:12:09] * (10)
        Type: inherit unicast univ
        Kernel.source: 3
        Kernel.metric: 0
10.65.0.3/32       dev tape0d7c27b-56 [kernel1 13:12:09] * (10)    ----> this is instance c2 (local)
        Type: inherit unicast univ
        Kernel.source: 3
        Kernel.metric: 0
10.65.0.2/32       via 2.1.1.1 on vxlan21 [N2 13:12:13] * (100/0) [i]    ----> this is instance c1 (remote)
        Type: BGP unicast univ
        BGP.origin: IGP
        BGP.as_path:
        BGP.next_hop: 2.1.1.1
        BGP.local_pref: 100
2.1.1.0/24         dev vxlan21 [direct1 13:12:09] * (240)
        Type: device unicast univ
10.66.0.2/32       via 2.1.1.1 on vxlan21 [N2 13:42:40] * (100/0) [i]    ----> this is instance d1 (remote)
        Type: BGP unicast univ
        BGP.origin: IGP
        BGP.as_path:
        BGP.next_hop: 2.1.1.1
        BGP.local_pref: 100
1.70.62.128/25     dev eth0 [direct1 13:12:09] * (240)
        Type: device unicast univ
bird>

Appendix B: Config References
BIRD config
compute 1
root@compute1:/etc/libvirt# cat /etc/bird/bird.conf
router id 1.70.62.151;
# We are only going to export routes from Calico interfaces.
# Currently, 'tap*' is used by the OpenStack implimentation
# and 'cali*' is used by the docker implimentation.
# dummy1 is the interface that bare metal "service" addresses
# should be bound to if they should be exported.
# This will need to be updated as we add new interface names.
#
# Also filter out default, just in case.
#
# We should automate the build of this out of variables when
# we have time.
filter export_bgp {
  if ( (ifname ~ "tap*") || (ifname ~ "cali*") || (ifname ~ "dummy1") ) then {
    if  net != 0.0.0.0/0 then accept;
  }
  reject;
}
# Configure synchronization between BIRD's routing tables and the
# kernel.
protocol kernel {
  learn;          # Learn all alien routes from the kernel
  persist;        # Don't remove routes on bird shutdown
  scan time 2;    # Scan kernel routing table every 2 seconds
  import all;
  graceful restart;
  export all;     # Default is export none
}
# Watch interface up/down events.
protocol device {
  scan time 2;    # Scan interfaces every 2 seconds
}
protocol direct {
   debug all;
   interface "-dummy0", "dummy1", "eth*", "em*", "en*", "br-mgmt", "vxlan21";
}


protocol bgp 'N2' {
  description "Compute2";
  local as 99;
  #neighbor 1.70.62.152 as 99;
  neighbor 2.1.1.2 as 99;
  #multihop;
  import all;
  graceful restart;
  export filter export_bgp;
  next hop self;
  source address 2.1.1.1;  # The local address we use for the TCP connection
  next hop self;
}


compute 2
root@compute2:/home/ubuntu# more /etc/bird/bird.conf
router id 1.70.62.152;
# We are only going to export routes from Calico interfaces.
# Currently, 'tap*' is used by the OpenStack implimentation
# and 'cali*' is used by the docker implimentation.
# dummy1 is the interface that bare metal "service" addresses
# should be bound to if they should be exported.
# This will need to be updated as we add new interface names.
#
# Also filter out default, just in case.
#
# We should automate the build of this out of variables when
# we have time.
filter export_bgp {
  if ( (ifname ~ "tap*") || (ifname ~ "cali*") || (ifname ~ "dummy1") ) then {
    if  net != 0.0.0.0/0 then accept;
  }
  reject;
}
# Configure synchronization between BIRD's routing tables and the
# kernel.
protocol kernel {
  learn;          # Learn all alien routes from the kernel
  persist;        # Don't remove routes on bird shutdown
  scan time 2;    # Scan kernel routing table every 2 seconds
  import all;
  graceful restart;
  export all;     # Default is export none
}
# Watch interface up/down events.
protocol device {
  scan time 2;    # Scan interfaces every 2 seconds
}
protocol direct {
   debug all;
   interface "-dummy0", "dummy1", "eth*", "em*", "en*", "br-mgmt", "vxlan21";
}
protocol bgp 'N2' {
  description "Compute1";
  local as 99;
  #neighbor 1.70.62.151 as 99;
  neighbor 2.1.1.1 as 99;
  #multihop;
  import all;
  graceful restart;
  export filter export_bgp;
  next hop self;
  source address 2.1.1.2;  # The local address we use for the TCP connection
  next hop self;
}



Misc
on this setup, for some reason, Horizon can't talk to nova, but all openstack CLI works. We leave this issue as is for now.

```
