
#!/bin/sh

echo "Will play '$1'"

mpc clear
mpc add $1
mpc play

sleep 2
mpc status > /home/pi/mpc_status
python display_track.py

mpc status
# | mail -s "LANABox Activity" "StefanMehnert+LANABox@gmail.com"
