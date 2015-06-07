original source: http://stackoverflow.com/questions/26716722/tcp-receives-packets-but-it-ignores-them

# TCP receives packets, but it ignores them

The problem was that I disabled the TSO (tcp-segmentation-offload) on the virtual bridge to which my Dockers are attached with the command:
```
ethtool -K IFACE_NAME tso off
```
It turns off only TSO, whereas the checksumming offload remains on. Evidently, this creates some problem and though Wireshark showed me that TCP checksum was OK, actually it wasn't. So the host ignored the packet due to the bad TCP checksum.

To turn off TSO and checksumming too, I just used the command:
```
ethtool --offload IFACE_NAME rx off tx off
```
And now everything works.