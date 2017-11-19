

```
# wget -O /usr/local/bin/calicoctl https://github.com/projectcalico/calicoctl/releases/download/v1.3.0/calicoctl
# chmod +x /usr/local/bin/calicoctl

#  mkdir /etc/calico

# cat /etc/calico/calicoctl.cfg
apiVersion: v1
kind: calicoApiConfig
metadata:
spec:
    etcdEndpoints: http://localhost:2379
    vim /etc/calico/calicoctl.cfg

#  calicoctl node run --node-image=quay.io/calico/node:v1.3.0
#  calicoctl get  ipPool --output wide


# cat ippool_v6.yaml
apiVersion: v1
kind: ipPool
metadata:
    cidr: 2001:db8:101::/64
spec:
    ipip:
      enabled: false
      mode: always


# cat ippool_v4.yaml
apiVersion: v1
kind: ipPool
metadata:
    cidr: 10.191.101.0/24
spec:
    ipip:
      enabled: false
      mode: always


# cat ippool_nat.yaml
apiVersion: v1
kind: ipPool
metadata:
    cidr: 10.254.101.0/24
spec:
    nat-outgoing: true
    ipip:
      enabled: false
      mode: always


# calicoctl create -f ippool_v6.yaml
# calicoctl create -f ippool_v4.yaml
# calicoctl create -f ippool_nat.yaml

# calicoctl get  ipPool --output wide

# more policy.yaml
apiVersion: v1
kind: profile
metadata:
    name: net1
    labels:
      role: net1
spec:
    ingress:
    - action: allow
      protocol: tcp
    - action: allow
      protocol: udp
    - action: allow
      protocol: icmp
    egress:
    - action: allow
      protocol: tcp
    - action: allow
      protocol: udp
    - action: allow
      protocol: icmp


# docker network create --driver calico --ipam-driver calico-ipam net1 --subnet 10.191.101.0/24
# calicoctl apply -f policy.yaml

# etcdctl get /calico/v1/policy/profile/net1/rules

# docker run -d --name test --privileged --restart=always rendoaw/ubuntu_netkit

```
