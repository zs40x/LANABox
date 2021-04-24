import drivers

display = drivers.Lcd()

file = open("/home/pi/mpc_status", "r")
lines = file.readlines()

if len(lines) > 2:
  print(lines[0])
  display.lcd_display_string(str(lines[0]), 1)
  display.lcd_display_string(str(lines[1]), 2)
else:
  display.lcd_clear()
  display.lcd_display_string("LANABox2 :-)", 1)
  display.lcd_display_string("-", 2)
