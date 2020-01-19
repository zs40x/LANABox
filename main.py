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

def readCardMappings():
  d = {}
  with open(baseDir + "/cardmappings.csv", "r") as f:
    for line in f:
       (key, val) = line.split(";")
       d[key] = val
  return d

print("Musicbox controller is running")
print("Press Ctrl-C to stop.")

signal.signal(signal.SIGINT, shutdown)
MIFAREReader = MFRC522.MFRC522()

GPIO.setmode(GPIO.BOARD)
GPIO.setup(stop_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(next_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

lastCardId = ""
last_stop_button_state = GPIO.input(stop_button_pin)
last_next_button_state = GPIO.input(next_button_pin)

while continue_reading:

  time.sleep(0.5)

  current_state = GPIO.input(stop_button_pin)
  if current_state != last_stop_button_state:
    print("Stop Playback button pressed")
    last_stop_button_state = current_state
    subp = Popen(baseDir + "/toggle_playpause.sh", shell=True)
    subp.communicate()
       
  current_state = GPIO.input(next_button_pin)
  if current_state != last_next_button_state:
    print("Next Track button pressed")
    last_next_button_state = current_state
    subp = Popen(baseDir + "/next_track.sh", shell=True)
    subp.communicate()

  (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

  if status == MIFAREReader.MI_OK:
    print("Card detected")
    
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    if status == MIFAREReader.MI_OK:
      cardId = str(uid[0]) + ":" + str(uid[1]) + ":" + str(uid[2]) + ":" + str(uid[3])
      
      if cardId != lastCardId:
        continue

      print("Card read UID: " + cardId)
     
      cardMappings = readCardMappings()
      
      if cardId in cardMappings:
        trackid = cardMappings[cardId]
        subp = Popen(baseDir + "/change_playlist.sh "+ trackid, shell=True)
        subp.communicate()
      else:
        print("No mapping for the card")
  
    
