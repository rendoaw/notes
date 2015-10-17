source: https://forums.freebsd.org/threads/add-static-route-with-netmask-to-dhcp.40584/

```
# Option to add static routes with netmask
# RFC3442 routes: overrides routers option
option rfc3442-classless-static-routes code 121 = array of unsigned integer 8;
# MS routes: adds extras to supplement routers option
option ms-classless-static-routes code 249 = array of unsigned integer 8;

# Local subnet
subnet 172.16.0.0 netmask 255.255.255.0 {
        range 172.16.0.151 172.16.0.199;
        option routers 172.16.0.1;
        option broadcast-address 172.16.0.255;

        # Static route for OpenVPN
        # Classless static routes overrides default route (option routers)
        # Default route needs to be added to the classless static routes
        option rfc3442-classless-static-routes 24, 10,8,0, 172,16,0,10,  0, 172,16,0,1;
        option ms-classless-static-routes      24, 10,8,0, 172,16,0,10,  0, 172,16,0,1;
}
```
