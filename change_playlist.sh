
#!/bin/sh

echo "Will play '$1'"

mpc clear
mpc add $1
mpc play

sleep 2
mpc status | mail -s "LANABox Activity" "StefanMehnert+LANABox@gmail.com"
