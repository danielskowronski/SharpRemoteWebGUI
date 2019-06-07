# Sharp Soundbar Remote Control Web GUI
Very simple Web GUI for controlling LIRC which controls Sharp Soundbar over infrared as provided remote control unit is very tiny.

## Adjusting for own needs / file list
* `index.html` has simple table based layout, change button names and signals (key names from lircd.conf)
* `sharp.py` has `sendToSharp(key)` which need adjusting 3rd param of `call` to reflect name of your lirc remote
* `lircd.conf` - use irrecord or browse internet
* `sharp.service` - systemd service file

## Demo
![](demo.jpg)