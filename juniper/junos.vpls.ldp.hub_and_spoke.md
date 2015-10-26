
# Hub and Spoke LDP-based VPLS 

## Overview

* Topology
    * PE14 is HUB PE, PE11 and PE17 are the Spoke PE

* there are 2 possible HUB PE configurations:
    * one mesh-group for each neighbor
        * default behavior: JunOS will switch the traffic between mesh-group, so no additional configurtaion is required
    * one mesh-group for all neighbors
        * by default, JunOS will not switch the traffic from neighbor to the other neighbor belong to the same mesh-group.
        * to change this behavior, add "local-switching" knob.


## Configuration

### PE HUB

```
rwibawa@vmx-13-14# show routing-instances VLDP1                                             
instance-type vpls;
interface ge-0/0/0.542;
protocols {
    vpls {
        interface ge-0/0/0.542;
        no-tunnel-services;
        vpls-id 502;
        mesh-group HUB {
            local-switching;
            neighbor 67.176.255.1;
            neighbor 67.176.255.7;
        }
    }
}

rwibawa@vmx-13-14# run show vpls connections instance VLDP1  
...

Instance: VLDP1
  VPLS-id: 502
  Mesh-group connections: HUB
    Neighbor                  Type  St     Time last up          # Up trans
    67.176.255.7(vpls-id 502) rmt   Up     Oct 26 17:44:04 2015           1
      Remote PE: 67.176.255.7, Negotiated control-word: No
      Incoming label: 262165, Outgoing label: 262151
      Negotiated PW status TLV: No
      Local interface: lsi.1048700, Status: Up, Encapsulation: ETHERNET
        Description: Intf - vpls VLDP1 neighbor 67.176.255.7 vpls-id 502
      Flow Label Transmit: No, Flow Label Receive: No
    67.176.255.1(vpls-id 502) rmt   Up     Oct 26 17:44:04 2015           1
      Remote PE: 67.176.255.1, Negotiated control-word: No
      Incoming label: 262164, Outgoing label: 262162
      Negotiated PW status TLV: No
      Local interface: lsi.1048701, Status: Up, Encapsulation: ETHERNET
        Description: Intf - vpls VLDP1 neighbor 67.176.255.1 vpls-id 502
      Flow Label Transmit: No, Flow Label Receive: No



    rwibawa@vmx-13-14# run show vpls mac-table instance VLDP1 
    
    MAC flags       (S -static MAC, D -dynamic MAC, L -locally learned, C -Control MAC
        O -OVSDB MAC, SE -Statistics enabled, NM -Non configured MAC, R -Remote PE MAC)
    
    Routing instance : VLDP1
     Bridging domain : __VLDP1__, VLAN : NA
       MAC                 MAC      Logical          NH     RTR
       address             flags    interface        Index  ID
       00:50:58:13:12:04   D        lsi.1048701     
       00:50:58:13:18:04   D        lsi.1048700     
    
```

### PE Spoke

```
 rwibawa@vmx-13-11# show routing-instances VLDP1  
 instance-type vpls;
 interface ge-0/0/0.512;
 protocols {
     vpls {
         interface ge-0/0/0.512;
         no-tunnel-services;
         vpls-id 502;
         neighbor 67.176.255.4;
         inactive: neighbor 67.176.255.7;
     }
 }
 
 
 rwibawa@vmx-13-11# run show vpls connections instance VLDP1   
 ...
 
 Instance: VLDP1
   VPLS-id: 502
     Neighbor                  Type  St     Time last up          # Up trans
     67.176.255.4(vpls-id 502) rmt   Up     Oct 26 17:43:36 2015           1
       Remote PE: 67.176.255.4, Negotiated control-word: No
       Incoming label: 262162, Outgoing label: 262164
       Negotiated PW status TLV: No
       Local interface: lsi.1048997, Status: Up, Encapsulation: ETHERNET
         Description: Intf - vpls VLDP1 neighbor 67.176.255.4 vpls-id 502
       Flow Label Transmit: No, Flow Label Receive: No
 
 
 
 rwibawa@vmx-13-11# run show vpls mac-table instance VLDP1 
 
 MAC flags       (S -static MAC, D -dynamic MAC, L -locally learned, C -Control MAC
     O -OVSDB MAC, SE -Statistics enabled, NM -Non configured MAC, R -Remote PE MAC)
 
 Routing instance : VLDP1
  Bridging domain : __VLDP1__, VLAN : NA
    MAC                 MAC      Logical          NH     RTR
    address             flags    interface        Index  ID
    00:50:58:13:12:04   D        ge-0/0/0.512    
    00:50:58:13:18:04   D        lsi.1048997     
```
    
### PE Spoke 2

```
 rwibawa@vmx-13-17# show routing-instances VLDP1  
 instance-type vpls;
 interface ge-0/0/0.572;
 protocols {
     vpls {
         interface ge-0/0/0.572;
         no-tunnel-services;
         vpls-id 502;
         inactive: neighbor 67.176.255.1;
         neighbor 67.176.255.4;
     }
 }
 
 
 rwibawa@vmx-13-17# run show vpls connections instance VLDP1                         
 ...
 
 Instance: VLDP1
   VPLS-id: 502
     Neighbor                  Type  St     Time last up          # Up trans
     67.176.255.4(vpls-id 502) rmt   Up     Oct 26 17:43:36 2015           1
       Remote PE: 67.176.255.4, Negotiated control-word: No
       Incoming label: 262151, Outgoing label: 262165
       Negotiated PW status TLV: No
       Local interface: lsi.1048863, Status: Up, Encapsulation: ETHERNET
         Description: Intf - vpls VLDP1 neighbor 67.176.255.4 vpls-id 502
       Flow Label Transmit: No, Flow Label Receive: No
 
 
 
 rwibawa@vmx-13-17# run show vpls mac-table instance VLDP1 
 
 MAC flags       (S -static MAC, D -dynamic MAC, L -locally learned, C -Control MAC
     O -OVSDB MAC, SE -Statistics enabled, NM -Non configured MAC, R -Remote PE MAC)
 
 Routing instance : VLDP1
  Bridging domain : __VLDP1__, VLAN : NA
    MAC                 MAC      Logical          NH     RTR
    address             flags    interface        Index  ID
    00:50:58:13:12:04   D        lsi.1048863     
    00:50:58:13:18:04   D        ge-0/0/0.572    
```   
