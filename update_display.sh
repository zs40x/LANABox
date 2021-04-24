
#!/bin/sh

mpc status > /home/pi/mpc_status
python /home/pi/LANABox/display_track.py
