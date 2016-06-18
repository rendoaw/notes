
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
  
  DNS.1        = micro
  DNS.2        = micro.inet0.net
  DNS.3        = micro.home.inet0.net
  IP.1 = 127.0.0.1
  IP.2 = 192.168.1.17
  IP.3 = 10.14.0.1
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
  
* verify if our certificate is correct and contain both hostname and IP address

  ```
  # openssl x509 -in domain.crt -text -noout
  Certificate:
      Data:
          Version: 3 (0x2)
          Serial Number: 11031869021798596984 (0x9919126d0cf10178)
      Signature Algorithm: sha256WithRSAEncryption
          Issuer: C=ID, ST=Jakarta, L=Jakarta, O=inet0, OU=home, CN=micro/emailAddress=rendo@inet0.net
          Validity
              Not Before: Jun 18 15:36:15 2016 GMT
              Not After : Jun 16 15:36:15 2026 GMT
          Subject: C=ID, ST=Jakarta, L=Jakarta, O=inet0, OU=home, CN=micro/emailAddress=rendo@inet0.net
          Subject Public Key Info:
              Public Key Algorithm: rsaEncryption
                  Public-Key: (2048 bit)
                  Modulus:
                      00:d3:ff:43:88:7e:67:c8:34:33:f6:54:be:c6:dd:
                      74:f7:08:ae:88:b3:17:ce:7f:e7:6b:8e:9e:85:1b:
                      53:bf:3a:04:87:b9:75:bc:28:49:69:6a:ed:cb:8c:
                      e8:ab:0d:73:c3:2b:c9:4f:0f:ab:5f:4e:e3:47:15:
                      e5:59:ed:b7:5d:3a:03:e1:09:0a:dc:46:f0:58:13:
                      fb:d4:85:e5:5b:f5:ec:80:bb:8d:8a:dd:b4:1e:36:
                      66:52:0c:d3:41:39:ed:dc:ab:1a:e8:f4:5b:ef:3b:
                      38:ec:17:8a:6b:8e:d6:6f:b0:0a:a3:99:df:34:c1:
                      f7:06:6a:66:9f:ab:f6:41:27:c5:16:a3:f4:8b:cd:
                      9f:9d:a7:46:9b:2e:f6:3d:e4:70:ba:b4:64:2e:b8:
                      0a:ab:81:84:c0:1d:af:84:5e:b0:2e:85:c8:bc:79:
                      a5:88:af:8c:ff:4d:71:2e:e4:b6:03:cb:09:aa:25:
                      c8:db:42:42:fb:e4:20:73:86:13:72:d7:2f:00:a4:
                      1d:23:19:d7:5c:fb:f9:f1:8c:27:ac:d2:07:16:16:
                      a6:d3:8d:57:eb:29:ea:bd:6a:eb:3c:f6:1c:ea:20:
                      3d:35:7e:cf:3a:ea:a5:7d:d0:be:d9:6e:5e:56:e8:
                      85:1c:c1:38:85:33:e8:2d:b7:f2:b8:c4:ea:d9:d2:
                      ec:29
                  Exponent: 65537 (0x10001)
          X509v3 extensions:
              X509v3 Subject Alternative Name:
                  DNS:micro, DNS:micro.inet0.net, DNS:micro.home.inet0.net, IP Address:192.168.1.17, IP Address:10.14.0.1, IP Address:10.15.0.1
              X509v3 Key Usage:
                  Digital Signature, Key Encipherment
              X509v3 Subject Key Identifier:
                  01:BB:65:EA:0D:81:DE:0A:ED:91:4D:90:E3:75:C2:91:45:D0:F7:96
              X509v3 Authority Key Identifier:
                  keyid:01:BB:65:EA:0D:81:DE:0A:ED:91:4D:90:E3:75:C2:91:45:D0:F7:96
  
              X509v3 Basic Constraints:
                  CA:TRUE
      Signature Algorithm: sha256WithRSAEncryption
           b6:ee:c9:1c:e2:77:2e:db:90:ed:14:5e:30:17:b8:53:60:7a:
           03:cd:30:36:38:a4:05:64:a1:67:6b:71:95:ee:7f:50:a8:f8:
           28:1f:c1:49:5d:59:7f:59:0f:14:5b:61:2a:c9:08:e5:59:9f:
           dd:4a:6f:b2:4d:1e:80:54:f2:c7:b9:58:56:71:fe:19:c4:44:
           e1:a7:d3:ee:33:04:b1:d0:df:77:80:77:18:e0:44:6c:d4:5b:
           e2:05:c3:b6:12:80:3f:7f:ff:df:2c:ee:b3:6a:5e:26:59:81:
           11:f6:e0:0a:08:c6:1b:72:1b:c1:65:a3:69:16:23:06:72:8b:
           6d:31:c5:83:2b:b3:87:fd:b0:67:80:b8:c1:51:f5:50:40:60:
           c0:fd:27:5f:38:22:ed:8d:25:10:f0:01:4e:48:07:57:5d:9d:
           8b:43:2a:f1:1f:d6:c5:0c:d5:9f:ff:94:1d:c2:75:db:30:57:
           ef:3a:bb:c9:87:bf:f2:83:fc:27:36:9d:5e:53:f9:17:3d:a3:
           5b:da:31:ef:26:66:3d:db:eb:98:6e:97:ec:3d:54:6a:21:57:
           66:68:b0:87:cc:65:f7:14:4e:07:4e:45:43:38:47:be:19:91:
           88:1b:1b:b2:d2:6d:37:f5:85:f3:f9:05:1b:c3:e4:6b:c1:95:
           c5:5f:1d:9b
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

