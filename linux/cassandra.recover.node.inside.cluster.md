# How to recover Cassandra database 

## Overview
* It is possible that the database become corrupt, for example due to server power failure
* The recovery procedure could be different depend on the problem and on the role of the database node


## Common failure

#### DB corrupt on Cassandra non-seed node

* Make sure if this node is not cassandra seed node
    * check /opt/apps/data/apache-cassandra/conf/cassandra.yaml  (please adjust the config folder location accordingly)
    * find entry similar to 
        
        ```
                - seeds: 1.25.152.237
        ```

    * compare the seed IP with this node local IP.
    * If the seed node != this node local IP, it means this node is not seed node.

* shutdown cassandra process (the example below assumes that cassandra is monitored by supervisord)

    ```
    [root@server-03 root]# supervisorctl stop group1:cassandra
    ```

* delete all cassandra data (please adjust the data folder location accordingly)

    ```
    [root@server-03 root]# rm -rf /opt/apps/data/apache-cassandra/data/*
    ```

* start cassandra process (the example below assumes that cassandra is monitored by supervisord)

    ```
    [root@server-03 root]# supervisorctl start group1:cassandra
    ```


#### DB corrupt on Cassandra seed node

* Make sure if this node is cassandra seed node
    * check /opt/apps/data/apache-cassandra/conf/cassandra.yaml (please adjust the config folder location accordingly)
    * find entry similar to 
        
        ```
                - seeds: 1.25.152.237
        ```
    * compare the seed IP with this node local IP.
    * If the seed node == this node local IP, it means this node is seed node.

* Promote other node as temporary seed node
    * Modify the seed configuration, point seeds IP to other existing node that currently running fine

        ```
                - seeds: 1.25.152.239
        ```

    * if initially it has 2 or more seed IP listed, only remove the one that same as local IP
    

* shutdown cassandra process (the example below assumes that cassandra is monitored by supervisord)

    ```
    [root@server-03 root]# supervisorctl stop group1:cassandra
    ```

* delete all cassandra data (please adjust the data folder location accordingly)

    ```
    [root@server-03 root]# rm -rf /opt/apps/data/apache-cassandra/data/*
    ```

* start cassandra process (the example below assumes that cassandra is monitored by supervisord)

    ```
    [root@server-03 root]# supervisorctl start group1:cassandra
    ```

* use nodetool command to see if this node already synced

    ```
    [root@server-03 root]# nodetool status

    ....

    Database status:
    Datacenter: datacenter1
    =======================
    Status=Up/Down
    |/ State=Normal/Leaving/Joining/Moving
    --  Address       Load       Tokens       Owns    Host ID                               Rack
    UN  1.25.152.237  86.71 MB   256          ?       8bdd484e-a957-4403-8ed5-67b65cdd2598  rack1
    UN  1.25.152.239  88.49 MB   256          ?       767062f9-9383-4fdb-8d76-c91dbd101ac0  rack1
    UN  1.25.152.241  105.15 MB  256          ?       253b3dec-b795-499e-81de-17989ed47664  rack1

    ...

    ```

* Because the way of Cassandra work, there is no exact indicator when the data is sync. Depend on the size of your data, it could take minutes or hours. Generally, if the Load value is similar, we can say that the new node is already been bootstraped. 

* If the new seed looks like have finish the bootstrap process (the load is not change that much anymore), we can shutdown the cassandra process again, and put its local IP to the seeds list.

    ```
          - seeds: 1.25.152.237, 1.25.152.239
    ```

* If your server only have one seed, it is best practice to add the second seed. You can pick any one of the existing node as second seed. But do not add all nodes as seed.

* start cassandra again



#### Node down temporarily

* Regardless the node is seed node or not, if it is down less than 10 days, simply start the cassandra on that node. 
* But, if the node is down > 10 days or 864000 seconds, please follow the same procedure as DB corrupt above.


