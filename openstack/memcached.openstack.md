# Memcached and Keystone

* To increase memcache size (example below will set cache size to 2G)

    ```
    # cat /etc/memcached.conf
    ...deleted...
    # Start with a cap of 64 megs of memory. It's reasonable, and the daemon default
    # Note that the daemon will grow to this size, but does not start out holding this much
    # memory
    -m 2000
    
    ...deleted...
    ```
  
* check memcache statistics

    ```
    # echo stats | nc 127.0.0.1 11211
    STAT pid 23838
    STAT uptime 1649
    STAT time 1469670161
    STAT version 1.4.14 (Ubuntu)
    STAT libevent 2.0.21-stable
    STAT pointer_size 64
    STAT rusage_user 0.653584
    STAT rusage_system 2.220942
    STAT curr_connections 37
    STAT total_connections 6217
    STAT connection_structures 39
    STAT reserved_fds 20
    STAT cmd_get 11179
    STAT cmd_set 8280
    STAT cmd_flush 0
    STAT cmd_touch 0
    STAT get_hits 8438
    STAT get_misses 2741
    STAT delete_misses 0
    STAT delete_hits 2717
    STAT incr_misses 0
    STAT incr_hits 0
    STAT decr_misses 0
    STAT decr_hits 0
    STAT cas_misses 0
    STAT cas_hits 0
    STAT cas_badval 0
    STAT touch_hits 0
    STAT touch_misses 0
    STAT auth_cmds 0
    STAT auth_errors 0
    STAT bytes_read 271037105
    STAT bytes_written 281414918
    STAT limit_maxbytes 2097152000
    STAT accepting_conns 1
    STAT listen_disabled_num 0
    STAT threads 4
    STAT conn_yields 0
    STAT hash_power_level 16
    STAT hash_bytes 524288
    STAT hash_is_expanding 0
    STAT expired_unfetched 0
    STAT evicted_unfetched 0
    STAT bytes 9985244
    STAT curr_items 2722
    STAT total_items 8151
    STAT evictions 0
    STAT reclaimed 0
    END
    ```
    
* important stats

    * limit_maxbytes = max cache size
    * bytes = current utilization
    ...TBD..
