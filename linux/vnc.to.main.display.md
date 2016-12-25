
To use vnc with linux desktop main display (display :0), use x11vnc

* install

    ```
    apt-get install x11vnc
    ```


* setup vnc password

    ```
    x11vnc -storepasswd <password> <password file location>
    e.g:

    x11vnc -storepasswd mypassword ~/.x11vnc/passwd
    ```


* run x11vnc (manually)

    ```
    x11vnc -display :0 -rfbauth <password file location>

    e.g:
    x11vnc -display :0 -rfbauth ~/.x11vnc/passwd
    ```


