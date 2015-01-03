#!/usr/bin/python

import sqlite3 
import spidev
import time
import os
import glob

#globals
dbname='/home/pi/nodedb.db'
vref_val = 3.3
#vref_val = 5.0
 
# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)
 
# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
def ReadChannel(channel):
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data
 
# Function to convert data to voltage level,
# rounded to specified number of decimal places.
def ConvertVolts(data,places,vref_val):
  volts = (data * vref_val) / float(1023)
  volts = round(volts,places)
  return volts

# get temerature
# returns None on error, or the temperature as a float
def get_temp(devicefile):

    try:
        fileobj = open(devicefile,'r')
        lines = fileobj.readlines()
        fileobj.close()
    except:
        return None

    # get the status from the end of line 1 
    status = lines[0][-4:-1]

    # is the status is ok, get the temperature from line 2
    if status=="YES":
        #print status
        tempstr= lines[1][-6:-1]
        tempvalue=float(tempstr)/1000
        #print tempvalue
        return tempvalue
    else:
        print "There was an error with the temperature sensor."
        return None

# store sensor data in the database
def log_data(temp, water, smoke, test, nodeID):

    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    curs.execute("INSERT INTO table_sensory_data values(datetime('now', 'localtime'), (?), (?), (?), (?), (?), (?), (?))", (temp, water, smoke, test, 0, 0, nodeID))

    # commit the changes
    conn.commit()

    conn.close()

# get current polling_rate value from DB
def get_polling_rate():
    polling_rate = 0
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    curs.execute("SELECT polling_rate FROM table_node_configuration limit 1")
    rows=curs.fetchall()
    for row in rows:
      polling_rate = int(row[0])

    conn.close()
    return polling_rate

# get current polling_rate value from DB
def get_nodeID():
    nodeID = 0
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    curs.execute("SELECT nodeID FROM table_node_configuration limit 1")
    rows=curs.fetchall()
    for row in rows:
      nodeID = int(row[0])

    conn.close()
    return nodeID


# Define sensor channels
water_channel = 0
smoke_channel = 1
test_channel = 2
 
# Define delay between readings in seconds
delay = 5


# enable kernel modules
os.system('sudo modprobe w1-gpio')
os.system('sudo modprobe w1-therm')

# search for a device file that starts with 28
devicelist = glob.glob('/sys/bus/w1/devices/28*')
if devicelist=='':
	print("Error: Temp sensor malfunction")
else:
	# append /w1slave to the device file
	w1devicefile = devicelist[0] + '/w1_slave'

while True:
 
  # Read the water sensor data
  # Water 
  water_level = ReadChannel(water_channel)
  water_volts = ConvertVolts(water_level,2,vref_val)
  # Smoke
  smoke_level = ReadChannel(smoke_channel)
  smoke_volts = ConvertVolts(smoke_level,2,vref_val)
  # Test 
  test_level = ReadChannel(test_channel)
  test_volts = ConvertVolts(test_level,2,vref_val)
  
##  # Print out results
##  print "--------------------------------------------"
##  print("Water Sensor Voltage: {} ({}V)".format(water_level,water_volts))
##  print("Smoke Sensor Voltage: {} ({}V)".format(smoke_level,smoke_volts))
##  print("Test Voltage (3.3/2): {} ({}V)".format(test_level,test_volts))
 
  # get the temperature from the device file
  temperature = get_temp(w1devicefile)
  if temperature != None:
##  	print "Temperature: " + str(temperature) + " deg. C"
 	log_data(temperature, water_volts, smoke_volts, test_volts, get_nodeID())
  # Wait before repeating loop
  delay = get_polling_rate()
  time.sleep(delay)
