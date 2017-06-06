# How to resize VM image

This is the procedure to resize a VM image that has single flat primary partition.

* resize the disk image

  ```
  # qemu-img resize <vmname>.qcow2 +<additional new size>G
  
  or
  
  # qemu-img resize <vmname>.qcow2 <new size>G
  ```


* resize the partition table (make sure DOS Compatibility flag is not set and display units is sectors)

  ```
  # fdisk <disk name>
  
  # fdisk /dev/vda
  
  WARNING: DOS-compatible mode is deprecated. It's strongly recommended to
          switch off the mode (command 'c') and change display units to
          sectors (command 'u').
  
  Command (m for help): c
  DOS Compatibility flag is not set  -------> WARNING! some linux version has DOS Compatibility is already unset
  
  Command (m for help): u
  Changing display/entry units to sectors    -------> WARNING! some linux version has unit set as sector by default
  
  Command (m for help): p
  
  Disk /dev/vda: 85.9 GB, 85899345920 bytes
  255 heads, 63 sectors/track, 10443 cylinders, total 167772160 sectors
  Units = sectors of 1 * 512 = 512 bytes
  Sector size (logical/physical): 512 bytes / 512 bytes
  I/O size (minimum/optimal): 512 bytes / 512 bytes
  Disk identifier: 0x00050c05
  
  Device Boot      Start         End      Blocks   Id  System
  /dev/vda1   *        2048    16777215     8387584   83  Linux
  
  Command (m for help): d
  Selected partition 1
  
  Command (m for help): n
  Command action
  e   extended
  p   primary partition (1-4)
  p
  Partition number (1-4): 1
  First sector (2048-167772159, default 2048):
  Using default value 2048
  Last sector, +sectors or +size{K,M,G} (2048-167772159, default 167772159):
  Using default value 167772159
  
  Command (m for help): w
  The partition table has been altered!
  
  Calling ioctl() to re-read partition table.
  
  WARNING: Re-reading the partition table failed with error 16: Device or resource busy.
  The kernel still uses the old table. The new table will be used at
  the next reboot or after you run partprobe(8) or kpartx(8)
  Syncing disks.
  #
  ```

* resize filesystem

```
# resize2fs <partition name>
# resize2fs /dev/vda1
```

