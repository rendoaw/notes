
* product
  * https://www.amazon.com/gp/product/B009YRP906/ref=oh_aui_detailpage_o00_s00?ie=UTF8&psc=1


* software

    ```
    # wget -q http://dl.panticz.de/pcsensor/pcsensor -O /usr/local/bin/pcsensor
    # chmod +x /usr/local/bin/pcsensor
    ```

* sample output

    ```
    # /usr/local/bin/pcsensor
    2016/07/23 19:57:07 Temperature 101.75F 38.75C
    ```

* as comparison, here is the internal CPU temperature

    ```
    # sensors
    coretemp-isa-0000
    Adapter: ISA adapter
    Core 0:       +38.0°C  (high = +80.0°C, crit = +96.0°C)
    Core 1:       +42.0°C  (high = +80.0°C, crit = +96.0°C)
    Core 2:       +33.0°C  (high = +80.0°C, crit = +96.0°C)
    Core 8:       +39.0°C  (high = +80.0°C, crit = +96.0°C)
    Core 9:       +41.0°C  (high = +80.0°C, crit = +96.0°C)
    Core 10:      +40.0°C  (high = +80.0°C, crit = +96.0°C)
    
    coretemp-isa-0001
    Adapter: ISA adapter
    Core 0:       +34.0°C  (high = +80.0°C, crit = +96.0°C)
    Core 1:       +37.0°C  (high = +80.0°C, crit = +96.0°C)
    Core 2:       +32.0°C  (high = +80.0°C, crit = +96.0°C)
    Core 8:       +30.0°C  (high = +80.0°C, crit = +96.0°C)
    Core 9:       +36.0°C  (high = +80.0°C, crit = +96.0°C)
    Core 10:      +34.0°C  (high = +80.0°C, crit = +96.0°C)
    ```


* Simple alert/monitorig script

    ```
    # cat check_temperature.sh
    #!/bin/bash
    
    i=`/usr/local/bin/pcsensor | awk '{print $5}' | sed 's/C//'`
    echo $i;
    int=${i%.*}
    if [ $int -gt 35 ]; then
     /usr/local/bin/pcsensor | mail -r sender@domain.net  -s "Room Temperature Alert" recepient@domain.com
    fi
    
    for i in `sensors -u | grep _input | awk '{print $2}'`; do
     echo $i;
     int=${i%.*}
     if [ $int -gt 50 ]; then
         sensors | mail -r sender@domain.net  -s "Server CPU Temperature Alert" recepient@domain.com
         exit 1
     fi
    done

 
    # cat /etc/crontab
    ...deleted...
    # m h dom mon dow user	command
    */15 *	* * *	root    /home/users/check_temperature.sh
    ...deleted...
    ```


* lsub result

  ```
  root@micro:/home/rendo# cat lsusb.txt
  Bus 006 Device 004: ID 0c45:7401 Microdia
  Device Descriptor:
    bLength                18
    bDescriptorType         1
    bcdUSB               2.00
    bDeviceClass            0 (Defined at Interface level)
    bDeviceSubClass         0
    bDeviceProtocol         0
    bMaxPacketSize0         8
    idVendor           0x0c45 Microdia
    idProduct          0x7401
    bcdDevice            0.01
    iManufacturer           1 RDing
    iProduct                2 TEMPerV1.4
    iSerial                 0
    bNumConfigurations      1
    Configuration Descriptor:
      bLength                 9
      bDescriptorType         2
      wTotalLength           59
      bNumInterfaces          2
      bConfigurationValue     1
      iConfiguration          0
      bmAttributes         0xa0
        (Bus Powered)
        Remote Wakeup
      MaxPower              100mA
      Interface Descriptor:
        bLength                 9
        bDescriptorType         4
        bInterfaceNumber        0
        bAlternateSetting       0
        bNumEndpoints           1
        bInterfaceClass         3 Human Interface Device
        bInterfaceSubClass      1 Boot Interface Subclass
        bInterfaceProtocol      1 Keyboard
        iInterface              0
          HID Device Descriptor:
            bLength                 9
            bDescriptorType        33
            bcdHID               1.10
            bCountryCode            0 Not supported
            bNumDescriptors         1
            bDescriptorType        34 Report
            wDescriptorLength      65
            Report Descriptor: (length is 65)
              Item(Global): Usage Page, data= [ 0x01 ] 1
                              Generic Desktop Controls
              Item(Local ): Usage, data= [ 0x06 ] 6
                              Keyboard
              Item(Main  ): Collection, data= [ 0x01 ] 1
                              Application
              Item(Global): Report ID, data= [ 0x01 ] 1
              Item(Global): Usage Page, data= [ 0x07 ] 7
                              Keyboard
              Item(Local ): Usage Minimum, data= [ 0xe0 ] 224
                              Control Left
              Item(Local ): Usage Maximum, data= [ 0xe7 ] 231
                              GUI Right
              Item(Global): Logical Minimum, data= [ 0x00 ] 0
              Item(Global): Logical Maximum, data= [ 0x01 ] 1
              Item(Global): Report Size, data= [ 0x01 ] 1
              Item(Global): Report Count, data= [ 0x08 ] 8
              Item(Main  ): Input, data= [ 0x02 ] 2
                              Data Variable Absolute No_Wrap Linear
                              Preferred_State No_Null_Position Non_Volatile Bitfield
              Item(Global): Report Count, data= [ 0x01 ] 1
              Item(Global): Report Size, data= [ 0x08 ] 8
              Item(Main  ): Input, data= [ 0x01 ] 1
                              Constant Array Absolute No_Wrap Linear
                              Preferred_State No_Null_Position Non_Volatile Bitfield
              Item(Global): Report Count, data= [ 0x03 ] 3
              Item(Global): Report Size, data= [ 0x01 ] 1
              Item(Global): Usage Page, data= [ 0x08 ] 8
                              LEDs
              Item(Local ): Usage Minimum, data= [ 0x01 ] 1
                              NumLock
              Item(Local ): Usage Maximum, data= [ 0x03 ] 3
                              Scroll Lock
              Item(Main  ): Output, data= [ 0x02 ] 2
                              Data Variable Absolute No_Wrap Linear
                              Preferred_State No_Null_Position Non_Volatile Bitfield
              Item(Global): Report Count, data= [ 0x05 ] 5
              Item(Global): Report Size, data= [ 0x01 ] 1
              Item(Main  ): Output, data= [ 0x01 ] 1
                              Constant Array Absolute No_Wrap Linear
                              Preferred_State No_Null_Position Non_Volatile Bitfield
              Item(Global): Report Count, data= [ 0x05 ] 5
              Item(Global): Report Size, data= [ 0x08 ] 8
              Item(Global): Logical Minimum, data= [ 0x00 ] 0
              Item(Global): Logical Maximum, data= [ 0xff ] 255
              Item(Global): Usage Page, data= [ 0x07 ] 7
                              Keyboard
              Item(Local ): Usage Minimum, data= [ 0x00 ] 0
                              No Event
              Item(Local ): Usage Maximum, data= [ 0xff ] 255
                              (null)
              Item(Main  ): Input, data= [ 0x00 ] 0
                              Data Array Absolute No_Wrap Linear
                              Preferred_State No_Null_Position Non_Volatile Bitfield
              Item(Main  ): End Collection, data=none
        Endpoint Descriptor:
          bLength                 7
          bDescriptorType         5
          bEndpointAddress     0x81  EP 1 IN
          bmAttributes            3
            Transfer Type            Interrupt
            Synch Type               None
            Usage Type               Data
          wMaxPacketSize     0x0008  1x 8 bytes
          bInterval              10
      Interface Descriptor:
        bLength                 9
        bDescriptorType         4
        bInterfaceNumber        1
        bAlternateSetting       0
        bNumEndpoints           1
        bInterfaceClass         3 Human Interface Device
        bInterfaceSubClass      1 Boot Interface Subclass
        bInterfaceProtocol      2 Mouse
        iInterface              0
          HID Device Descriptor:
            bLength                 9
            bDescriptorType        33
            bcdHID               1.10
            bCountryCode            0 Not supported
            bNumDescriptors         1
            bDescriptorType        34 Report
            wDescriptorLength      41
            Report Descriptor: (length is 41)
              Item(Global): Usage Page, data= [ 0x00 0xff ] 65280
                              (null)
              Item(Local ): Usage, data= [ 0x01 ] 1
                              (null)
              Item(Main  ): Collection, data= [ 0x01 ] 1
                              Application
              Item(Local ): Usage, data= [ 0x01 ] 1
                              (null)
              Item(Global): Logical Minimum, data= [ 0x00 ] 0
              Item(Global): Logical Maximum, data= [ 0xff 0x00 ] 255
              Item(Global): Report Size, data= [ 0x08 ] 8
              Item(Global): Report Count, data= [ 0x08 ] 8
              Item(Main  ): Input, data= [ 0x02 ] 2
                              Data Variable Absolute No_Wrap Linear
                              Preferred_State No_Null_Position Non_Volatile Bitfield
              Item(Local ): Usage, data= [ 0x01 ] 1
                              (null)
              Item(Global): Report Count, data= [ 0x08 ] 8
              Item(Main  ): Output, data= [ 0x02 ] 2
                              Data Variable Absolute No_Wrap Linear
                              Preferred_State No_Null_Position Non_Volatile Bitfield
              Item(Global): Usage Page, data= [ 0x0c ] 12
                              Consumer
              Item(Local ): Usage, data= [ 0x00 ] 0
                              Unassigned
              Item(Global): Logical Minimum, data= [ 0x80 ] 128
              Item(Global): Logical Maximum, data= [ 0x7f ] 127
              Item(Global): Report Size, data= [ 0x08 ] 8
              Item(Global): Report Count, data= [ 0x08 ] 8
              Item(Main  ): Feature, data= [ 0x02 ] 2
                              Data Variable Absolute No_Wrap Linear
                              Preferred_State No_Null_Position Non_Volatile Bitfield
              Item(Main  ): End Collection, data=none
        Endpoint Descriptor:
          bLength                 7
          bDescriptorType         5
          bEndpointAddress     0x82  EP 2 IN
          bmAttributes            3
            Transfer Type            Interrupt
            Synch Type               None
            Usage Type               Data
          wMaxPacketSize     0x0008  1x 8 bytes
          bInterval              10
  Device Status:     0x0000
    (Bus Powered)
  ```
