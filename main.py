#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import signal
from subprocess import Popen, PIPE
import time

stop_button_pin = 40
next_button_pin = 38
continue_reading = True
baseDir = "/home/pi/LANABox"

# Capture SIGINT for cleanup when the script is aborted
def shutdown(signal,frame):
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()


print("Musicbox controller is running")
print("Press Ctrl-C to stop.")

signal.signal(signal.SIGINT, shutdown)
MIFAREReader = MFRC522.MFRC522()

GPIO.setmode(GPIO.BOARD)
GPIO.setup(stop_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(next_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while continue_reading:

  button_state = GPIO.input(stop_button_pin)
  if button_state == False:
    print("Stop Playback button pressed")
    subp = Popen(baseDir + "/toggle_playpause.sh", shell=True)
    subp.communicate()
       
  button_state = GPIO.input(next_button_pin)
  if button_state == False:
    print("Next Track button pressed")
    subp = Popen(baseDir + "/next_track.sh", shell=True)
    subp.communicate()

  (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

  if status == MIFAREReader.MI_OK:
    print("Card detected")
    
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    if status == MIFAREReader.MI_OK:
      print("Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]))

      file = open(baseDir + "/cardmappings.csv", "r") 
      trackid = file.readline() 
      print(trackid)

      if uid[0] == 49 and uid[1] == 182 and uid[2] == 230 and uid[3] == 43:
        subp = Popen(baseDir + "/change_playlist.sh "+ trackid, shell=True)
        subp.communicate()
  else:
    time.sleep(0.5)
