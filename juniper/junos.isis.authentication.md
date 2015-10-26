# ISIS authentication

## level based

* simple

    ```
    rwibawa@vmx-13-14# show protocols isis 
    level 1 disable;
    level 2 {
        authentication-key "$9$PfT36/tBRSHqfz36u0vWLXVYJZjkmT"; ## SECRET-DATA
        authentication-type simple;
        wide-metrics-only;
    }
    interface ge-0/0/0.916;
    interface ge-0/0/1.0;
    interface ge-0/0/5.0;
    interface lo0.0;
    
    [edit]
    rwibawa@vmx-13-14# run show isis authentication 
    Interface             Level IIH Auth  CSN Auth  PSN Auth
    ge-0/0/0.916          2     Simple    Simple    Simple  
    ge-0/0/1.0            2     Simple    Simple    Simple  
    ge-0/0/5.0            2     Simple    Simple    Simple  
    
    L2 LSP Authentication: Simple
    ```

* md5

    ```
    rwibawa@vmx-13-14# show protocols isis 
    level 1 disable;
    level 2 {
        authentication-key "$9$PfT36/tBRSHqfz36u0vWLXVYJZjkmT"; ## SECRET-DATA
        authentication-type md5;
        wide-metrics-only;
    }
    interface ge-0/0/0.916;
    interface ge-0/0/1.0;
    interface ge-0/0/5.0;
    interface lo0.0;

    ```
    
* md5 with key-chain

    ```
    rwibawa@vmx-13-12# show protocols isis 
    level 1 disable;
    level 2 {
        authentication-key-chain isiskey;
        wide-metrics-only;
    }
    interface ge-0/0/0.5;
    interface ge-0/0/1.0;
    interface ge-0/0/2.0;
    interface ge-0/0/3.0;
    interface ge-0/0/4.0;
    interface lo0.0;
    
    rwibawa@vmx-13-12# show security 
    authentication-key-chains {
        key-chain isiskey {
            key 1 {
                secret "$9$bHwYoJZj.fz7-wgoJHk9ApuRSvMXNVY"; ## SECRET-DATA
                start-time "2000-1-1.00:00:00 +0000";
                algorithm md5;
            }
        }
    }
    ```



## interface level - hello authentication

* simple

    ```
    rwibawa@vmx-13-12# show protocols isis 
    level 1 disable;
    level 2 {
        wide-metrics-only;
    }
    interface ge-0/0/0.5 {
        level 2 hello-authentication-key "$9$MFyL7VgoGqmTwYmTz3tpWLxNwY"; ## SECRET-DATA
    }
    ```

* md5

    ```
    rwibawa@vmx-13-12# show protocols isis 
    level 1 disable;
    level 2 {
        wide-metrics-only;
    }
    interface ge-0/0/2.0 {
        level 2 {
            hello-authentication-key "$9$S7YlvLdb2GDkxNDk.P3nylKW7-"; ## SECRET-DATA
            hello-authentication-type md5;
        }
    }
    ```


* md5 with key-chain (interoperable with md5 only)

    ```
    rwibawa@vmx-13-14# show protocols isis                                                               
    level 1 disable;
    level 2 wide-metrics-only;
    interface ge-0/0/0.916;
    interface ge-0/0/1.0 {
        level 2 hello-authentication-key-chain isiskey;
    }
    interface ge-0/0/5.0;
    interface lo0.0;
    
    
    rwibawa@vmx-13-14# show security              
    authentication-key-chains {
        key-chain isiskey {
            key 1 {
                secret "$9$8QQx-woJDmfzYgfz36u0LxNV24"; ## SECRET-DATA
                start-time "2000-1-1.00:00:00 +0000";
                algorithm md5;
            }
        }
    }
    ```
