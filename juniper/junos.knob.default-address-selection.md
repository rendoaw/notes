
### base config

* R6

    ```
    rwibawa@vmx-13-16> show configuration interfaces lo0
    unit 0 {
        family inet {
            address 67.176.255.6/32;
        }
        family iso {
            address 49.0002.0671.7625.5006.00;
        }
        family inet6 {
            address 2400:67:176:255::6/128;
        }
    }

    rwibawa@vmx-13-16> show configuration interfaces ge-0/0/0.42
    description R8;
    vlan-id 42;
    family inet {
        address 67.176.0.37/30;
    }
    family inet6 {
        address 2400:67:176:0:68::1/126;
    }
    family mpls;
    ```

* R8

    ```
    rwibawa@vmx-13-18# show interfaces lo0
    unit 0 {
        family inet {
            address 67.176.255.8/32;
        }
        family iso {
            address 49.0002.0671.7625.5008.00;
        }
        family inet6 {
            address 2400:67:176:255::8/128;
        }
    }

    rwibawa@vmx-13-18# show interfaces ge-0/0/4
    unit 0 {
        description R6;
        family inet {
            address 67.176.0.38/30;
        }
        family inet6 {
            address 2400:67:176:0:68::2/126;
        }
        family mpls;
    }
    ```

### knob configuration

```
rwibawa@vmx-13-18# show system
...
default-address-selection;
...
```


### without "default-address-selection" knob

* ping 

    ```
    rwibawa@vmx-13-18# run ping 67.176.255.6

    rwibawa@vmx-13-18# run ping 2400:67:176:0:68::1
    ```

* monitor traffic interface on the neighbor side

    ```
    00:51:07.456383  In IP6 2400:67:176:0:68::2 > 2400:67:176:0:68::1: ICMP6, echo request, seq 3, length 16
    00:51:07.456414 Out IP6 2400:67:176:0:68::1 > 2400:67:176:0:68::2: ICMP6, echo reply, seq 3, length 16
    00:51:08.456840  In IP6 2400:67:176:0:68::2 > 2400:67:176:0:68::1: ICMP6, echo request, seq 4, length 16
    00:51:08.456873 Out IP6 2400:67:176:0:68::1 > 2400:67:176:0:68::2: ICMP6, echo reply, seq 4, length 16

    00:47:49.452825  In IP 67.176.0.38 > 67.176.255.6: ICMP echo request, id 63375, seq 27, length 64
    00:47:49.452843 Out IP 67.176.255.6 > 67.176.0.38: ICMP echo reply, id 63375, seq 27, length 64
    00:47:50.462942  In IP 67.176.0.38 > 67.176.255.6: ICMP echo request, id 63375, seq 28, length 64
    00:47:50.462963 Out IP 67.176.255.6 > 67.176.0.38: ICMP echo reply, id 63375, seq 28, length 64
    ```


### with "default-address-selection" knob

* ping 

    ```
    rwibawa@vmx-13-18# run ping 67.176.255.6

    rwibawa@vmx-13-18# run ping 2400:67:176:0:68::1
    ```

* monitor traffic interface on the neighbor side

    ```
    00:48:21.450930  In IP 67.176.255.8 > 67.176.255.6: ICMP echo request, id 35217, seq 0, length 64
    00:48:21.450959 Out IP 67.176.255.6 > 67.176.255.8: ICMP echo reply, id 35217, seq 0, length 64
    00:48:22.453550  In IP 67.176.255.8 > 67.176.255.6: ICMP echo request, id 35217, seq 1, length 64
    00:48:22.453567 Out IP 67.176.255.6 > 67.176.255.8: ICMP echo reply, id 35217, seq 1, length 64

    00:51:28.643581  In IP6 2400:67:176:255::8 > 2400:67:176:0:68::1: ICMP6, echo request, seq 0, length 16
    00:51:28.643622 Out IP6 2400:67:176:0:68::1 > 2400:67:176:255::8: ICMP6, echo reply, seq 0, length 16
    00:51:28.663514  In IP6 2400:67:176:255::8 > 2400:67:176:0:68::1: ICMP6, echo request, seq 1, length 16
    00:51:28.663545 Out IP6 2400:67:176:0:68::1 > 2400:67:176:255::8: ICMP6, echo reply, seq 1, length 16
    ```


