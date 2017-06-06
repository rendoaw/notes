# Troubleshooting Keystone and Memcached

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
        * if bytes close to limit_maxbytes, increase the memory/cache size
    * evictions = number of data that removed from the cache before it is expired, usually because the is no more space for new data
        * if evictions stat increases, it is time to increate the cache size. Ideally evictions should be 0
    * delete_miss
        * number of data that could not be found during delete operation, probably because of evictions.
    ...TBD..


* complete stats desciptions (from https://github.com/memcached/memcached/blob/master/doc/protocol.txt)

    ```
    
    |-----------------------+---------+-------------------------------------------|
    | Name                  | Type    | Meaning                                   |
    |-----------------------+---------+-------------------------------------------|
    | pid                   | 32u     | Process id of this server process         |
    | uptime                | 32u     | Number of secs since the server started   |
    | time                  | 32u     | current UNIX time according to the server |
    | version               | string  | Version string of this server             |
    | pointer_size          | 32      | Default size of pointers on the host OS   |
    |                       |         | (generally 32 or 64)                      |
    | rusage_user           | 32u.32u | Accumulated user time for this process    |
    |                       |         | (seconds:microseconds)                    |
    | rusage_system         | 32u.32u | Accumulated system time for this process  |
    |                       |         | (seconds:microseconds)                    |
    | curr_items            | 64u     | Current number of items stored            |
    | total_items           | 64u     | Total number of items stored since        |
    |                       |         | the server started                        |
    | bytes                 | 64u     | Current number of bytes used              |
    |                       |         | to store items                            |
    | curr_connections      | 32u     | Number of open connections                |
    | total_connections     | 32u     | Total number of connections opened since  |
    |                       |         | the server started running                |
    | rejected_connections  | 64u     | Conns rejected in maxconns_fast mode      |
    | connection_structures | 32u     | Number of connection structures allocated |
    |                       |         | by the server                             |
    | reserved_fds          | 32u     | Number of misc fds used internally        |
    | cmd_get               | 64u     | Cumulative number of retrieval reqs       |
    | cmd_set               | 64u     | Cumulative number of storage reqs         |
    | cmd_flush             | 64u     | Cumulative number of flush reqs           |
    | cmd_touch             | 64u     | Cumulative number of touch reqs           |
    | get_hits              | 64u     | Number of keys that have been requested   |
    |                       |         | and found present                         |
    | get_misses            | 64u     | Number of items that have been requested  |
    |                       |         | and not found                             |
    | get_expired           | 64u     | Number of items that have been requested  |
    |                       |         | but had already expired.                  |
    | get_flushed           | 64u     | Number of items that have been requested  |
    |                       |         | but have been flushed via flush_all       |
    | delete_misses         | 64u     | Number of deletions reqs for missing keys |
    | delete_hits           | 64u     | Number of deletion reqs resulting in      |
    |                       |         | an item being removed.                    |
    | incr_misses           | 64u     | Number of incr reqs against missing keys. |
    | incr_hits             | 64u     | Number of successful incr reqs.           |
    | decr_misses           | 64u     | Number of decr reqs against missing keys. |
    | decr_hits             | 64u     | Number of successful decr reqs.           |
    | cas_misses            | 64u     | Number of CAS reqs against missing keys.  |
    | cas_hits              | 64u     | Number of successful CAS reqs.            |
    | cas_badval            | 64u     | Number of CAS reqs for which a key was    |
    |                       |         | found, but the CAS value did not match.   |
    | touch_hits            | 64u     | Numer of keys that have been touched with |
    |                       |         | a new expiration time                     |
    | touch_misses          | 64u     | Numer of items that have been touched and |
    |                       |         | not found                                 |
    | auth_cmds             | 64u     | Number of authentication commands         |
    |                       |         | handled, success or failure.              |
    | auth_errors           | 64u     | Number of failed authentications.         |
    | idle_kicks            | 64u     | Number of connections closed due to       |
    |                       |         | reaching their idle timeout.              |
    | evictions             | 64u     | Number of valid items removed from cache  |
    |                       |         | to free memory for new items              |
    | reclaimed             | 64u     | Number of times an entry was stored using |
    |                       |         | memory from an expired entry              |
    | bytes_read            | 64u     | Total number of bytes read by this server |
    |                       |         | from network                              |
    | bytes_written         | 64u     | Total number of bytes sent by this server |
    |                       |         | to network                                |
    | limit_maxbytes        | size_t  | Number of bytes this server is allowed to |
    |                       |         | use for storage.                          |
    | accepting_conns       | bool    | Whether or not server is accepting conns  |
    | listen_disabled_num   | 64u     | Number of times server has stopped        |
    |                       |         | accepting new connections (maxconns).     |
    | time_in_listen_disabled_us                                                  |
    |                       | 64u     | Number of microseconds in maxconns.       |
    | threads               | 32u     | Number of worker threads requested.       |
    |                       |         | (see doc/threads.txt)                     |
    | conn_yields           | 64u     | Number of times any connection yielded to |
    |                       |         | another due to hitting the -R limit.      |
    | hash_power_level      | 32u     | Current size multiplier for hash table    |
    | hash_bytes            | 64u     | Bytes currently used by hash tables       |
    | hash_is_expanding     | bool    | Indicates if the hash table is being      |
    |                       |         | grown to a new size                       |
    | expired_unfetched     | 64u     | Items pulled from LRU that were never     |
    |                       |         | touched by get/incr/append/etc before     |
    |                       |         | expiring                                  |
    | evicted_unfetched     | 64u     | Items evicted from LRU that were never    |
    |                       |         | touched by get/incr/append/etc.           |
    | slab_reassign_running | bool    | If a slab page is being moved             |
    | slabs_moved           | 64u     | Total slab pages moved                    |
    | crawler_reclaimed     | 64u     | Total items freed by LRU Crawler          |
    | crawler_items-checked | 64u     | Total items examined by LRU Crawler       |
    | lrutail_reflocked     | 64u     | Times LRU tail was found with active ref. |
    |                       |         | Items can be evicted to avoid OOM errors. |
    | moves_to_cold         | 64u     | Items moved from HOT/WARM to COLD LRU's   |
    | moves_to_warm         | 64u     | Items moved from COLD to WARM LRU         |
    | moves_within_lru      | 64u     | Items reshuffled within HOT or WARM LRU's |
    | direct_reclaims       | 64u     | Times worker threads had to directly      |
    |                       |         | reclaim or evict items.                   |
    | lru_crawler_starts    | 64u     | Times an LRU crawler was started          |
    | lru_maintainer_juggles                                                      |
    |                       | 64u     | Number of times the LRU bg thread woke up |
    | slab_global_page_pool | 32u     | Slab pages returned to global pool for    |
    |                       |         | reassignment to other slab classes.       |
    | slab_reassign_rescues | 64u     | Items rescued from eviction in page move  |
    | slab_reassign_evictions_nomem                                               |
    |                       | 64u     | Valid items evicted during a page move    |
    |                       |         | (due to no free memory in slab)           |
    | slab_reassign_chunk_rescues                                                 |
    |                       | 64u     | Individual sections of an item rescued    |
    |                       |         | during a page move.                       |
    | slab_reassign_inline_reclaim                                                |
    |                       | 64u     | Internal stat counter for when the page   |
    |                       |         | mover clears memory from the chunk        |
    |                       |         | freelist when it wasn't expecting to.     |
    | slab_reassign_busy_items                                                    |
    |                       | 64u     | Items busy during page move, requiring a  |
    |                       |         | retry before page can be moved.           |
    | log_worker_dropped    | 64u     | Logs a worker never wrote due to full buf |
    | log_worker_written    | 64u     | Logs written by a worker, to be picked up |
    | log_watcher_skipped   | 64u     | Logs not sent to slow watchers.           |
    | log_watcher_sent      | 64u     | Logs written to watchers.                 |
    |-----------------------+---------+-------------------------------------------|
    
    ```

* useful links 
    * https://github.com/memcached/memcached/blob/master/doc/protocol.txt
    * http://work.tinou.com/2011/04/memcached-for-dummies.html   
    * https://blog.engineyard.com/2015/fine-tuning-memcached
    * https://skuicloud.wordpress.com/2014/11/15/openstack-memcached-for-keystone/
