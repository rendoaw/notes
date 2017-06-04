
* split big tcpdump file to smaller files

    ```
    tcpdump -r big_file -w new_small_files -C <size in MB>
    ```

* remove first N bytes from each packet

    ```
    # editcap -C <N bytes> -F pcap source.pcap new.pcap
    ```

