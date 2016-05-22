
# Enable Serial Console @ Ubuntu

The following steps will output the console to both serial and vga output

## Steps

* modify/create /etc/init/ttyS0.conf

  ```
  root@linux-cloud:/etc/grub.d# more /etc/init/ttyS0.conf
  # ttyS0 - getty
  #
  # This service maintains a getty on ttyS0 from the point the system is
  # started until it is shut down again.
  
  start on stopped rc RUNLEVEL=[2345] and (
              not-container or
              container CONTAINER=lxc or
              container CONTAINER=lxc-libvirt)
  
  stop on runlevel [!2345]
  
  pre-start script
      # getty will not be started if the serial console is not present
      stty -F /dev/ttyS0 -a 2> /dev/null > /dev/null || { stop ; exit 0; }
  end script
  
  respawn
  script
      exec /sbin/getty -L ttyS0 115200 vt102
  end script
  ```


* modify /etc/default/grub

  ```
  edit the following line:
  
  GRUB_CMDLINE_LINUX_DEFAULT="console=tty1 console=ttyS0"
  ```
