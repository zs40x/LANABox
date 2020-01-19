#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import signal
from subprocess import Popen, PIPE
import time

stopButtonPin = 40
nextButtonState = 38
continueReading = True
baseDir = "/home/pi/LANABox"
cardMappingsFile = "/home/pi/LANABoxMappings/cardmappings.csv"

# Capture SIGINT for cleanup when the script is aborted
def shutdown(signal,frame):
    global continueReading
    print("Ctrl+C captured, ending read.")
    continueReading = False
    GPIO.cleanup()

def readCardMappings():
  d = {}
  with open(cardMappingsFile, "r") as f:
    for line in f:
       (key, val) = line.split(",")
       d[key] = val
  return d

def appendNewCardIdToMappings(cardId):
  with open(cardMappingsFile, "a") as f:
    f.write(cardId + ",\n")

print("LANABox controller is running")
print("Press Ctrl-C to stop.")

signal.signal(signal.SIGINT, shutdown)
MIFAREReader = MFRC522.MFRC522()

GPIO.setmode(GPIO.BOARD)
GPIO.setup(stopButtonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(nextButtonState, GPIO.IN, pull_up_down=GPIO.PUD_UP)

lastCardId = ""
lastStopButtonState = GPIO.input(stopButtonPin)
lastNextButtonState = GPIO.input(nextButtonState)

while continueReading:

  time.sleep(0.5)

  current_state = GPIO.input(stopButtonPin)
  if current_state != lastStopButtonState:
    print("Stop Playback button pressed")
    lastStopButtonState = current_state
    subp = Popen(baseDir + "/toggle_playpause.sh", shell=True)
    subp.communicate()
       
  current_state = GPIO.input(nextButtonState)
  if current_state != lastNextButtonState:
    print("Next Track button pressed")
    lastNextButtonState = current_state
    subp = Popen(baseDir + "/next_track.sh", shell=True)
    subp.communicate()

  (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

  if status == MIFAREReader.MI_OK:
   
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    if status == MIFAREReader.MI_OK:
      cardId = str(uid[0]) + ":" + str(uid[1]) + ":" + str(uid[2]) + ":" + str(uid[3])
      
      if cardId == lastCardId:
        continue

      print("Card read UID: " + cardId)
      lastCardId = cardId
      cardMappings = readCardMappings()
      
      if cardId in cardMappings:
        trackId = cardMappings[cardId]
        if len(trackId) > 1:
          subp = Popen(baseDir + "/change_playlist.sh "+ trackId, shell=True)
          subp.communicate()
        else:
          print("Cannot play initial trackId for card " + cardId)
      else:
        print("No mapping for the card, appendig it to the mappings file")
        appendNewCardIdToMappings(cardId)
  
    
