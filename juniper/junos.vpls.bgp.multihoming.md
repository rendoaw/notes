
## Configuration

### Overview

* basic configuration
    * PE12 multihome with PE14 with site id = 1
        * PE12 has preference 200
        * PE14 has preference 400. This config should make this router as the preferred PE.
    * PE11 multihome with PE17 with site id = 2
        * no explicit preference configured. By default lower router-id should be preferred.
    * PE-CE @site 1 is using vlan 949 and PE-CE @site 2 is using vlan 950. Therefore, vlan mapping is used to connect them. To show different mapping solution, two different mechanism are being used:
        * at site 1, vlan-id is configured on routing-instance to allow automatic vlan push/pop/swap
        * at site 2, input-vlan-map and output-vlan-map is configured on PE-CE interface
* Optional configuration 
    * Additional dummy site is configured on each PE to demonstrate always on pseudowire feature to imporve failover time.
        * PE11 @ site 2 is configured with site id 11
        * PE17 @ site 2 is configured with site id 17
        * PE12 @ site 1 is configured with site id 12
        * PE14 @ site 1 is configured with site id 14
    * dummy site configuration configured with "best-site" keyword and has no PE-CE interface associated with it. This is to make sure the dummy site is always up.

### Router Configuration 

* PE1
    
    ```
    rwibawa@vmx-13-11# show interfaces ge-0/0/0 unit 950
    apply-groups-except interface-group;
    encapsulation vlan-vpls;
    vlan-id 950;
    input-vlan-map {
        swap;
        vlan-id 951;
    }
    output-vlan-map swap;
    family vpls;
    
    
    rwibawa@vmx-13-11# show routing-instances VPLS3
    instance-type vpls;
    interface ge-0/0/0.950;
    route-distinguisher 67.176.255.1:766;
    vrf-target target:7041:776;
    protocols {
        vpls {
            site-range 20;
            no-tunnel-services;
            site 2 {
                site-identifier 2;
                multi-homing;
                interface ge-0/0/0.950;
            }
            site 11 {
                site-identifier 11;
                best-site;
            }
            mac-flush;
        }
    }
    ```
    
* PE17

    ```
    rwibawa@vmx-13-17# show interfaces ge-0/0/0.950
    apply-groups-except interface-group;
    encapsulation vlan-vpls;
    vlan-id 950;
    input-vlan-map {
        swap;
        vlan-id 951;
    }
    output-vlan-map swap;
    family vpls;
    
    
    rwibawa@vmx-13-17# show routing-instances VPLS3
    instance-type vpls;
    interface ge-0/0/0.950;
    route-distinguisher 67.176.255.7:766;
    vrf-target target:7041:776;
    protocols {
        vpls {
            site-range 20;
            no-tunnel-services;
            site 2 {
                site-identifier 2;
                multi-homing;
                interface ge-0/0/0.950;
            }
            site 17 {
                site-identifier 17;
                best-site;
            }
            mac-flush;
        }
    }
    ```

* PE12

    ```
    rwibawa@vmx-13-12# show interfaces ge-0/0/0.949
    apply-groups-except interface-group;
    encapsulation vlan-vpls;
    vlan-id 949;
    family vpls;
    
    
    rwibawa@vmx-13-12# show routing-instances VPLS3
    instance-type vpls;
    vlan-id 951;
    interface ge-0/0/0.949;
    route-distinguisher 67.176.255.2:766;
    vrf-target target:7041:776;
    protocols {
        vpls {
            no-tunnel-services;
            site 1 {
                site-identifier 1;
                multi-homing;
                site-preference 200;
                interface ge-0/0/0.949;
            }
            site 12 {
                site-identifier 12;
                best-site;
            }
            mac-flush;
        }
    }
    ```

* PE14
    
    ```
    rwibawa@vmx-13-14# show interfaces ge-0/0/0.949
    apply-groups-except interface-group;
    encapsulation vlan-vpls;
    vlan-id 949;
    family vpls;
    
    rwibawa@vmx-13-14# show routing-instances VPLS3
    instance-type vpls;
    vlan-id 951;
    interface ge-0/0/0.949;
    route-distinguisher 67.176.255.4:766;
    vrf-target target:7041:776;
    protocols {
        vpls {
            no-tunnel-services;
            site 1 {
                site-identifier 1;
                multi-homing;
                site-preference 300;
                interface ge-0/0/0.949;
            }
            site 14 {
                site-identifier 14;
                best-site;
            }
            mac-flush;
        }
    }
    ```
    
## Verification

* All PE has full-mesh pseudo-wire for dummy site

* PE11

    ```
    rwibawa@vmx-13-11# run show vpls connections instance VPLS3 extensive
    Layer-2 VPN connections:
    
    Legend for connection status (St)
    EI -- encapsulation invalid      NC -- interface encapsulation not CCC/TCC/VPLS
    EM -- encapsulation mismatch     WE -- interface and instance encaps not same
    VC-Dn -- Virtual circuit down    NP -- interface hardware not present
    CM -- control-word mismatch      -> -- only outbound connection is up
    CN -- circuit not provisioned    <- -- only inbound connection is up
    OR -- out of range               Up -- operational
    OL -- no outgoing label          Dn -- down
    LD -- local site signaled down   CF -- call admission control failure
    RD -- remote site signaled down  SC -- local and remote site ID collision
    LN -- local site not designated  LM -- local site ID not minimum designated
    RN -- remote site not designated RM -- remote site ID not minimum designated
    XX -- unknown connection status  IL -- no incoming label
    MM -- MTU mismatch               MI -- Mesh-Group ID not available
    BK -- Backup connection          ST -- Standby connection
    PF -- Profile parse failure      PB -- Profile busy
    RS -- remote site standby        SN -- Static Neighbor
    LB -- Local site not best-site   RB -- Remote site not best-site
    VM -- VLAN ID mismatch
    
    Legend for interface status
    Up -- operational
    Dn -- down
    
    Instance: VPLS3
    Edge protection: Not-Primary
      Local site: 2 (2)
        Number of local interfaces: 1
        Number of local interfaces up: 1
        IRB interface present: no
        ge-0/0/0.950
        Label-base        Offset     Size  Range     Preference
        262505            1          8      8         100
        Label-base        Offset     Size  Range     Preference
        262529            9          8      6         100
        Label-base        Offset     Size  Range     Preference
        262521            17         8      1         100
        connection-site           Type  St     Time last up          # Up trans
        1                         rmt   LB
        2                         rmt   RN
        12                        rmt   LB
        14                        rmt   LB
        17                        rmt   LB
      Local site: 11 (11)
        Number of local interfaces: 0
        Number of local interfaces up: 0
        IRB interface present: no
        lsi.1048924         12        Intf - vpls VPLS3 local site 11 remote site 12
        lsi.1048922         14        Intf - vpls VPLS3 local site 11 remote site 14
        lsi.1048923         17        Intf - vpls VPLS3 local site 11 remote site 17
        Label-base        Offset     Size  Range     Preference
        262537            1          8      2         100
        Label-base        Offset     Size  Range     Preference
        262513            9          8      8         100
        Label-base        Offset     Size  Range     Preference
        262545            17         8      1         100
        connection-site           Type  St     Time last up          # Up trans
        1                         rmt   RB
        2                         rmt   RN
        12                        rmt   Up     Oct 21 01:15:01 2015           1
          Remote PE: 67.176.255.2, Negotiated control-word: No
          Incoming label: 262516, Outgoing label: 262179
          Local interface: lsi.1048924, Status: Up, Encapsulation: VPLS
            Description: Intf - vpls VPLS3 local site 11 remote site 12
        Connection History:
            Oct 21 01:15:01 2015  status update timer
            Oct 21 01:15:01 2015  loc intf up                  lsi.1048924
            Oct 21 01:15:01 2015  PE route changed
            Oct 21 01:15:01 2015  Out lbl Update                    262179
            Oct 21 01:15:01 2015  In lbl Update                     262516
            Oct 21 01:15:01 2015  loc intf down
        14                        rmt   Up     Oct 21 01:14:04 2015           1
          Remote PE: 67.176.255.4, Negotiated control-word: No
          Incoming label: 262518, Outgoing label: 262475
          Local interface: lsi.1048922, Status: Up, Encapsulation: VPLS
            Description: Intf - vpls VPLS3 local site 11 remote site 14
        Connection History:
            Oct 21 01:14:04 2015  status update timer
            Oct 21 01:14:04 2015  loc intf up                  lsi.1048922
            Oct 21 01:14:04 2015  PE route changed
            Oct 21 01:14:04 2015  Out lbl Update                    262475
            Oct 21 01:14:04 2015  In lbl Update                     262518
            Oct 21 01:14:04 2015  loc intf down
        17                        rmt   Up     Oct 21 01:14:04 2015           1
          Remote PE: 67.176.255.7, Negotiated control-word: No
          Incoming label: 262545, Outgoing label: 262483
          Local interface: lsi.1048923, Status: Up, Encapsulation: VPLS
            Description: Intf - vpls VPLS3 local site 11 remote site 17
        Connection History:
            Oct 21 01:14:04 2015  status update timer
            Oct 21 01:14:04 2015  loc intf up                  lsi.1048923
            Oct 21 01:14:04 2015  PE route changed
            Oct 21 01:14:04 2015  Out lbl Update                    262483
            Oct 21 01:14:04 2015  In lbl Update                     262545
            Oct 21 01:14:04 2015  loc intf down
    
    [edit]
    rwibawa@vmx-13-11#
    ```

* PE17, ge-0/0/0.950 marked as VC-Down, means this PE is not the active one

    ```
    rwibawa@vmx-13-17# run show vpls connections instance VPLS3 extensive
    Layer-2 VPN connections:
    
    Legend for connection status (St)
    EI -- encapsulation invalid      NC -- interface encapsulation not CCC/TCC/VPLS
    EM -- encapsulation mismatch     WE -- interface and instance encaps not same
    VC-Dn -- Virtual circuit down    NP -- interface hardware not present
    CM -- control-word mismatch      -> -- only outbound connection is up
    CN -- circuit not provisioned    <- -- only inbound connection is up
    OR -- out of range               Up -- operational
    OL -- no outgoing label          Dn -- down
    LD -- local site signaled down   CF -- call admission control failure
    RD -- remote site signaled down  SC -- local and remote site ID collision
    LN -- local site not designated  LM -- local site ID not minimum designated
    RN -- remote site not designated RM -- remote site ID not minimum designated
    XX -- unknown connection status  IL -- no incoming label
    MM -- MTU mismatch               MI -- Mesh-Group ID not available
    BK -- Backup connection          ST -- Standby connection
    PF -- Profile parse failure      PB -- Profile busy
    RS -- remote site standby        SN -- Static Neighbor
    LB -- Local site not best-site   RB -- Remote site not best-site
    VM -- VLAN ID mismatch
    
    Legend for interface status
    Up -- operational
    Dn -- down
    
    Instance: VPLS3
    Edge protection: Not-Primary
      Local site: 2 (2)
        Number of local interfaces: 1
        Number of local interfaces up: 1
        IRB interface present: no
        ge-0/0/0.950
            Interface flags: VC-Down
        Label-base        Offset     Size  Range     Preference
        262449            1          8      8         100
        Label-base        Offset     Size  Range     Preference
        262473            9          8      6         100
        connection-site           Type  St     Time last up          # Up trans
        1                         rmt   LN
        2                         rmt   LN
        11                        rmt   LN
        12                        rmt   LN
        14                        rmt   LN
      Local site: 17 (17)
        Number of local interfaces: 0
        Number of local interfaces up: 0
        IRB interface present: no
        lsi.1048612         11        Intf - vpls VPLS3 local site 17 remote site 11
        lsi.1048613         12        Intf - vpls VPLS3 local site 17 remote site 12
        lsi.1048611         14        Intf - vpls VPLS3 local site 17 remote site 14
        Label-base        Offset     Size  Range     Preference
        262465            1          8      2         100
        Label-base        Offset     Size  Range     Preference
        262481            9          8      6         100
        Label-base        Offset     Size  Range     Preference
        262457            17         8      8         100
        connection-site           Type  St     Time last up          # Up trans
        1                         rmt   RB
        2                         rmt   RB
        11                        rmt   Up     Oct 21 01:14:04 2015           1
          Remote PE: 67.176.255.1, Negotiated control-word: No
          Incoming label: 262483, Outgoing label: 262545
          Local interface: lsi.1048612, Status: Up, Encapsulation: VPLS
            Description: Intf - vpls VPLS3 local site 17 remote site 11
        Connection History:
            Oct 21 01:14:04 2015  status update timer
            Oct 21 01:14:04 2015  loc intf up                  lsi.1048612
            Oct 21 01:14:04 2015  PE route changed
            Oct 21 01:14:04 2015  Out lbl Update                    262545
            Oct 21 01:14:04 2015  In lbl Update                     262483
            Oct 21 01:14:04 2015  loc intf down
        12                        rmt   Up     Oct 21 01:15:02 2015           1
          Remote PE: 67.176.255.2, Negotiated control-word: No
          Incoming label: 262484, Outgoing label: 262209
          Local interface: lsi.1048613, Status: Up, Encapsulation: VPLS
            Description: Intf - vpls VPLS3 local site 17 remote site 12
        Connection History:
            Oct 21 01:15:02 2015  status update timer
            Oct 21 01:15:02 2015  loc intf up                  lsi.1048613
            Oct 21 01:15:02 2015  PE route changed
            Oct 21 01:15:02 2015  Out lbl Update                    262209
            Oct 21 01:15:02 2015  In lbl Update                     262484
            Oct 21 01:15:02 2015  loc intf down
        14                        rmt   Up     Oct 21 01:10:08 2015           1
          Remote PE: 67.176.255.4, Negotiated control-word: No
          Incoming label: 262486, Outgoing label: 262505
          Local interface: lsi.1048611, Status: Up, Encapsulation: VPLS
            Description: Intf - vpls VPLS3 local site 17 remote site 14
        Connection History:
            Oct 21 01:10:08 2015  status update timer
            Oct 21 01:10:08 2015  loc intf up                  lsi.1048611
            Oct 21 01:10:08 2015  PE route changed
            Oct 21 01:10:08 2015  Out lbl Update                    262505
            Oct 21 01:10:08 2015  In lbl Update                     262486
            Oct 21 01:10:08 2015  loc intf down
    
    ```

* PE12, ge-0/0/0.949 marked as VC-Down, means this PE is currently not the active one

    ```
    rwibawa@vmx-13-12# run show vpls connections instance VPLS3 extensive
    Layer-2 VPN connections:
    
    Legend for connection status (St)
    EI -- encapsulation invalid      NC -- interface encapsulation not CCC/TCC/VPLS
    EM -- encapsulation mismatch     WE -- interface and instance encaps not same
    VC-Dn -- Virtual circuit down    NP -- interface hardware not present
    CM -- control-word mismatch      -> -- only outbound connection is up
    CN -- circuit not provisioned    <- -- only inbound connection is up
    OR -- out of range               Up -- operational
    OL -- no outgoing label          Dn -- down
    LD -- local site signaled down   CF -- call admission control failure
    RD -- remote site signaled down  SC -- local and remote site ID collision
    LN -- local site not designated  LM -- local site ID not minimum designated
    RN -- remote site not designated RM -- remote site ID not minimum designated
    XX -- unknown connection status  IL -- no incoming label
    MM -- MTU mismatch               MI -- Mesh-Group ID not available
    BK -- Backup connection          ST -- Standby connection
    PF -- Profile parse failure      PB -- Profile busy
    RS -- remote site standby        SN -- Static Neighbor
    LB -- Local site not best-site   RB -- Remote site not best-site
    VM -- VLAN ID mismatch
    
    Legend for interface status
    Up -- operational
    Dn -- down
    
    Instance: VPLS3
    Edge protection: Not-Primary
      Local site: 1 (1)
        Number of local interfaces: 1
        Number of local interfaces up: 1
        IRB interface present: no
        ge-0/0/0.949
            Interface flags: VC-Down
        Label-base        Offset     Size  Range     Preference
        262169            1          8      8         200
        Label-base        Offset     Size  Range     Preference
        262193            9          8      6         200
        Label-base        Offset     Size  Range     Preference
        262201            17         8      1         200
        connection-site           Type  St     Time last up          # Up trans
        1                         rmt   LN
        2                         rmt   LN
        11                        rmt   LN
        14                        rmt   LN
        17                        rmt   LN
      Local site: 12 (12)
        Number of local interfaces: 0
        Number of local interfaces up: 0
        IRB interface present: no
        lsi.1049600         11        Intf - vpls VPLS3 local site 12 remote site 11
        lsi.1049601         14        Intf - vpls VPLS3 local site 12 remote site 14
        lsi.1049602         17        Intf - vpls VPLS3 local site 12 remote site 17
        Label-base        Offset     Size  Range     Preference
        262185            1          8      2         100
        Label-base        Offset     Size  Range     Preference
        262177            9          8      8         100
        Label-base        Offset     Size  Range     Preference
        262209            17         8      1         100
        connection-site           Type  St     Time last up          # Up trans
        1                         rmt   RB
        2                         rmt   RB
        11                        rmt   Up     Oct 21 01:14:56 2015           1
          Remote PE: 67.176.255.1, Negotiated control-word: No
          Incoming label: 262179, Outgoing label: 262516
          Local interface: lsi.1049600, Status: Up, Encapsulation: VPLS
            Description: Intf - vpls VPLS3 local site 12 remote site 11
        Connection History:
            Oct 21 01:14:56 2015  status update timer
            Oct 21 01:14:56 2015  loc intf up                  lsi.1049600
            Oct 21 01:14:56 2015  PE route changed
            Oct 21 01:14:56 2015  Out lbl Update                    262516
            Oct 21 01:14:56 2015  In lbl Update                     262179
            Oct 21 01:14:56 2015  loc intf down
        14                        rmt   Up     Oct 21 01:14:56 2015           1
          Remote PE: 67.176.255.4, Negotiated control-word: No
          Incoming label: 262182, Outgoing label: 262476
          Local interface: lsi.1049601, Status: Up, Encapsulation: VPLS
            Description: Intf - vpls VPLS3 local site 12 remote site 14
        Connection History:
            Oct 21 01:14:56 2015  status update timer
            Oct 21 01:14:56 2015  loc intf up                  lsi.1049601
            Oct 21 01:14:56 2015  PE route changed
            Oct 21 01:14:56 2015  Out lbl Update                    262476
            Oct 21 01:14:56 2015  In lbl Update                     262182
            Oct 21 01:14:56 2015  loc intf down
        17                        rmt   Up     Oct 21 01:14:56 2015           1
          Remote PE: 67.176.255.7, Negotiated control-word: No
          Incoming label: 262209, Outgoing label: 262484
          Local interface: lsi.1049602, Status: Up, Encapsulation: VPLS
            Description: Intf - vpls VPLS3 local site 12 remote site 17
        Connection History:
            Oct 21 01:14:56 2015  status update timer
            Oct 21 01:14:56 2015  loc intf up                  lsi.1049602
            Oct 21 01:14:56 2015  PE route changed
            Oct 21 01:14:56 2015  Out lbl Update                    262484
            Oct 21 01:14:56 2015  In lbl Update                     262209
            Oct 21 01:14:56 2015  loc intf down
    
    ```

* PE14

    ```
    rwibawa@vmx-13-14# run show vpls connections instance VPLS3 extensive
    Layer-2 VPN connections:
    
    Legend for connection status (St)
    EI -- encapsulation invalid      NC -- interface encapsulation not CCC/TCC/VPLS
    EM -- encapsulation mismatch     WE -- interface and instance encaps not same
    VC-Dn -- Virtual circuit down    NP -- interface hardware not present
    CM -- control-word mismatch      -> -- only outbound connection is up
    CN -- circuit not provisioned    <- -- only inbound connection is up
    OR -- out of range               Up -- operational
    OL -- no outgoing label          Dn -- down
    LD -- local site signaled down   CF -- call admission control failure
    RD -- remote site signaled down  SC -- local and remote site ID collision
    LN -- local site not designated  LM -- local site ID not minimum designated
    RN -- remote site not designated RM -- remote site ID not minimum designated
    XX -- unknown connection status  IL -- no incoming label
    MM -- MTU mismatch               MI -- Mesh-Group ID not available
    BK -- Backup connection          ST -- Standby connection
    PF -- Profile parse failure      PB -- Profile busy
    RS -- remote site standby        SN -- Static Neighbor
    LB -- Local site not best-site   RB -- Remote site not best-site
    VM -- VLAN ID mismatch
    
    Legend for interface status
    Up -- operational
    Dn -- down
    
    Instance: VPLS3
    Edge protection: Not-Primary
      Local site: 1 (1)
        Number of local interfaces: 1
        Number of local interfaces up: 1
        IRB interface present: no
        ge-0/0/0.949
        Label-base        Offset     Size  Range     Preference
        262465            1          8      8         300
        Label-base        Offset     Size  Range     Preference
        262481            9          8      4         300
        Label-base        Offset     Size  Range     Preference
        262489            17         8      1         300
        connection-site           Type  St     Time last up          # Up trans
        1                         rmt   RN
        2                         rmt   LB
        11                        rmt   LB
        12                        rmt   LB
        17                        rmt   LB
      Local site: 14 (14)
        Number of local interfaces: 0
        Number of local interfaces up: 0
        IRB interface present: no
        lsi.1048607         11        Intf - vpls VPLS3 local site 14 remote site 11
        lsi.1048608         12        Intf - vpls VPLS3 local site 14 remote site 12
        lsi.1048605         17        Intf - vpls VPLS3 local site 14 remote site 17
        Label-base        Offset     Size  Range     Preference
        262497            1          8      2         100
        Label-base        Offset     Size  Range     Preference
        262473            9          8      8         100
        Label-base        Offset     Size  Range     Preference
        262505            17         8      1         100
        connection-site           Type  St     Time last up          # Up trans
        1                         rmt   RN
        2                         rmt   RB
        11                        rmt   Up     Oct 21 01:14:04 2015           1
          Remote PE: 67.176.255.1, Negotiated control-word: No
          Incoming label: 262475, Outgoing label: 262518
          Local interface: lsi.1048607, Status: Up, Encapsulation: VPLS
            Description: Intf - vpls VPLS3 local site 14 remote site 11
        Connection History:
            Oct 21 01:14:04 2015  status update timer
            Oct 21 01:14:04 2015  loc intf up                  lsi.1048607
            Oct 21 01:14:04 2015  PE route changed
            Oct 21 01:14:04 2015  Out lbl Update                    262518
            Oct 21 01:14:04 2015  In lbl Update                     262475
            Oct 21 01:14:04 2015  loc intf down
        12                        rmt   Up     Oct 21 01:15:02 2015           1
          Remote PE: 67.176.255.2, Negotiated control-word: No
          Incoming label: 262476, Outgoing label: 262182
          Local interface: lsi.1048608, Status: Up, Encapsulation: VPLS
            Description: Intf - vpls VPLS3 local site 14 remote site 12
        Connection History:
            Oct 21 01:15:02 2015  status update timer
            Oct 21 01:15:02 2015  loc intf up                  lsi.1048608
            Oct 21 01:15:02 2015  PE route changed
            Oct 21 01:15:02 2015  Out lbl Update                    262182
            Oct 21 01:15:02 2015  In lbl Update                     262476
            Oct 21 01:15:02 2015  loc intf down
        17                        rmt   Up     Oct 21 01:10:09 2015           1
          Remote PE: 67.176.255.7, Negotiated control-word: No
          Incoming label: 262505, Outgoing label: 262486
          Local interface: lsi.1048605, Status: Up, Encapsulation: VPLS
            Description: Intf - vpls VPLS3 local site 14 remote site 17
        Connection History:
            Oct 21 01:10:09 2015  status update timer
            Oct 21 01:10:09 2015  loc intf up                  lsi.1048605
            Oct 21 01:10:09 2015  PE route changed
            Oct 21 01:10:09 2015  Out lbl Update                    262486
            Oct 21 01:10:09 2015  In lbl Update                     262505
            Oct 21 01:10:09 2015  loc intf down
            
    ```
    
### How to find the active remote PE

* for local-site, as shown above, we know whether this PE is the active/master or not by checking the VC flag on the PE-CE interface
* for remote-site, based on the output below, we are trying to find which one is the active PE for site 2
* the following output shows that the remote CE MAC address is tied with __lsi.1048607__ interface
* by looking at the "show vpls connections instance VPLS3" output of PE14 above, we know that __lsi.1048607__ is going to PE11. This means, PE11 is the remote active PE.
* sample output:

    ```
    rwibawa@vmx-13-14# run show vpls mac-table
    
    MAC flags       (S -static MAC, D -dynamic MAC, L -locally learned, C -Control MAC
        O -OVSDB MAC, SE -Statistics enabled, NM -Non configured MAC, R -Remote PE MAC)
    
    Routing instance : VPLS3
     Bridging domain : __VPLS3__, VLAN : 951
       MAC                 MAC      Logical          NH     RTR
       address             flags    interface        Index  ID
       00:50:58:13:13:04   D        lsi.1048607
       00:50:58:13:19:04   D        ge-0/0/0.949
       
       
    rwibawa@vmx-13-14# run show vpls connections instance VPLS3
    ...
    
    Instance: VPLS3
    Edge protection: Not-Primary
      Local site: 1 (1)
        connection-site           Type  St     Time last up          # Up trans
        1                         rmt   RN
        2                         rmt   LB
        11                        rmt   LB
        12                        rmt   LB
        17                        rmt   LB
      Local site: 14 (14)
        connection-site           Type  St     Time last up          # Up trans
        1                         rmt   RN
        2                         rmt   RB
        11                        rmt   Up     Oct 21 01:14:04 2015           1
          Remote PE: 67.176.255.1, Negotiated control-word: No
          Incoming label: 262475, Outgoing label: 262518
          Local interface: lsi.1048607, Status: Up, Encapsulation: VPLS     ---------------> lsi interface 
            Description: Intf - vpls VPLS3 local site 14 remote site 11
    ...


