# Various type of JunOS L2VPN 

## CCC

* JunOS legacy L2VPN type
* requires 1 dedicated transmiting LSP and 1 dedicated receiving LSP
* Configuration example

    ```
    rwibawa@vmx-13-11# show protocols connections 
    remote-interface-switch PE14 {
        interface ge-0/0/0.970;
        transmit-lsp ccc-r1-r4;
        receive-lsp ccc-r4-r1;
    }
    
    [edit]
    rwibawa@vmx-13-11# show interfaces ge-0/0/0.970 
    apply-groups-except interface-group;
    encapsulation vlan-ccc;
    vlan-id 970;
    input-vlan-map {
        swap;
        vlan-id 969;
    }
    output-vlan-map swap;
    family ccc;
    ```

* redundancy is achieved by configuring multiple path for transmit LSP


## BGP-based L2VPN (L2VPN Kompella)

* Using BGP for signaling and auto-discovery
* redundancy is achived by setting site-preference on local site. Same as BGP-based VPLS.
* required BGP family l2vpn signaling
* configuration

    ```
    rwibawa@vmx-13-11# show routing-instances L2VPN1 
    instance-type l2vpn;
    interface ge-0/0/0.967;
    route-distinguisher 67.176.255.1:782;
    vrf-target target:7041:782;
    protocols {
        l2vpn {
            encapsulation-type ethernet-vlan;
            interface ge-0/0/0.967;
            site 1 {
                site-identifier 1;
                interface ge-0/0/0.967;
            }
        }
    }
    
    [edit]
    rwibawa@vmx-13-11# show interfaces ge-0/0/0.967 
    apply-groups-except interface-group;
    encapsulation vlan-ccc;
    vlan-id 967;
    input-vlan-map {
        swap;
        vlan-id 966;
    }
    output-vlan-map swap;
    family ccc;
    ```

## LDP-based L2VPN (L2VPN Martini)

* no BGP is required
* targeted LDP is used between local PE and remote PE
* redundancy is achived by configuring backup neighbor explicitly
* configuration

    ```
    rwibawa@vmx-13-11# show protocols l2circuit 
    neighbor 67.176.255.7 {
        interface ge-0/0/0.964 {
            virtual-circuit-id 781;
            backup-neighbor 67.176.255.4 {
                virtual-circuit-id 781;
            }
        }
    }
    
    [edit]
    rwibawa@vmx-13-11# show interfaces ge-0/0/0.964 
    apply-groups-except interface-group;
    encapsulation vlan-ccc;
    vlan-id 964;
    input-vlan-map {
        swap;
        vlan-id 963;
    }
    output-vlan-map swap;
    family ccc;
    ```
