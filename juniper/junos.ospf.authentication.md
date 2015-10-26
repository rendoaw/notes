# OSPF Authentication

```
rwibawa@vmx-13-11# show protocols ospf   
...
area 0.0.0.0 {
    interface ge-0/0/5.0 {
        authentication {
            simple-password "$9$-pbYoDi.z39JG39ApREdbs2JG"; ## SECRET-DATA
        }
    }
    interface ge-0/0/3.0 {
        authentication {
            md5 1 key "$9$ofZDk5Qnp0I.P0IEcvMaZU" start-time "2000-1-1.00:01:00 +0000"; ## SECRET-DATA
        }
    }
    interface lo0.0;
}
```

* ge-0/0/5.0 is using simple auth
* ge-0/0/3.0 is using md5
