# How to enable nested KVM

## Ubuntu
Check if nested is enabled
```
cat /sys/module/kvm_intel/parameters/nested
N
```
Enable nested in Intel based chip
```
sudo rmmod kvm-intel
sudo sh -c "echo 'options kvm-intel nested=y' >> /etc/modprobe.d/dist.conf"
sudo modprobe kvm-intel
```

Enable nested in AMD
```
sudo rmmod kvm-amd
sudo sh -c "echo 'options amd nested=1' >> /etc/modprobe.d/dist.conf"
sudo modprobe kvm-amd
```

## Centos
install Kernel 3.x, either from elrepo or from Xen kernel

### using xen kernel
* Step 1: add the xen-c6 repo to your system
```
su -
cd /etc/yum.repos.d
wget http://dev.centos.org/centos/6/xen-c6/xen-c6.repo
yum repolist
[optional] vi xen-c6.repo : change to "enabled=0" to not take the repo enabled by default
```

* Step 2: install the new kernel
```
su -
yum --enablerepo xen-c6 install kernel kernel-firmware
vi /boot/grub/grub.conf : add "kvm-intel.nested=1" to the end of the kernel line
reboot
verify proper operation: "cat /sys/module/kvm_intel/parameters/nested" will output "Y"
```

### using elrepo 
* Enable ELRepo Project repository
```
rpm --import https://www.elrepo.org/RPM-GPG-KEY-elrepo.org
rpm -Uvh http://www.elrepo.org/elrepo-release-6-6.el6.elrepo.noarch.rpm
```

* Install the kernel
```
yum --enablerepo=elrepo-kernel install kernel-lt
```

* configure grub
You also need edit /etc/grub.conf to change the kernel order, change default from 1 to 0, must looks like the below:
```
default=0
timeout=5
splashimage=(hd0,0)/grub/splash.xpm.gz
hiddenmenu
title CentOS (3.10.55-1.el6.elrepo.x86_64)
  root (hd0,0)
  kernel /vmlinuz-3.10.55-1.el6.elrepo.x86_64 ro root=/dev/mapper/VolGroup-lv_root rd_NO_LUKS LANG=en_US.UTF-8 rd_NO_MD rd_LVM_LV=VolGroup/lv_swap SYSFONT=latarcyrheb-sun16 crashkernel=auto rd_LVM_LV=VolGroup/lv_root rd_NO_DM  KEYBOARDTYPE=pc KEYTABLE=br-abnt2 rhgb quiet
```


## Modify guest VM to support nested
For the setup to work, we need the "vmx" flag in the virtual cpu inside the VM.
* Option 1: using virt-manager
```
virt-manager
open the hypervisor virtual machine, go to Details > Processor
unfold the "Configuration"
press the "Copy host CPU configuration" button
unfold the "CPU Features"
verify the "vmx" feature is set to "require"
press Apply
```

* Option 2: using virsh
```
sudo virsh edit <vm name>
<cpu mode='host-passthrough'>
</cpu>
```
