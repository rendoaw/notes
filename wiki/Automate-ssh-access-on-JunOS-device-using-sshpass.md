# Automate ssh access on JunOS device using sshpass

This is an alternative way to mass configuring/accessing multiple devices at once, by using sshpass

* create a simple general purpose script

    ```
    $ cat ssh_multiple.bat

    #!/bin/bash

    user=$1
    passwd=$2
    target=$3
    cmd=$4

    for host in $target; do
        echo
        echo "Accessing $host ...."
        sshpass -p ${passwd} ssh ${user}@${host} "$cmd"
    done
    ```


* run the script, for example to enable telnet

    ```
    ./ssh_multiple.bat myuser mypassword "r1 r2 r3 r4" "configure;set system services telnet;commit synchronize;exit"
    ```


