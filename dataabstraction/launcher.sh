#!bin/sh
# launcher.sh
# navigate to home directory and run python script to log sensor data into DB

cd /home/pi
su pi -c 'node /home/pi/mysqlliteexample.js&'
sudo python notification.py&
sudo python getsensordata.py

# if this doesn't work try again (upto a total of 3 times)
sudo python getsensordata.py
# one last time
sudo python getsensordata.py 
