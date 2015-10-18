
# JunOS OSPF Import Policy

## Official

source: http://www.juniper.net/documentation/en_US/junos15.1/topics/example/ospf-import-routing-policy-configuring.html

OSPF import policy allows you to prevent external routes from being added to the routing tables of OSPF neighbors. The import policy does not impact the OSPF database. This means that the import policy has no impact on the link-state advertisements. The filtering is done only on external routes in OSPF. The intra-area and interarea routes are not considered for filtering. The default action is to accept the route when the route does not match the policy.


## Personal note
* possible case
  * backbone is using ISIS
  * PE-CE (non vpn) is using OSPF
  * CE is dual homed
  * make sure PE1/PE2 is not using CE to reach any destination in the backbone, especially for any external route
  * using import policy will block any unwanted external route in the OSPF database to be imported into routing table
