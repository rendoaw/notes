original source: https://community.mellanox.com/docs/DOC-1522
 
## Option 1: lldpad
 
1. Install lldpad on the server:
  - For RHEL/CentOS
```
#yum install lldpad
```
  - For Ubuntu
```
#apt-get install lldpad
```
 
2. Run the LLDP Daemon:
```
#lldpad -d
```
 
3. Run the following script:
```
for i in `ls /sys/class/net/ | grep eth` ;
      do echo "enabling lldp for interface: $i" ;
      lldptool set-lldp -i $i adminStatus=rxtx  ;
      lldptool -T -i $i -V  sysName enableTx=yes;
      lldptool -T -i $i -V  portDesc enableTx=yes ;
      lldptool -T -i $i -V  sysDesc enableTx=yes;
      lldptool -T -i $i -V sysCap enableTx=yes;
      lldptool -T -i $i -V mngAddr enableTx=yes;
done
```
 
Note: for RHEL 7 the interface name doesn't contain "eth" but "enp"  (or similar) to the grep should be "grep enp".
 
Note: in case you use lldpad and wish to pass the management address via LLDP TLV on specific interface, you need to add this specifically.
Otherwise, only the hostname will pass via LLDP TLV.
 
For example:
```
# lldptool -T -i eth2 -V mngAddr ipv4=192.168.24.185
```
 
## Option 2: lldpd
 
Another possible LLDP linux application is called lldpd (not lldpad)
This version of LLDP doesn't require and specific configuration, it sends the TLVs by default. including the management address.
 
- For RHEL/CentoOS
There is no yum inventory For RHEL/CentOS for this application, need to download the install the rpm (there are several location on the web for that) and then to restart the application.
Here is a link to download the llapd.
```
#/etc/init.d/lldpd restart
```
  - For Ubuntu
```
#apt-get install lldpad
#/etc/init.d/lldpd restart
```
 
Once lldpad or lldpd are installed, make sure SNMP is running:
```
# /etc/init.d/snmpd start
Starting snmpd (via systemctl):                            [  OK  ]
```
 
