# Some ESXi related commands

* add static route

    ```
    esxcfg-route -a 192.168.100.0 255.255.255.0 192.168.0.1
    ```

* list partition

    ```
    ~ # ls /vmfs/devices/disks/
    ....
    t10.ATA_____ST91000640NS________________________________________9XG8SW0  ---> main disk  vml.01000000002020202020202020202020203958473853573045535439313030:9
    t10.ATA_____ST91000640NS________________________________________9XG8SW0E:1   ----> partition 1      vml.01000000003339666463643637386664666364313736633963653930306630373064363932536572766572
    t10.ATA_____ST91000640NS________________________________________9XG8SW0E:2   -----> partition 2                  vml.01000000003339666463643637386664666364313736633963653930306630373064363932536572766572:1
    t10.ATA_____ST91000640NS________________________________________9XG8SW0E:3                    vml.01000000003638383439363366616432336131333536633963653930306630373064363932536572766572
    t10.ATA_____ST91000640NS________________________________________9XG8SW0E:5                    vml.01000000003638383439363366616432336131333536633963653930306630373064363932536572766572:1
    t10.ATA_____ST91000640NS________________________________________9XG8SW0E:6                    vml.01000000006163306439653930613138663035663336633963653930306630373064363932536572766572
    t10.ATA_____ST91000640NS________________________________________9XG8SW0E:7                    vml.01000000006163306439653930613138663035663336633963653930306630373064363932536572766572:1
    t10.ATA_____ST91000640NS________________________________________9XG8SW0E:8                    vml.01000000006336383332653337353065623066376136633963653930306630373064363932536572766572
    t10.ATA_____ST91000640NS________________________________________9XG8SW0E:9                    vml.01000000006336383332653337353065623066376136633963653930306630373064363932536572766572:1
    ~ #
    ```

* Get partition

    ```
    ~ # partedUtil getptbl /vmfs/devices/disks/t10.ATA_____ST91000640NS________________________________________9XG8SW0E
    gpt
    121601 255 63 1953525168
    1 64 8191 C12A7328F81F11D2BA4B00A0C93EC93B systemPartition 128
    5 8224 520191 EBD0A0A2B9E5443387C068B6B72699C7 linuxNative 0
    6 520224 1032191 EBD0A0A2B9E5443387C068B6B72699C7 linuxNative 0
    7 1032224 1257471 9D27538040AD11DBBF97000C2911D1B8 vmkDiagnostic 0
    8 1257504 1843199 EBD0A0A2B9E5443387C068B6B72699C7 linuxNative 0
    9 1843200 7086079 9D27538040AD11DBBF97000C2911D1B8 vmkDiagnostic 0
    2 7086080 15472639 EBD0A0A2B9E5443387C068B6B72699C7 linuxNative 0
    3 15472640 1953525134 AA31E02A400F11DB9590000C2911D1B8 vmfs 0
    ~ #
    ```

* delete partition #1

    ```
    partedUtil delete /vmfs/devices/disks/t10.ATA_____ST91000640NS________________________________________9XG8SW0E 1
    ```

* Register/Un-register VM

    ```
    vim-cmd solo/registervm /vmfs/volumes/datastore1/linux.vmx
    vim-cmd solo/unregister <vmid>
    ```

* create vswitch (not dv switch)

    ```
    execute from esx host: vicfg-vswitch -a <vswitchname> 
    execute from vsphere or VMA: vicfg-vswitch -a <vswitchname> --vihost <esxi host>
    ```

* create port group on vswitch

    ```
    execute from esx host: vicfg-vswitch --add-pg <portgroupname> <vswitchname>
    execute from vsphere or VMA: vicfg-vswitch --vihost <esxi host> --add-pg <portgroupname> <vswitchname>
    ```

* assign vlan to port group on vswitch

    ```
    execute from esx host: vicfg-vswitch --pg <portgroupname> <vswitchname> --vlan <vlanid>
    execute from vsphere or VMA: vicfg-vswitch --vihost <esxi host> --pg <portgroupname> <vswitchname> --vlan <vlanid>
    ```

* clone VM

    ```
    - shutdown the VM that want to be cloned
    - copy the whole folder to a new folder
    - go to the new folder
    -  modify vmx file
        - change display name to a new name
    - register the VM (see above)
    ```
