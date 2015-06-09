Send standard juniper stanza inside netconf
```
<rpc> 
    <edit-config> 
        <target> 
            <candidate/> 
        </target> 
        <config-text>
            <configuration-text>

            system { 
                host-name juniper1; 
            }

            </configuration-text>
        </config-text> 
    </edit-config> 
</rpc>]]>]]>

<rpc> 
<commit-configuration> 
    <synchronize/> 
    </commit-configuration> 
</rpc>]]>]]>
```


get standard juniper show output inside netconf
```
<rpc><get-interface-information format="text"></get-interface-information></rpc>

<output>
Physical interface: ge-0/0/0, Enabled, Physical link is Up
]]>]]>
  Interface index: 138, SNMP ifIndex: 513
  Link-level type: Ethernet, MTU: 1518, MRU: 1526, LAN-PHY mode,
  Speed: 1000mbps, BPDU Error: None, MAC-REWRITE Error: None,
  Loopback: Disabled, Source filtering: Disabled, Flow control: Enabled
  Pad to minimum frame size: Disabled
  Device flags   : Present Running

....

</output>
```

send standard text command and get output in text format
```
<rpc><command format="text">show mpls lsp terse</command></rpc>
<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:junos="http://xml.juniper.net/junos/14.2/junos">
<output>
Ingress LSP: 11 sessions
Total 11 displayed, Up 11, Down 0

Egress LSP: 16 sessions
Total 16 displayed, Up 16, Down 0

Transit LSP: 0 sessions
Total 0 displayed, Up 0, Down 0
</output>
</rpc-reply>
]]>]]>
```

send xml , get xml output
```
<rpc><get-interface-information></get-interface-information></rpc>
<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:junos="http://xml.juniper.net/junos/14.2/junos">
<interface-information xmlns="http://xml.juniper.net/junos/14.2X1/junos-interface" junos:style="normal">
<physical-interface>
<name>
ge-0/0/0
</name>
<admin-status junos:format="Enabled">
up
</admin-status>
<oper-status>
up
</oper-status>
<local-index>
138
</local-index>
<snmp-index>
518
</snmp-index>
<link-level-type>
Ethernet
</link-level-type>
...
...
```

