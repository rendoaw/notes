1. Register/Un-register VM
```
vim-cmd solo/registervm /vmfs/volumes/datastore1/linux.vmx
vim-cmd solo/unregister <vmid>
```

2. create vswitch (not dv switch)
```
execute from esx host: vicfg-vswitch -a <vswitchname> 
execute from vsphere or VMA: vicfg-vswitch -a <vswitchname> --vihost <esxi host>
```

3. create port group on vswitch
```
execute from esx host: vicfg-vswitch --add-pg <portgroupname> <vswitchname>
execute from vsphere or VMA: vicfg-vswitch --vihost <esxi host> --add-pg <portgroupname> <vswitchname>
```

4. assign vlan to port group on vswitch
```
execute from esx host: vicfg-vswitch --pg <portgroupname> <vswitchname> --vlan <vlanid>
execute from vsphere or VMA: vicfg-vswitch --vihost <esxi host> --pg <portgroupname> <vswitchname> --vlan <vlanid>
```

5. clone VM
* shutdown the VM that want to be cloned
* copy the whole folder to a new folder
* go to the new folder
* modify vmx file
** change display name to a new name
* register the VM (see above)
