
```
bash-4.3# docker pull jfloff/alpine-python:2.7
Warning: failed to get default registry endpoint from daemon (Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?). Using system default: https://index.docker.io/v1/
Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?
bash-4.3# systemctl docker start
Unknown operation 'docker'.
bash-4.3# systemctl start docker
bash-4.3# docker pull jfloff/alpine-python:2.7
2.7: Pulling from jfloff/alpine-python
ff3a5c916c92: Pull complete
da32d2726fe3: Pull complete
Digest: sha256:c036d927a465ed00de4e278f1707af3f61605f095c32e505b1a398dea7f69f72
Status: Downloaded newer image for jfloff/alpine-python:2.7
bash-4.3#
bash-4.3#
bash-4.3#
bash-4.3#
bash-4.3# docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
bash-4.3# docker images
REPOSITORY             TAG                 IMAGE ID            CREATED             SIZE
jfloff/alpine-python   2.7                 e7d12f060254        3 weeks ago         232MB
bash-4.3# docker run -dit --name alpine_python jfloff/alpine-python:2.7
cb32fb6a3759906343d5451c2d4d64706c63fbd36ae3ec439eae728017e78f7c
bash-4.3# docker ps
CONTAINER ID        IMAGE                      COMMAND                  CREATED             STATUS              PORTS               NAMES
cb32fb6a3759        jfloff/alpine-python:2.7   "/usr/bin/dumb-ini..."   3 seconds ago       Up 2 seconds                            alpine_python
bash-4.3# docker exec -it alpine_python bash
bash-4.4# python --version
Python 2.7.14
bash-4.4# exit
exit
bash-4.3#
```
