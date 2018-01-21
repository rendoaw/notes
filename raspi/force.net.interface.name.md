

* for wlanX and ethX naming
  * from https://www.raspberrypi.org/forums/viewtopic.php?t=197537
  * delete symlink to /dev/null  /etc/systemd/network/99-default.link
  * Replace with a text file /etc/systemd/network/99-default.link that contains

    ```
    [Link]
    NamePolicy=kernel database onboard slot path mac
    MACAddressPolicy=persistent
    ```
