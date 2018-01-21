

* for wlanX and ethX naming
  * delete symlink to /dev/null  /etc/systemd/network/99-default.link
  * Replace with a text file /etc/systemd/network/99-default.link that contains

    ```
    [Link]
    NamePolicy=kernel database onboard slot path mac
    MACAddressPolicy=persistent
    ```
