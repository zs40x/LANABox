
#!/bin/sh

echo "Will play $1"

mpc clear
mpc add $1
mpc play