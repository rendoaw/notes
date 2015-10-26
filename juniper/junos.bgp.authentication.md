# BGP authentication

## md5

```
rwibawa@vmx-13-11# show protocols bgp group as766  
...
family inet {
    unicast;
}
authentication-key "$9$h.3SyK8X-gaZbwTz"; ## SECRET-DATA
peer-as 766;
neighbor 67.176.0.162;
```


## md5 with keychain

```
rwibawa@vmx-13-11# show protocols bgp group as766    
...
family inet {
    unicast;
}
authentication-key-chain bgpkey;
peer-as 766;
neighbor 67.176.0.162;


rwibawa@vmx-13-11# show security authentication-key-chains key-chain bgpkey 
key 1 {
    secret "$9$fTQnCtOSlKIRwY"; ## SECRET-DATA
    start-time "2000-1-1.00:01:00 +0000";
    algorithm md5;
}
```
