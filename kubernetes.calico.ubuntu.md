
## Setup Kubernetes Cluster using Kubeadm

### Install docker, kubeadm and other kubernetes tools. 

* Reference
Follow https://kubernetes.io/docs/setup/independent/install-kubeadm/

* Summary step

```
apt-get update && apt-get install -y curl apt-transport-https
apt-get install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker

curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
cat <<EOF >/etc/apt/sources.list.d/kubernetes.list
deb http://apt.kubernetes.io/ kubernetes-xenial main
EOF
apt-get update
apt-get install -y kubelet kubeadm kubectl
```

### Initialize Kubernetes

* Decide and reserver the subnet range that will be used for container IP address
In the following example, i am using 10.201.0.0/25 as IP Pool for the container

* Command example

```
ubuntu@ubuntu-4:~$ sudo su  
ubuntu@ubuntu-4:~# kubeadm init --pod-network-cidr=10.201.0.0/25 --token-ttl 0

[kubeadm] WARNING: kubeadm is in beta, please do not use it for production clusters.
[init] Using Kubernetes version: v1.8.1
[init] Using Authorization modes: [Node RBAC]
[preflight] Running pre-flight checks
[preflight] Starting the kubelet service
[certificates] Generated ca certificate and key.
[certificates] Generated apiserver certificate and key.
[certificates] apiserver serving cert is signed for DNS names [ubuntu-4 kubernetes kubernetes.default kubernetes.default.svc kubernetes.default.svc.clus
ter.local] and IPs [10.96.0.1 100.64.1.23]
[certificates] Generated apiserver-kubelet-client certificate and key.
[certificates] Generated sa key and public key.
[certificates] Generated front-proxy-ca certificate and key.
[certificates] Generated front-proxy-client certificate and key.
[certificates] Valid certificates and keys now exist in "/etc/kubernetes/pki"
[kubeconfig] Wrote KubeConfig file to disk: "admin.conf"
[kubeconfig] Wrote KubeConfig file to disk: "kubelet.conf"
[kubeconfig] Wrote KubeConfig file to disk: "controller-manager.conf"
[kubeconfig] Wrote KubeConfig file to disk: "scheduler.conf"
[controlplane] Wrote Static Pod manifest for component kube-apiserver to "/etc/kubernetes/manifests/kube-apiserver.yaml"
[controlplane] Wrote Static Pod manifest for component kube-controller-manager to "/etc/kubernetes/manifests/kube-controller-manager.yaml"
[controlplane] Wrote Static Pod manifest for component kube-scheduler to "/etc/kubernetes/manifests/kube-scheduler.yaml"
[etcd] Wrote Static Pod manifest for a local etcd instance to "/etc/kubernetes/manifests/etcd.yaml"
[init] Waiting for the kubelet to boot up the control plane as Static Pods from directory "/etc/kubernetes/manifests"
[init] This often takes around a minute; or longer if the control plane images have to be pulled.
[apiclient] All control plane components are healthy after 32.504184 seconds
[uploadconfig] Storing the configuration used in ConfigMap "kubeadm-config" in the "kube-system" Namespace
[markmaster] Will mark node ubuntu-4 as master by adding a label and a taint
[markmaster] Master ubuntu-4 tainted and labelled with key/value: node-role.kubernetes.io/master=""
[bootstraptoken] Using token: 33794e.456bdf6538ec8783
[bootstraptoken] Configured RBAC rules to allow Node Bootstrap tokens to post CSRs in order for nodes to get long term certificate credentials
[bootstraptoken] Configured RBAC rules to allow the csrapprover controller automatically approve CSRs from a Node Bootstrap Token
[bootstraptoken] Configured RBAC rules to allow certificate rotation for all node client certificates in the cluster
[bootstraptoken] Creating the "cluster-info" ConfigMap in the "kube-public" namespace
[addons] Applied essential addon: kube-dns
[addons] Applied essential addon: kube-proxy

Your Kubernetes master has initialized successfully!

To start using your cluster, you need to run (as a regular user):

  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config

You should now deploy a pod network to the cluster.
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
  http://kubernetes.io/docs/admin/addons/

You can now join any number of machines by running the following on each node
as root:

  kubeadm join --token 33794e.456bdf6538ec8783 100.64.1.23:6443 --discovery-token-ca-cert-hash sha256:518238e71fd5484de58d15d91cb7196498f23154a924bc249bc7453487246f59
```

* Copy the success message above to any text editor, especially the kubeadm join parameter. We will need this to join worker node later.

* Exit from sudo. All the remaining command will be done as normal user.

```
root@ubuntu-4:/home/ubuntu# exit
exit
```

* Copy the config and the key to ~/.kube  
  
ubuntu@ubuntu-4:~$ rm -rf .kube
ubuntu@ubuntu-4:~$ mkdir -p $HOME/.kube
ubuntu@ubuntu-4:~$ sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
ubuntu@ubuntu-4:~$ sudo chown $(id -u):$(id -g) $HOME/.kube/config

* Run simple sanity check, to see if all Kubernetes component is fine

```
ubuntu@ubuntu-4:~$ kubectl get pods --all-namespaces -o wide
NAMESPACE     NAME                               READY     STATUS    RESTARTS   AGE       IP            NODE
kube-system   etcd-ubuntu-4                      1/1       Running   0          19m       100.64.1.23   ubuntu-4
kube-system   kube-apiserver-ubuntu-4            1/1       Running   0          19m       100.64.1.23   ubuntu-4
kube-system   kube-controller-manager-ubuntu-4   1/1       Running   0          19m       100.64.1.23   ubuntu-4
kube-system   kube-dns-545bc4bfd4-wnjxc          0/3       Pending   0          20m       <none>        <none>
kube-system   kube-proxy-jm7xj                   1/1       Running   0          20m       100.64.1.23   ubuntu-4
kube-system   kube-scheduler-ubuntu-4            1/1       Running   0          19m       100.64.1.23   ubuntu-4
```

* I believe it is ok for kube-dns to be pending. It will be up once we configure the networking part.


### Install Calico 

* Download Calico YAML file

```  
wget https://docs.projectcalico.org/v2.6/getting-started/kubernetes/installation/hosted/kubeadm/1.6/calico.yaml
```

* Adjust the IP Pool range inside Calico manifest
	By default Calico is using 192.168.0.0/16 as IP Pool for the container. To change that:
	* edit calico.yaml
	* find  attribute CALICO_IPV4POOL_CIDR
	* change the value to CIDR that you want e.g: 10.16.0.0/16


* Install Calico module

```
ubuntu@ubuntu-4:~$ kubectl apply -f calico.yaml  
configmap "calico-config" created
daemonset "calico-etcd" created
service "calico-etcd" created
daemonset "calico-node" created
deployment "calico-kube-controllers" created
deployment "calico-policy-controller" created
clusterrolebinding "calico-cni-plugin" created
clusterrole "calico-cni-plugin" created
serviceaccount "calico-cni-plugin" created
clusterrolebinding "calico-kube-controllers" created
clusterrole "calico-kube-controllers" created
serviceaccount "calico-kube-controllers" created
```


* Check if all Kubernetes and Calico components are up and running (It may take few minutes)

```
ubuntu@ubuntu-4:~$ kubectl get pods --all-namespaces -o wide
NAMESPACE     NAME                                       READY     STATUS    RESTARTS   AGE       IP            NODE
kube-system   calico-etcd-n9tn2                          1/1       Running   0          25s       100.64.1.23   ubuntu-4
kube-system   calico-kube-controllers-6ff88bf6d4-9n2zn   1/1       Running   0          23s       100.64.1.23   ubuntu-4
kube-system   calico-node-hq75v                          2/2       Running   0          24s       100.64.1.23   ubuntu-4
kube-system   etcd-ubuntu-4                              1/1       Running   0          20m       100.64.1.23   ubuntu-4
kube-system   kube-apiserver-ubuntu-4                    1/1       Running   0          20m       100.64.1.23   ubuntu-4
kube-system   kube-controller-manager-ubuntu-4           1/1       Running   0          20m       100.64.1.23   ubuntu-4
kube-system   kube-dns-545bc4bfd4-wnjxc                  0/3       Pending   0          21m       <none>        <none>
kube-system   kube-proxy-jm7xj                           1/1       Running   0          21m       100.64.1.23   ubuntu-4
kube-system   kube-scheduler-ubuntu-4                    1/1       Running   0          20m       100.64.1.23   ubuntu-4
```

### (Optional) Enable the master node as worker 

By default, Kubernetes master node will not become a worker, means no user container will be run on master node. For this testing i want the master node to become worker too.

```
ubuntu@ubuntu-4:~$ kubectl taint nodes --all node-role.kubernetes.io/master-
node "ubuntu-4" untainted
```

### Check the node status

```
ubuntu@ubuntu-4:~$ kubectl get nodes  -o wide
NAME       STATUS    ROLES     AGE       VERSION   EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION     CONTAINER-RUNTIME
ubuntu-4   Ready     master    26m       v1.8.1    <none>        Ubuntu 16.04.3 LTS   4.4.0-97-generic   docker://1.12.6
```

  
  
### Install Calicoctl

Calicoctl is a utility to manage Calico plugin.

* To install, run:

```
ubuntu@ubuntu-4:~$ kubectl apply -f https://docs.projectcalico.org/v2.6/getting-started/kubernetes/installation/hosted/calicoctl.yaml
pod "calicoctl" created
```

* Check the calicoctl installation status

```
ubuntu@ubuntu-4:~$ kubectl get pods --all-namespaces -o wide
NAMESPACE     NAME                                       READY     STATUS    RESTARTS   AGE       IP             NODE
... deleted...
kube-system   calicoctl                                  1/1       Running   0          6s        100.64.1.23    ubuntu-4

... deleted...
ubuntu@ubuntu-4:~$
```

* Check if Calicoctl works  
  
```  
ubuntu@ubuntu-4:~$ kubectl exec -ti -n kube-system calicoctl -- /calicoctl get profiles -o wide
NAME                 TAGS
k8s_ns.default
k8s_ns.kube-public
k8s_ns.kube-system
```

## Run the Containers

### Bring up some basic containers for sanity check

* Bring up a single ubuntu-based sshd container

```
ubuntu@ubuntu-4:~$ kubectl run sshd-1 --image=rastasheep/ubuntu-sshd:16.04
deployment "sshd-1" created
```

* Check the container status

```
ubuntu@ubuntu-4:~$ kubectl get pods -o wide
NAME                      READY     STATUS    RESTARTS   AGE       IP             NODE
sshd-1-84c4bf4558-284dj   1/1       Running   0          23s       10.201.0.197   ubuntu-4
```








## Misc
  
* The following is the output when IP Pool is too small 

```
ubuntu@ubuntu-4:~$ kubectl get pods --all-namespaces -o wide
NAMESPACE     NAME                               READY     STATUS             RESTARTS   AGE       IP            NODE
kube-system   etcd-ubuntu-4                      1/1       Running            0          17s       100.64.1.23   ubuntu-4
kube-system   kube-apiserver-ubuntu-4            1/1       Running            0          9s        100.64.1.23   ubuntu-4
kube-system   kube-controller-manager-ubuntu-4   0/1       CrashLoopBackOff   3          1m        100.64.1.23   ubuntu-4
kube-system   kube-scheduler-ubuntu-4            1/1       Running            0          11s       100.64.1.23   ubuntu-4
```

* Try to login to the container

```
ubuntu@ubuntu-4:~$ ssh root@10.201.0.197
The authenticity of host '10.201.0.197 (10.201.0.197)' can't be established.
ECDSA key fingerprint is SHA256:oeXGFyX/mdzuCxeulD1bOzDe1lCbIktPxb7vKNPiDOs.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '10.201.0.197' (ECDSA) to the list of known hosts.


root@sshd-1-84c4bf4558-284dj:/# apt-get update 
root@sshd-1-84c4bf4558-284dj:/# apt-get install iproute 2
root@sshd-1-84c4bf4558-284dj:~# apt-get install inetutils-ping traceroute

root@sshd-1-84c4bf4558-284dj:/sbin# ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: tunl0@NONE: <NOARP> mtu 1480 qdisc noop state DOWN group default qlen 1
    link/ipip 0.0.0.0 brd 0.0.0.0
4: eth0@if7: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
    link/ether ea:ff:92:a4:32:63 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 10.201.0.197/32 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::e8ff:92ff:fea4:3263/64 scope link 
       valid_lft forever preferred_lft forever
	   
root@sshd-1-84c4bf4558-284dj:~# ip r
default via 169.254.1.1 dev eth0
169.254.1.1 dev eth0  scope link
```


## Join the second worker node to the cluster 

* kubeadm join

```
root@ubuntu-3:/home/ubuntu# kubeadm join --token 33794e.456bdf6538ec8783 100.64.1.23:6443 --discovery-token-ca-cert-hash sha256:518238e71fd5484de58d15d91cb7196498f23154a924bc249bc7453487246f59
[kubeadm] WARNING: kubeadm is in beta, please do not use it for production clusters.
[preflight] Running pre-flight checks
[discovery] Trying to connect to API Server "100.64.1.23:6443"
[discovery] Created cluster-info discovery client, requesting info from "https://100.64.1.23:6443"
[discovery] Requesting info from "https://100.64.1.23:6443" again to validate TLS against the pinned public key
[discovery] Cluster info signature and contents are valid and TLS certificate validates against pinned roots, will use API Server "100.64.1.23:6443"
[discovery] Successfully established connection with API Server "100.64.1.23:6443"
[bootstrap] Detected server version: v1.8.1
[bootstrap] The server supports the Certificates API (certificates.k8s.io/v1beta1)

Node join complete:
* Certificate signing request sent to master and response
  received.
* Kubelet informed of new secure connection details.

Run 'kubectl get nodes' on the master to see this machine join.
```

* Verify the node list

```
ubuntu@ubuntu-4:~$ kubectl get nodes -o wide
NAME       STATUS    ROLES     AGE       VERSION   EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION     CONTAINER-RUNTIME
ubuntu-3   Ready     <none>    38s       v1.8.1    <none>        Ubuntu 16.04.3 LTS   4.4.0-97-generic   docker://1.12.6
ubuntu-4   Ready     master    50m       v1.8.1    <none>        Ubuntu 16.04.3 LTS   4.4.0-97-generic   docker://1.12.6
```


* Verify the system containers again

```
ubuntu@ubuntu-4:~$ kubectl get pods --all-namespaces -o wide
NAMESPACE     NAME                                       READY     STATUS    RESTARTS   AGE       IP             NODE
default       sshd-1-84c4bf4558-284dj                    1/1       Running   0          22m       10.201.0.197   ubuntu-4
kube-system   calico-etcd-n9tn2                          1/1       Running   0          29m       100.64.1.23    ubuntu-4
kube-system   calico-kube-controllers-6ff88bf6d4-9n2zn   1/1       Running   0          29m       100.64.1.23    ubuntu-4
kube-system   calico-node-hq75v                          2/2       Running   0          29m       100.64.1.23    ubuntu-4
kube-system   calico-node-xgf66                          1/2       Running   1          51s       100.64.1.24    ubuntu-3
kube-system   calicoctl                                  1/1       Running   0          24m       100.64.1.23    ubuntu-4
kube-system   etcd-ubuntu-4                              1/1       Running   0          49m       100.64.1.23    ubuntu-4
kube-system   kube-apiserver-ubuntu-4                    1/1       Running   0          49m       100.64.1.23    ubuntu-4
kube-system   kube-controller-manager-ubuntu-4           1/1       Running   0          49m       100.64.1.23    ubuntu-4
kube-system   kube-dns-545bc4bfd4-wnjxc                  3/3       Running   0          50m       10.201.0.196   ubuntu-4
kube-system   kube-proxy-jm7xj                           1/1       Running   0          50m       100.64.1.23    ubuntu-4
kube-system   kube-proxy-t82nz                           1/1       Running   0          51s       100.64.1.24    ubuntu-3
kube-system   kube-scheduler-ubuntu-4                    1/1       Running   0          49m       100.64.1.23    ubuntu-4
```


## Bring up second container

```
ubuntu@ubuntu-4:~$ kubectl run sshd-2 --image=rastasheep/ubuntu-sshd:16.04
deployment "sshd-2" created
```

* Verify container status

```
ubuntu@ubuntu-4:~$ kubectl get pods --all-namespaces -o wide
NAMESPACE     NAME                                       READY     STATUS    RESTARTS   AGE       IP             NODE
default       sshd-1-84c4bf4558-284dj                    1/1       Running   0          26m       10.201.0.197   ubuntu-4
default       sshd-2-78f7789cc8-95srr                    1/1       Running   0          10s       10.201.0.130   ubuntu-3
kube-system   calico-etcd-n9tn2                          1/1       Running   0          33m       100.64.1.23    ubuntu-4
kube-system   calico-kube-controllers-6ff88bf6d4-9n2zn   1/1       Running   0          33m       100.64.1.23    ubuntu-4
kube-system   calico-node-hq75v                          2/2       Running   0          33m       100.64.1.23    ubuntu-4
kube-system   calico-node-xgf66                          2/2       Running   1          4m        100.64.1.24    ubuntu-3
kube-system   calicoctl                                  1/1       Running   0          28m       100.64.1.23    ubuntu-4
kube-system   etcd-ubuntu-4                              1/1       Running   0          53m       100.64.1.23    ubuntu-4
kube-system   kube-apiserver-ubuntu-4                    1/1       Running   0          53m       100.64.1.23    ubuntu-4
kube-system   kube-controller-manager-ubuntu-4           1/1       Running   0          53m       100.64.1.23    ubuntu-4
kube-system   kube-dns-545bc4bfd4-wnjxc                  3/3       Running   0          54m       10.201.0.196   ubuntu-4
kube-system   kube-proxy-jm7xj                           1/1       Running   0          54m       100.64.1.23    ubuntu-4
kube-system   kube-proxy-t82nz                           1/1       Running   0          4m        100.64.1.24    ubuntu-3
kube-system   kube-scheduler-ubuntu-4                    1/1       Running   0          53m       100.64.1.23    ubuntu-4
```


* Login to second container 

```
root@ubuntu-3:/home/ubuntu# ssh root@10.201.0.130
The authenticity of host '10.201.0.130 (10.201.0.130)' can't be established.
ECDSA key fingerprint is SHA256:oeXGFyX/mdzuCxeulD1bOzDe1lCbIktPxb7vKNPiDOs.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '10.201.0.130' (ECDSA) to the list of known hosts.
root@10.201.0.130's password:
root@sshd-2-78f7789cc8-95srr:~# apt-get update && apt-get install iproute2 traceroute inetutils-ping
```

* test connectivity to container 1

```
root@sshd-2-78f7789cc8-95srr:~# ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: tunl0@NONE: <NOARP> mtu 1480 qdisc noop state DOWN group default qlen 1
    link/ipip 0.0.0.0 brd 0.0.0.0
4: eth0@if6: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
    link/ether de:b9:ee:74:0c:c7 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 10.201.0.130/32 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::dcb9:eeff:fe74:cc7/64 scope link
       valid_lft forever preferred_lft forever

	   
root@sshd-2-78f7789cc8-95srr:~# ip r
default via 169.254.1.1 dev eth0
169.254.1.1 dev eth0  scope link


root@sshd-2-78f7789cc8-95srr:~# ping 10.201.0.197
PING 10.201.0.197 (10.201.0.197): 56 data bytes
64 bytes from 10.201.0.197: icmp_seq=0 ttl=62 time=0.986 ms
64 bytes from 10.201.0.197: icmp_seq=1 ttl=62 time=0.627 ms
^C--- 10.201.0.197 ping statistics ---
2 packets transmitted, 2 packets received, 0% packet loss
round-trip min/avg/max/stddev = 0.627/0.806/0.986/0.180 ms


root@sshd-2-78f7789cc8-95srr:~# traceroute -n 10.201.0.197
traceroute to 10.201.0.197 (10.201.0.197), 30 hops max, 60 byte packets
 1  100.64.1.24  0.192 ms  0.068 ms  0.082 ms
 2  10.201.0.192  0.525 ms  0.355 ms  0.281 ms
 3  10.201.0.197  0.421 ms  0.564 ms  0.356 ms
root@sshd-2-78f7789cc8-95srr:~#
```

	   
### Do some basic Calico related checking
	   
```	   
ubuntu@ubuntu-4:~$ kubectl exec -ti -n kube-system calicoctl -- /calicoctl get -o yaml node 
- apiVersion: v1
  kind: node
  metadata:
    name: ubuntu-3
  spec:
    bgp:
      ipv4Address: 100.64.1.24/24
- apiVersion: v1
  kind: node
  metadata:
    name: ubuntu-4
  spec:
    bgp:
      ipv4Address: 100.64.1.23/24	   
	   
	   
ubuntu@ubuntu-4:~$ kubectl exec -ti -n kube-system calicoctl -- /calicoctl get -o yaml ipPool
- apiVersion: v1
  kind: ipPool
  metadata:
    cidr: 10.201.0.0/24
  spec:
    ipip:
      enabled: true
      mode: always
    nat-outgoing: true
```
	
	   
	   
### ALternatively, we can attach to calicoctl container and run all the command from there

```
ubuntu@ubuntu-4:~$ sudo docker exec -it ca4c48f14c8e  /bin/busybox sh
~ # ls -al
total 16
drwx------    2 root     root          4096 Oct 19 19:47 .
drwxr-xr-x   35 root     root          4096 Oct 19 19:47 ..
-rw-------    1 root     root             7 Oct 19 19:47 .ash_history
-rw-r--r--    1 root     root           215 Sep 29 04:04 .wget-hsts
~ #
```

### Prepare a new IP Pool

/ # cat >> ippool.yaml << EOF
> - apiVersion: v1
>   kind: ipPool
>   metadata:
>     cidr: 10.91.1.0/24
>   spec:
>     ipip:
>       enabled: true
>       mode: always
>     nat-outgoing: false
> EOF


* Enable the new IP Pool
/ # /calicoctl create -f ippool.yaml
Successfully created 1 'ipPool' resource(s)


* Verify all IP Pools

```
/ # /calicoctl get -o yaml ippool
- apiVersion: v1
  kind: ipPool
  metadata:
    cidr: 10.201.0.0/24
  spec:
    ipip:
      enabled: true
      mode: always
    nat-outgoing: true
- apiVersion: v1
  kind: ipPool
  metadata:
    cidr: 10.91.1.0/24
  spec:
    ipip:
      enabled: true
      mode: always
/ #
```


* Create a new pod definition

```
ubuntu@ubuntu-4:~$ cat pod1.yaml
---
apiVersion: v1
kind: Pod
metadata:
  annotations:
    "cni.projectcalico.org/ipv4pools": "[\"10.91.1.0/24\"]"
  name: ssh-server
  labels:
    app: sshd
spec:
  containers:
    - name: ssh-server-container
      image: "rastasheep/ubuntu-sshd:16.04"
```

* Bring up the new pod

```
ubuntu@ubuntu-4:~$ kubectl create -f pod1.yaml
pod "ssh-server" created
```


## Configure external BGP Peer

```
ubuntu@ubuntu-4:~$ kubectl exec -ti -n kube-system calicoctl -- /bin/busybox sh
~ # cat >> bgp.yaml << EOF
> apiVersion: v1
> kind: bgpPeer
> metadata:
>   peerIP: 100.64.1.1
>   scope: global
> spec:
>   asNumber: 64512
> EOF

~ # calicoctl create -f bgp.yaml
Successfully created 1 'bgpPeer' resource(s)
~ # calicoctl get -o yaml bgppeer
- apiVersion: v1
  kind: bgpPeer
  metadata:
    peerIP: 100.64.1.1
    scope: global
  spec:
    asNumber: 64512
~ #
```


* Create a seconf subnet with very small subnet size 

```
~ # cat ippool2.yaml
- apiVersion: v1
  kind: ipPool
  metadata:
    cidr: 10.91.2.0/27
  spec:
    ipip:
      enabled: true
      mode: always
    nat-outgoing: false
~ # calicoctl create -f ippool2.yaml
Failed to execute command: error with field CIDR = '10.91.2.0/27' (IP pool size is too small (min /26) for use with Calico IPAM)
```


* Increase the subnet size 

```
~ # cat ippool2.yaml 
- apiVersion: v1
  kind: ipPool
  metadata:
    cidr: 10.91.2.0/26
  spec:
    ipip:
      enabled: true
      mode: always
    nat-outgoing: false
~ # calicoctl create -f ippool2.yaml
Successfully created 1 'ipPool' resource(s)
```


* Check all available IP Pool

```
~ # calicoctl get -o wide ippool
CIDR            NAT     IPIP
10.201.0.0/24   true    true
10.91.1.0/24    false   true
10.91.2.0/26    false   true
```


* Put some label on each Node to map Pod to a specific node

```
ubuntu@ubuntu-4:~$ kubectl label nodes ubuntu-4 node_id=n4
node "ubuntu-4" labeled
ubuntu@ubuntu-4:~$ kubectl label nodes ubuntu-3 node_id=n3
node "ubuntu-3" labeled
```


* Create a new Pod that must run on "ubuntu-4" node

```
ubuntu@ubuntu-4:~$ kubectl create -f pod_on_node4.yaml
ubuntu@ubuntu-4:~$ kubectl get pods -o wide
NAME                      READY     STATUS    RESTARTS   AGE       IP             NODE
ssh-server                1/1       Running   0          20h       10.91.1.128    ubuntu-3
ssh-server4               1/1       Running   0          12s       10.91.2.0      ubuntu-4
sshd-1-84c4bf4558-284dj   1/1       Running   0          22h       10.201.0.197   ubuntu-4
sshd-2-78f7789cc8-95srr   1/1       Running   0          21h       10.201.0.130   ubuntu-3
sshd-3-6bb86d6bf8-bq4q8   1/1       Running   0          20h       10.201.0.131   ubuntu-3
```


  
```
ubuntu@ubuntu-4:~$ kubectl create -f pod_on_node3.yaml

ubuntu@ubuntu-4:~$ kubectl get pods -o wide
NAME                      READY     STATUS    RESTARTS   AGE       IP             NODE
ssh-server                1/1       Running   0          20h       10.91.1.128    ubuntu-3
ssh-server3               0/1       Pending   0          25s       <none>         <none>
ssh-server4               1/1       Running   0          1m        10.91.2.0      ubuntu-4
sshd-1-84c4bf4558-284dj   1/1       Running   0          22h       10.201.0.197   ubuntu-4
sshd-2-78f7789cc8-95srr   1/1       Running   0          21h       10.201.0.130   ubuntu-3
sshd-3-6bb86d6bf8-bq4q8   1/1       Running   0          20h       10.201.0.131   ubuntu-3


ubuntu@ubuntu-4:~$ kubectl describe pod ssh-server3
Name:         ssh-server3
Namespace:    default
Node:         <none>
Labels:       app=sshd
Annotations:  cni.projectcalico.org/ipv4pools=["10.91.2.0/26"]
Status:       Pending
IP:           
Containers:
  ssh-server-container:
    Image:        rastasheep/ubuntu-sshd:16.04
    Port:         <none>
    Environment:  <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from default-token-h52zb (ro)
Conditions:
  Type           Status
  PodScheduled   False
Volumes:
  default-token-h52zb:
    Type:        Secret (a volume populated by a Secret)
    SecretName:  default-token-h52zb
    Optional:    false
QoS Class:       BestEffort
Node-Selectors:  node_id=n3
Tolerations:     node.alpha.kubernetes.io/notReady:NoExecute for 300s
                 node.alpha.kubernetes.io/unreachable:NoExecute for 300s
Events:
  Type     Reason            Age                From               Message
  ----     ------            ----               ----               -------
  Warning  FailedScheduling  26s (x7 over 57s)  default-scheduler  No nodes are available that match all of the predicates: MatchNodeSelector (2).
```

https://github.com/projectcalico/libcalico/blob/master/calico_containers/pycalico/block.py


```  
kubectl drain ubuntu-3 --delete-local-data --force --ignore-daemonsets
kubectl delete node ubuntu-3
kubectl drain ubuntu-2 --delete-local-data --force --ignore-daemonsets
kubectl delete node ubuntu-2
```





