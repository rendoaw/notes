This post contains brief instruction on how to establish IPv6 over GPRS.

In general, there are two basic methods:

1. Old but fastest way, just do normal IPv4 GPRS PDP context and after that you create IPv6 over IPv4 tunnel on top of your GPRS connection. The tunnel can be any tunnel mechanism such as 6-to-4, IPv6 gre tunnel, IPIP tunnel, IPSec tunnel, etc
2. Native IPv6 GPRS connection

Today, i will only explain about native IPv6 connection. I'll try to explain from mobile operator side as well as end user side.
I'll start from the mobile operator side first. There are five network elements inside mobile operator network which must be have IPv6 capability. if you feel hard to understand my writing below, please read http://en.wikipedia.org/wiki/GPRS_core_network first.
1. SGSN (Serving GPRS support node). In simple language, we can see SGSN as the first control gateway from radio network. SGSN is retrieving enduser profile from "central database". SGSN need to have IPv6 capability so it can carry end user IPv6 packet over IPv4 GTP tunnel towards GGSN.
2. GGSN (Gateway GPRS support node). GGSN is the gateway from GPRS network towards normal IP network such as internet or corporate LAN. GGSN need to have IPv6 capability to open the encapsulation header of GTP tunnel from SGSN side and route the IPv6 traffic to the internet.
3. HLR (home location register). HLR stores a very complete data for each subscriber including what APNs are allowed for each subcriber, its QoS profile and the important thing for this IPv6 GPRS is what kind of PDP context that allowed for each subcriber. Normally, only IPv4 PDP is allowed, so we need to insert new profile to allow IPv6 PDP from certain subcribers.
4. IP Router. I think i don't need to explain about the router. If you want end-to-end native IPv6 connectivity, you need dual stack (IPv4 and IPv6) capability in your routers.
5. DNS server. IPv6 enabled DNS server is the important thing in general IPv6 networks. It is impossible for us to remember the 128 bit IPv6 address for each machine.

Now, time for enduser side. There are two important things that you must have to be able to get IPv6 over GPRS connection.
1. handset. It is a must for you to have GPRS capable handset that have IPv6 capability. There are two types of IPv6 GPRS capable handset, the first is handset that only support IPv6 GPRS connection if only you are using that handset as a modem for your PC, either using serial/usb cable, bluetooth or infrared. The second is the handset that has IPv6 capabilty inside its operating system such as HP IPAQ, Nokia N73, etc. The advantages of the second handset is you are able to do IPv6 WAP or HTTP browsing directly from your phone. Unfortunately, I can not found any IPv6 enabled 3G data card.
2. If you are using a laptop with a IPv6 capable handset as a modem, you need operating system that support IPv6 in its PPP stack. If you are Microsoft Windows user, you need at least Windows Vista. Although windows XP is already has native IPv6 capability, XP does not have IPv6 in PPP stack. The good news is, if you are unix user, especially FreeBSD and Linux (sorry i can't give any info regarding any other Unx family since i never test them), you already have IPv6 in your OS PPP stack since few years ago.

So, if you are already those two required things above, you can start to create IPv6 GPRS connection. I give the configuraton and steps example based on my experience by using FreeBSD.
a. make sure you are attached to GPRS network to be able to have GPRS PDP context. It doesn't matter you are in GSM or WCDMA network.
b. make sure your gprs profile in your handset is already PDP type IPv6. Unfortunately, in most phone, there is no setting menu to do this, so you may need to issue an AT command to your phone. The required AT command is AT+CGDCONT=X,”IPv6”,”apn name”. X=APN setting ID (CID) inhandset. Please refer to how to know GPRS cid in SE M600i if you want to know more about CID.
c. configure your ppp.conf. If you don't issue any AT command as specified in step b above, you can configure it inside your ppp.conf as below. In example below I use cid number 8 and apn name "gprs6"
```
gprs:
set dial "ABORT BUSY ABORTNO\\sCARRIER TIMEOUT 5 \
\"\" ATZ OK-ATZ-OKAT+CGDCONT=8,\\\"ipv6\\\",\\\"gprs6\\\" OK \\dATD\\TTIMEOUT 60 CONNECT"
enable force-scripts
disable vjcomp
set authname your-username
set authkey your-password
set phone "*99***8#"
setlogin
set timeout 0
enable dns
add default HISADDR
add default HISADDR6
```
d. and if you are success, you will get an output like
```
> ifconfig tun0
tun0: flags=8051<UP,POINTOPOINT,RUNNING,MULTICAST> mtu 1500
inet6 fe80::e36:ae02:cdd9:134c%tun0 prefixlen 64 scopeid 0x5
inet6 xxxx:yyyy:f:1001:e36:ae02:cdd9:134c prefixlen 64 autoconf
Opened by PID 676
>
```
And you are connected to native IPv6 world. And if your connection is OK, as usual you will see dancing turtle in www.kame.net or dancing elephant in ITB website :)

Notes:
Attach: GPRS state when you are connected to GPRS network but you don't do anything such as, dialling *99***1#, *99# or doing any wap browsing. In SoneEricsson phone, this state is indicate by upsidedown triangle symbol above your signal bar indicator
PDP context: if you do GPRS dial with your pc or maybe do wap browsing from your phone, it means that you are doing PDP context to the network and you are in active state. In SonyEricsson phone,it usually is indicated by small globe symbol.

