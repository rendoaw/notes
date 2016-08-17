
# How to run rabbitmq on osx

* the following example is based on brew

    ```
    $ brew install rabbitmq
    
    ...deleted..
    
    Access them with `erl -man`, or add this directory to MANPATH.
    ==> Summary
    🍺  /usr/local/Cellar/erlang/19.0.2: 7,292 files, 278.6M
    ==> Installing rabbitmq
    ==> Using the sandbox
    ==> Downloading https://www.rabbitmq.com/releases/rabbitmq-server/v3.6.4/rabbitmq-server-generic-unix-3.6.4.tar.xz
    ######################################################################## 100.0%
    ==> /usr/bin/unzip -qq -j /usr/local/Cellar/rabbitmq/3.6.4/plugins/rabbitmq_management-3.6.4.ez rabbitmq_management-
    ==> Caveats
    Management Plugin enabled by default at http://localhost:15672
    
    Bash completion has been installed to:
      /usr/local/etc/bash_completion.d
    
    To have launchd start rabbitmq now and restart at login:
      brew services start rabbitmq
    Or, if you don't want/need a background service you can just run:
      rabbitmq-server
    ==> Summary
    🍺  /usr/local/Cellar/rabbitmq/3.6.4: 186 files, 5.8M, built in 15 minutes 25 seconds
    
    ```

* add rabbitmq to the path (by default, 

    ```
    $ vim ~/.bash_profile
    
    ..deleted..
    export PATH="/usr/local/sbin:$PATH"
    ..deleted..
    ```

