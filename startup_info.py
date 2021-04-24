#! /usr/bin/env python

import drivers
from time import sleep
from datetime import datetime
from subprocess import check_output
display = drivers.Lcd()
Host = check_output(["hostname"]).split()[0]
IP = ""

while len(IP) < 1:
  output = check_output(["hostname", "-I"])
  if len(output.split()) > 0:
	IP = output.split()[0]

print("Display Startup Message on Display")
sleep(5)
display.lcd_display_string(str(Host), 1)
display.lcd_display_string(str(IP), 2)
