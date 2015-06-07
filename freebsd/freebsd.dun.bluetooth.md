This note will show you how to make gprs connection by using bluetooth DUN profile in FreeBSD. 
It is assumed that all bluetooth device (your laptop and your mobile phone for example) are already configured.

the devices:
1. HP NC6000 laptop with builtin bluetooth adapter
2. Sony Ericsson T630 mobile phone

Steps:
* Make sure your bluetooth device in your laptop is ready to use. Your syslog should show something like this:
```
ubt0: ACTIONTEC Bluetooth by hp, rev 1.10/8.02, addr 2
ubt0: ACTIONTEC Bluetooth by hp, rev 1.10/8.02, addr 2
ubt0: Interface 0 endpoints: interrupt=0×81, bulk-in=0×82, bulk-out=0×2
ubt0: Interface 1 (alt.config 5) endpoints: isoc-in=0×83, isoc-out=0×3; wMaxPacketSize=49; nframes=6, buffer size=294
```

* start your bluetoot 
```
amnesiac# /etc/rc.bluetooth start ubt0
BD_ADDR: 00:0f:b3:17:81:f9
Features: 0xff 0xff 0xf 00 00 00 00 00
<3-Slot> <5-Slot> <Encryption> <Slot offset>
<Timing accuracy> <Switch> <Hold mode> <Sniff mode>
<Park mode> <RSSI> <Channel quality> <SCO link>
<HV2 packets> <HV3 packets> <u-law log> <A-law log> <CVSD>
<Paging scheme> <Power control> <Transparent SCO data>
Max. ACL packet size: 192 bytes
Number of ACL packets: 8
Max. SCO packet size: 64 bytes
Number of SCO packets: 8
amnesiac#
```

* Search your remote bluetooth device
```
amnesiac# hccontrol -n ubt0hci inquiry
Inquiry result, num_responses=1
Inquiry result #0
BD_ADDR: 00:0e:07:a4:c8:f6
Page Scan Rep. Mode: 0×1
Page Scan Period Mode: 00
Page Scan Mode: 00
Class: 52:02:04
Clock offset: 0×6214
Inquiry complete. Status: No error [00]
```

from the result above, you can see that your remote device has h/w address
00:0e:07:a4:c8:f6

* define your remote device in /etc/bluetooth/hcsecd.conf
for example, my device name is blobi and the pin for pairing purpose is "1"
```
device {
bdaddr 00:0e:07:a4:c8:f6;
name "blobi";
key nokey;
pin "1";
}
```

* Run hcsecd daemon by using this command
```
hcsecd -d
```
note: -d means that the daemon will be in foreground mode, it is just show how bluetooth works. You can also run without "-d" option.

This is ouput sample after pairing:
```
hcsecd[694]: Got Link_Key_Request event from 'ubt0hci', remote bdaddr 00:0e:07:a4:c8:f6
hcsecd[694]: Found matching entry, remote bdaddr 00:0e:07:a4:c8:f6, name 'blobi', link key doesn't exist
hcsecd[694]: Sending Link_Key_Negative_Reply to 'ubt0hci' for remote bdaddr 00:0e:07:a4:c8:f6
hcsecd[694]: Got PIN_Code_Request event from 'ubt0hci', remote bdaddr 00:0e:07:a4:c8:f6
hcsecd[694]: Found matching entry, remote bdaddr 00:0e:07:a4:c8:f6, name 'blobi', PIN code exists
hcsecd[694]: Sending PIN_Code_Reply to 'ubt0hci' for remote bdaddr 00:0e:07:a4:c8:f6
hcsecd[694]: Got Link_Key_Notification event from 'ubt0hci', remote bdaddr 00:0e:07:a4:c8:f6
hcsecd[694]: Updating link key for the entry, remote bdaddr 00:0e:07:a4:c8:f6, name 'blobi', link key doesn't exist
```

* check whether DUN profile is supported in your remote device or not
this is the sample output of my Sony Ericsson T630
```
Record Handle: 0×00010000
Service Class ID List:
Dial-Up Networking (0×1103)
Generic Networking (0×1201)
Protocol Descriptor List:
L2CAP (0×0100)
RFCOMM (0×0003)
Protocol specific parameter #1: u/int8/bool 1
Bluetooth Profile Descriptor List:
Dial-Up Networking (0×1103) ver. 1.0

..deleted to save space..
```

* Add gprs connection definition in /etc/ppp/ppp.conf as shown below:
```
gprs:
enable force-scripts
set authname wap
set authkey wap123
set phone "*99***1#"
set login
set timeout 0
enable dns
set ifaddr 0 0
add default HISADDR
```

In this example, I use GPRS from Telkomsel with username "wap" and password "wap123"

* run the rfcomm_pppd daemon
```
amnesiac#rfcomm_ppd -c -a 00:0e:07:a4:c8:f6 -c -C dun -l gprs
```

this daemon will automatically dial the gprs connection based on label called "gprs" which has been defined in /etc/ppp/ppp.conf

* verify your connection by checking your interface ip address and default route. This connection should use tun interface
This is the sample of the connection:
```
amnesiac# ifconfig
tun0: flags=8051<UP,POINTOPOINT,RUNNING,MULTICAST> mtu 1500
inet 10.128.110.190 –> 10.128.110.191 netmask 0xffffffff
Opened by PID 6178
amnesiac#
```

and the traceroute result to this website
```
amnesiac# traceroute -n rendo.no-ip.info
traceroute to rendo.no-ip.info (202.51.232.116), 64 hops max, 40 byte packets
1 10.1.10.121 452.633 ms 535.863 ms 482.915 ms
2 203.130.200.126 490.891 ms 509.901 ms 510.900 ms
3 192.168.3.105 472.909 ms 524.895 ms 493.908 ms
4 61.94.0.137 484.908 ms 515.896 ms 503.903 ms
5 218.100.27.179 656.886 ms 580.981 ms 558.778 ms
6 218.100.27.169 470.916 ms 529.872 ms 488.909 ms
7 202.51.224.1 509.899 ms 509.900 ms 503.909 ms
8 202.51.232.225 480.903 ms 518.899 ms 498.902 ms
9 202.51.232.116 480.914 ms 527.886 ms 485.906 ms
amnesiac#
```
