
```
docker run -d -it --name elk --restart=always -v /data/docker/elk/elasticsearch:/var/lib/elasticsearch -p 9200:9200 -p 5601:5601  rendoaw/ubuntu_netkit
docker run -d -it --name nextcloud --restart=always -v /data/docker/nextcloud:/data -p 10080:80 nextcloud
docker run -d -it --net=host --name openr_test3 --privileged --restart=always  rendoaw/openr:test3

docker pull docker.elastic.co/logstash/logstash-oss:6.1.2
docker run -d -it --name logstash --restart=always -p 9300:9300  logstash-oss:6.1.2

docker run -d -it --name cacti -p 10081:80  quantumobject/docker-cacti
```
