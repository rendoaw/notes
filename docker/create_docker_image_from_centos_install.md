Here is the procedure to create your own centos docker image

* Install centos on a server/VM

* After installation finish, boot the server

* do any necessary modification, e.g: yum update, yum install ..., edit /etc/..

* clean yum cache
```
yum clean all
```

* Tar the whole file system (original: http://comments.gmane.org/gmane.comp.sysutils.docker.user/5952)
```
# tar --numeric-owner --exclude=/proc --exclude=/sys --exclude=/mnt --exclude=/var/cache --exclude=/usr/share/{foomatic,backgrounds,perl5,fonts,cups,qt4,groff,kde4,icons,pixmaps,emacs,gnome-background-properties,sounds,gnome,games,desktop-directories}  --exclude=/var/log -zcvf /mnt/centos-base.tar.gz /
```

* copy the tar.gz file to docker host

* import tar.gz to docker image
```
cat centos-base.tar.gz | docker import - centos/6.5
```


