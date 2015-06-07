original source: https://ostechnix.wordpress.com/2013/02/03/linux-basics-lvm-logical-volume-manager-tutorial/

# Linux Basics – LVM (Logical Volume Manager) Tutorial
February 3, 2013 ~ Admin
Logical Volume Manager (LVM);

LVM is a tool for logical volume management which is used to allocating disks, striping, mirroring and resizing logical volumes. With LVM, a hard drive or set of hard drives is allocated to one or more physical volumes. LVM physical volumes can be placed on other block devices which might span two or more disks. Since a physical volume cannot span over multiple drives, to span over more than one drive, create one or more physical volumes per drive. The volume groups can be divided into logical volumes, which are assigned mount points, such as /home and / and file system types, such as ext2 or ext3 or ext4. When “partitions” reach their full capacity, free space from the volume group can be added to the logical volume to increase the size of the partition. When a new hard drive is added to the system, it can be added to the volume group, and partitions that are logical volumes can be increased in size.
On the other hand, if a system is partitioned with the ext4 file system, the hard drive is divided into partitions of defined sizes. If a partition becomes full, it is not easy to expand the size of the partition. Even if the partition is moved to another hard drive, the original hard drive space has to be reallocated as a different partition or not used.   

In this how-to tutorial let us learn some basics of LVM commands.     
Scenario: 
* Create 3 partitions of size each 100MB.
* Convert them into physical  volumes.
* Combine physical volumes into volume group.
* Finally create a logical volume from the volume group.

## Create Partitions
Use fdisk command to create and manage partions.
To view the existing partitions use following command
```
[root@server ~]# fdisk -l
Disk /dev/sdb: 8589 MB, 8589934592 bytes
255 heads, 63 sectors/track, 1044 cylinders
Units = cylinders of 16065 * 512 = 8225280 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk identifier: 0x0007b12c
   Device Boot      Start         End      Blocks   Id  System
Disk /dev/sda: 8589 MB, 8589934592 bytes
255 heads, 63 sectors/track, 1044 cylinders
Units = cylinders of 16065 * 512 = 8225280 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk identifier: 0x000ac451
   Device Boot      Start         End      Blocks   Id  System
/dev/sda1   *           1         128     1024000   83  Linux
Partition 1 does not end on cylinder boundary.
/dev/sda2             128         291     1310720   82  Linux swap / Solaris
Partition 2 does not end on cylinder boundary.
/dev/sda3             291        1045     6052864   83  Linux
```
The above output shows us two physical hard disks. The /dev/sda contains three partitions and no space to create additional partions. And the second drive /dev/sdb contains no partions yet. So let us use the second one in this tutorial.

Now let us create three partions of each size 100MB using fdisk command.
```
[root@server ~]# fdisk /dev/sdb 
WARNING: DOS-compatible mode is deprecated. It's strongly recommended to
         switch off the mode (command 'c') and change display units to
         sectors (command 'u').
Command (m for help): n
Command action
   e   extended
   p   primary partition (1-4)
p
Partition number (1-4): 1
First cylinder (1-1044, default 1): 
Using default value 1
Last cylinder, +cylinders or +size{K,M,G} (1-1044, default 1044): +100M
Command (m for help): n
Command action
   e   extended
   p   primary partition (1-4)
p
Partition number (1-4): 2
First cylinder (15-1044, default 15): 
Using default value 15
Last cylinder, +cylinders or +size{K,M,G} (15-1044, default 1044): +100M
Command (m for help): n
Command action
   e   extended
   p   primary partition (1-4)
p
Partition number (1-4): 3
First cylinder (29-1044, default 29): 
Using default value 29
Last cylinder, +cylinders or +size{K,M,G} (29-1044, default 1044): +100M
```

To check whether the partions have been created use the parameter “p”.
```
Command (m for help): p
Disk /dev/sdb: 8589 MB, 8589934592 bytes
255 heads, 63 sectors/track, 1044 cylinders
Units = cylinders of 16065 * 512 = 8225280 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk identifier: 0x0007b12c
   Device Boot      Start         End      Blocks   Id  System
/dev/sdb1               1          14      112423+  83  Linux
/dev/sdb2              15          28      112455   83  Linux
/dev/sdb3              29          42      112455   83  Linux
```

Save the newly created partions.
```
Command (m for help): w
The partition table has been altered!
Calling ioctl() to re-read partition table.
Syncing disks.
```

Update the kernel to save the changes without restarting the system.
```
[root@server ~]# partprobe 
Warning: WARNING: the kernel failed to re-read the partition table on /dev/sda (Device or resource busy).  As a result, it may not reflect all of your changes until after reboot.
```

Again we will check the existing partitions using fdisk command.
```
[root@server ~]# fdisk -l
Disk /dev/sdb: 8589 MB, 8589934592 bytes
255 heads, 63 sectors/track, 1044 cylinders
Units = cylinders of 16065 * 512 = 8225280 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk identifier: 0x0007b12c
   Device Boot      Start         End      Blocks   Id  System
/dev/sdb1               1          14      112423+  83  Linux
/dev/sdb2              15          28      112455   83  Linux
/dev/sdb3              29          42      112455   83  Linux
Disk /dev/sda: 8589 MB, 8589934592 bytes
255 heads, 63 sectors/track, 1044 cylinders
Units = cylinders of 16065 * 512 = 8225280 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk identifier: 0x000ac451
   Device Boot      Start         End      Blocks   Id  System
/dev/sda1   *           1         128     1024000   83  Linux
Partition 1 does not end on cylinder boundary.
/dev/sda2             128         291     1310720   82  Linux swap / Solaris
Partition 2 does not end on cylinder boundary.
/dev/sda3             291        1045     6052864   83  Linux
```
The above output shows three partions has been created in the /dev/sdb disk. If fdisk -l doesn’t show the output reboot to take effect.

##Create Physical Volumes
Note: If you had installed the server in the minimal mode, the commands pvcreate, lvcreate, vgcreate etc., couldn’t be found. To use that commands install the lvm2 package first.
```
[root@server ~]# yum install lvm2
Loaded plugins: rhnplugin
This system is not registered with RHN.
RHN support will be disabled.
Setting up Install ProcessThe
Resolving Dependencies
--> Running transaction check
---> Package lvm2.i686 0:2.02.72-8.el6 set to be updated
--> Processing Dependency: lvm2-libs = 2.02.72-8.el6 for package: lvm2-2.02.72-8.el6.i686
--> Processing Dependency: libdevmapper-event.so.1.02(Base) for package: lvm2-2.02.72-8.el6.i686
--> Processing Dependency: libdevmapper-event.so.1.02 for package: lvm2-2.02.72-8.el6.i686
--> Running transaction check
---> Package device-mapper-event-libs.i686 0:1.02.53-8.el6 set to be updated
---> Package lvm2-libs.i686 0:2.02.72-8.el6 set to be updated
--> Processing Dependency: device-mapper-event >= 1.02.53-8.el6 for package: lvm2-libs-2.02.72-8.el6.i686
--> Running transaction check
---> Package device-mapper-event.i686 0:1.02.53-8.el6 set to be updated
--> Finished Dependency Resolution
Dependencies Resolved
================================================================================
 Package                      Arch     Version              Repository     Size
================================================================================
Installing:
 lvm2                         i686     2.02.72-8.el6        localrepo     514 k
Installing for dependencies:
 device-mapper-event          i686     1.02.53-8.el6        localrepo      79 k
 device-mapper-event-libs     i686     1.02.53-8.el6        localrepo      74 k
 lvm2-libs                    i686     2.02.72-8.el6        localrepo     565 k
Transaction Summary
================================================================================
Install       4 Package(s)
Upgrade       0 Package(s)
Total download size: 1.2 M
Installed size: 2.5 M
Is this ok [y/N]: y
Downloading Packages:
--------------------------------------------------------------------------------
Total                                            11 MB/s | 1.2 MB     00:00     
Running rpm_check_debug
Running Transaction Test
Transaction Test Succeeded
Running Transaction
  Installing     : device-mapper-event-libs-1.02.53-8.el6.i686              1/4 
  Installing     : device-mapper-event-1.02.53-8.el6.i686                   2/4 
  Installing     : lvm2-libs-2.02.72-8.el6.i686                             3/4 
  Installing     : lvm2-2.02.72-8.el6.i686                                  4/4 
Installed:
  lvm2.i686 0:2.02.72-8.el6                                                     
Dependency Installed:
  device-mapper-event.i686 0:1.02.53-8.el6                                      
  device-mapper-event-libs.i686 0:1.02.53-8.el6                                 
  lvm2-libs.i686 0:2.02.72-8.el6                                                
Complete!
```

Now create physical volumes using the command pvcreate.
```
[root@server ~]# pvcreate /dev/sdb1 /dev/sdb2 /dev/sdb3 
  Physical volume "/dev/sdb1" successfully created
  Physical volume "/dev/sdb2" successfully created
  Physical volume "/dev/sdb3" successfully created
```

To verify the newly created physical volumes use the command pvdisplay.
```
[root@server ~]# pvdisplay 
  "/dev/sdb1" is a new physical volume of "109.79 MiB"
  --- NEW Physical volume ---
  PV Name               /dev/sdb1
  VG Name               
  PV Size               109.79 MiB
  Allocatable           NO
  PE Size               0   
  Total PE              0
  Free PE               0
  Allocated PE          0
  PV UUID               jQl5F4-DyLj-SkHu-4lhZ-J3nQ-zax9-aT8sc4
   
  "/dev/sdb2" is a new physical volume of "109.82 MiB"
  --- NEW Physical volume ---
  PV Name               /dev/sdb2
  VG Name               
  PV Size               109.82 MiB
  Allocatable           NO
  PE Size               0   
  Total PE              0
  Free PE               0
  Allocated PE          0
  PV UUID               i4MHvw-8hYB-Fwz8-fxTL-G3mu-fl5E-zGYhDO
   
  "/dev/sdb3" is a new physical volume of "109.82 MiB"
  --- NEW Physical volume ---
  PV Name               /dev/sdb3
  VG Name               
  PV Size               109.82 MiB
  Allocatable           NO
  PE Size               0   
  Total PE              0
  Free PE               0
  Allocated PE          0
  PV UUID               99qkNw-3oAw-vXwg-WE6U-zyKO-Ffs3-rDSqUY
```

##Create Volume Groups
Create a new volume group called vg1 using two physical volumes /dev/sdb1 and /dev/sdb2 using the command vgcreate.
```
[root@server ~]# vgcreate vg1 /dev/sdb1 /dev/sdb2 
  Volume group "vg1" successfully created
```

To verify the volume group has been created or not use the command vgdisplay.
```
[root@server ~]# vgdisplay 
  --- Volume group ---
  VG Name               vg1
  System ID             
  Format                lvm2
  Metadata Areas        2
  Metadata Sequence No  1
  VG Access             read/write
  VG Status             resizable
  MAX LV                0
  Cur LV                0
  Open LV               0
  Max PV                0
  Cur PV                2
  Act PV                2
  VG Size               216.00 MiB
  PE Size               4.00 MiB
  Total PE              54
  Alloc PE / Size       0 / 0   
  Free  PE / Size       54 / 216.00 MiB
  VG UUID               ds3OtP-DMUx-33nN-HDar-eqNj-uIED-41gjqI
```

##Create Logical Volume
To create logical volume use the command lvcreate. Let us create a logical volume called lv1 with size 200MB.
```
[root@server ~]# lvcreate -L 200M vg1 -n lv1
  Logical volume "lv1" created
```

Verify the logical volume is created or not using command lvdisplay.
```
[root@server ~]# lvdisplay 
  --- Logical volume ---
  LV Name                /dev/vg1/lv1
  VG Name                vg1
  LV UUID                dgLZ79-JZdn-NUSF-fUS1-YVFk-36qs-iuafhE
  LV Write Access        read/write
  LV Status              available
  # open                 0
  LV Size                200.00 MiB
  Current LE             50
  Segments               2
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     256
  Block device           253:0
```

Format and Mount the logical volume
Now format the newly created logical volume and mount it in the /mnt directory or wherever you want.
```
[root@server ~]# mkfs.ext4 /dev/vg1/lv1 
mke2fs 1.41.12 (17-May-2010)
Filesystem label=
OS type: Linux
Block size=1024 (log=0)
Fragment size=1024 (log=0)
Stride=0 blocks, Stripe width=0 blocks
51200 inodes, 204800 blocks
10240 blocks (5.00%) reserved for the super user
First data block=1
Maximum filesystem blocks=67371008
25 block groups
8192 blocks per group, 8192 fragments per group
2048 inodes per group
Superblock backups stored on blocks: 
 8193, 24577, 40961, 57345, 73729
Writing inode tables: done                            
Creating journal (4096 blocks): done
Writing superblocks and filesystem accounting information: done
This filesystem will be automatically checked every 35 mounts or
180 days, whichever comes first.  Use tune2fs -c or -i to override.
```

And mount the logical volume in the /mnt mount point.
```
[root@server ~]# mount /dev/vg1/lv1 /mnt/
```

Now the logical volume is successfully mounted in /mnt. You can use the new logical volume to store your datas.
```
[root@server ~]# cd /mnt/
[root@server mnt]# touch file1 file2 file3
[root@server mnt]# mkdir dir1 dir2 dir3
[root@server mnt]# ls
dir1  dir2  dir3  file1  file2  file3  lost+found
```

## Extend Volume Group Size
If you’re running out of the space in the logical volume, you can extend the size of it easily if your physical disk contains free space or with additional physical disk(Hard disk).
Say for example let us extend the volume group vg1 using the physical volume /dev/sdb3. And let us add additonal 100MB to logical volume lv1.
```
[root@server mnt]# vgextend vg1 /dev/sdb3 
  Volume group "vg1" successfully extended
```

Then resize the logical vloume lv1.
```
[root@server mnt]# lvresize -L +100M /dev/vg1/lv1 
  Extending logical volume lv1 to 300.00 MiB
  Logical volume lv1 successfully resized
```

Resize the filesystem of logical volume lv1.
```
[root@server mnt]# resize2fs /dev/vg1/lv1 
resize2fs 1.41.12 (17-May-2010)
Filesystem at /dev/vg1/lv1 is mounted on /mnt; on-line resizing required
old desc_blocks = 1, new_desc_blocks = 2
Performing an on-line resize of /dev/vg1/lv1 to 307200 (1k) blocks.
The filesystem on /dev/vg1/lv1 is now 307200 blocks long.
```

Now verify the new size of the logical volume lv1.
```
[root@server mnt]# lvdisplay /dev/vg1/lv1 
  --- Logical volume ---
  LV Name                /dev/vg1/lv1
  VG Name                vg1
  LV UUID                dgLZ79-JZdn-NUSF-fUS1-YVFk-36qs-iuafhE
  LV Write Access        read/write
  LV Status              available
  # open                 1
  LV Size                300.00 MiB
  Current LE             75
  Segments               3
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     256
  Block device           253:0
```

It’s done. Now the size of the logical volume lv1 is extended by 100MB.

## Remove Logical Volume
Come out of the /mnt mount point, unmount the logical volume lv1 and remove it using command lvremove.
```
[root@server mnt]# cd ..
[root@server /]# umount /mnt/
[root@server /]# lvremove /dev/vg1/lv1 
Do you really want to remove active logical volume lv1? [y/n]: y
  Logical volume "lv1" successfully removed
```

Remove Volume Group
```
[root@server /]# vgremove /dev/vg1
  Volume group "vg1" successfully removed
```

Remove Physical Volume
```
[root@server /]# pvremove /dev/sdb1 /dev/sdb2 /dev/sdb3
  Labels on physical volume "/dev/sdb1" successfully wiped
  Labels on physical volume "/dev/sdb2" successfully wiped
  Labels on physical volume "/dev/sdb3" successfully wiped
```
