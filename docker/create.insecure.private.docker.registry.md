
# Create private docker registry


## prepare the folder (we are going to put the repository and certs file outside the container)

```
# mkdir -p /data
# mkdir -p /data/docker
# mkdir -p /data/docker/registry
# mkdir -p /data/docker/registry/certs
```


## modify openssl cnf to add IP SAN into certificates

* location
  * centos 6:  /etc/pki/tls/openssl.cnf
  * ubuntu  : /etc/ssl/openssl.cnf
  
* edit the file, add/modify the folowing section

  ```
  [ CA_default ]
  # Extension copying option: use with caution.
  copy_extensions = copy
  
  [ v3_ca ]
  subjectAltName      = @alternate_names
  keyUsage = digitalSignature, keyEncipherment
  
  [ alternate_names ]
  
  DNS.1        = myserver
  DNS.2        = myserver.net
  IP.1 = 127.0.0.1
  IP.2 = 192.168.100.100
  ```

## Create private/self signing certificate

* create private key and CA signing request

  ```
  # cd /data/docker/registry/certs
  
  # openssl req -newkey rsa:2048 -nodes -keyout domain.key -out domain.csr
  Generating a 2048 bit RSA private key
  ....................................................................+++
  ......................................................................................................................................................+++
  writing new private key to 'domain.key'
  -----
  You are about to be asked to enter information that will be incorporated
  into your certificate request.
  What you are about to enter is what is called a Distinguished Name or a DN.
  There are quite a few fields but you can leave some blank
  For some fields there will be a default value,
  If you enter '.', the field will be left blank.
  -----
  Country Name (2 letter code) [AU]:ID
  State or Province Name (full name) [Some-State]:Jakarta
  Locality Name (eg, city) []:Jakarta
  Organization Name (eg, company) [Internet Widgits Pty Ltd]:inet0
  Organizational Unit Name (eg, section) []:home
  Common Name (e.g. server FQDN or YOUR name) []:micro
  Email Address []:rendo@inet0.net
  
  Please enter the following 'extra' attributes
  to be sent with your certificate request
  A challenge password []:
  An optional company name []:
  ```

* create server certificate

  ```
  # openssl req -newkey rsa:2048 -nodes -keyout domain.key -x509 -days 3650 -out domain.crt
  Generating a 2048 bit RSA private key
  ........................................................................................+++
  ...............................................+++
  writing new private key to 'domain.key'
  -----
  You are about to be asked to enter information that will be incorporated
  into your certificate request.
  What you are about to enter is what is called a Distinguished Name or a DN.
  There are quite a few fields but you can leave some blank
  For some fields there will be a default value,
  If you enter '.', the field will be left blank.
  -----
  Country Name (2 letter code) [AU]:ID
  State or Province Name (full name) [Some-State]:Jakarta
  Locality Name (eg, city) []:Jakarta
  Organization Name (eg, company) [Internet Widgits Pty Ltd]:inet0
  Organizational Unit Name (eg, section) []:home
  Common Name (e.g. server FQDN or YOUR name) []:micro
  Email Address []:rendo@inet0.net
  ```

* create combined private and client cert

  ```
  # openssl pkcs12 -inkey domain.key -in domain.crt -export -out domain.pfx
  Enter Export Password:
  Verifying - Enter Export Password:
  
  # openssl pkcs12 -in domain.pfx -nodes -out domain.combined.crt
  Enter Import Password:
  MAC verified OK
  
  # cp domain.combined.crt domain.pem
  ```

## run the registry

* download and run docker for registry container
  
  ```
  # docker run -d -p 5000:5000 --restart=always --name registry -v /data/docker/registry/data:/var/lib/registry -v /data/docker/registry/certs:/certs -e REGISTRY_HTTP_TLS_CERTIFICATE=/certs/domain.crt -e REGISTRY_HTTP_TLS_KEY=/certs/domain.key registry:2
  Unable to find image 'registry:2' locally
  2: Pulling from library/registry
  5c90d4a2d1a8: Pull complete
  fb8b2153aae6: Pull complete
  f719459a7672: Pull complete
  fa42982c9892: Pull complete
  Digest: sha256:504b44c0ca43f9243ffa6feaf3934dd57895aece36b87bc25713588cdad3dd10
  Status: Downloaded newer image for registry:2
  8686d7073a386f3403466665a02bbf6f755541cae0daa708b30d8844a316c376
  ```

## Test the registry

* lets pick one existing image and push it to our new private registry

  ```
  # docker images
  REPOSITORY                         TAG                 IMAGE ID            CREATED             SIZE
  ...
  ubuntu                             14.04               8f1bd21bd25c        3 weeks ago         188 MB
  ...
  
  # docker tag 8f1bd21bd25c micro.home.inet0.net:5000/ubuntu:14.04
  
  # docker push micro.home.inet0.net:5000/ubuntu:14.04
  The push refers to a repository [micro.home.inet0.net:5000/ubuntu]
  Get https://micro.home.inet0.net:5000/v1/_ping: x509: certificate signed by unknown authority
  ```

* ok, since we are using self signed certificate, we need to tell docker to connect to it in insecure mode

* modify the docker config

  ```
  # ubuntu
  add DOCKER_OPTS="$DOCKER_OPTS --insecure-registry micro.home.inet0.net:5000"  to /etc/default/docker
  
  # centos 6
  add other_args="--insecure-registry 172.25.152.2:5000"" to /etc/sysconfig/docker
  
  # centos 7
  add --insecure-registry 172.25.152.2:5000 at the end of "ExecStart" line inside /lib/systemd/system/docker.service
  ```
  
* restart docker service

  ```
  # service docker restart
  ```

* try push again

  ```
  # docker push micro.home.inet0.net:5000/ubuntu:14.04
  The push refers to a repository [micro.home.inet0.net:5000/ubuntu]
  5f70bf18a086: Pushed
  6f8be37bd578: Pushed
  9f7ab087e6e6: Pushed
  dc109d4b4ccf: Pushed
  a7e1c363defb: Pushed
  14.04: digest: sha256:8a8665b4568a56accf58dca75cf31a278ae2749d4a4bf31a861710eaa1ec4f01 size: 1358
  ```

* success!

