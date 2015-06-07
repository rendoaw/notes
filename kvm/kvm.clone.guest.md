original source: http://unix.stackexchange.com/questions/8351/how-to-create-a-dupe-of-a-kvm-libvirt-virt-manager-vm

```
# You cannot "clone" a running vm, stop it.  suspend and destroy
# are also valid options for less graceful cloning
virsh shutdown this.vm

# copy the storage.
cp /var/lib/libvirt/images/{this-vm,that-vm}.img

# dump the xml for the original
virsh dumpxml this-vm > /tmp/that-vm.xml

# hardware addresses need to be removed, libvirt will assign
# new addresses automatically
sed -i /uuid/d /tmp/that-vm.xml
sed -i '/mac address/d' /tmp/that-vm.xml

# and actually rename the vm: (this also updates the storage path)
sed -i s/this-vm/that-vm /tmp/that-vm.xml

# finally, create the new vm
virsh define /tmp/that-vm.xml
virsh start this-vm
virsh start that-vm
```