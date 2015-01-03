#!/usr/bin/env python

import sqlite3
import sys
import cgi
import cgitb


# global variables
dbname='/home/pi/nodedb.db'

# print the HTTP header
def printHTTPheader(option):
	if option == 0:
		print "Content-type: text/html\n\n"
	else:
		print "Location: ../\r\n"

# get data from the database
def get_data():

    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    curs.execute("SELECT t1.sensor1,t1.sensor3,t1.sensor2,t1.timestamp,(t1.sensor1-t2.th_sensor1) as sensor1th, (t1.sensor3-t2.th_sensor3) as sensorth3, (t1.sensor2-t2.th_sensor2) as sensor2th FROM table_sensory_data t1, table_node_configuration t2 WHERE t1.nodeID=t2.nodeID ORDER BY timestamp DESC LIMIT 1")
    rows=curs.fetchall()
    
    conn.close()

    return rows

# print the data table
def print_data_table(records):

    print """<form action="/cgi-bin/dashboard.py" method="POST">"""
    print "<table>"
    for row in records:
        if float(row[4]) > 0.0:
                print """<tr><td align="center"><img src="../Earth_w_fever.jpg" alt="Temperature" height="100" width="100"></td><td align="right"><b>Temperature:</b></td><td align="left"><font color="#FF0000">""" + str(row[0]) + " deg. Celsius<font></td></tr>"
        else:
                print """<tr><td align="center"><img src="../Earth_w_fever.jpg" alt="Temperature" height="100" width="100"></td><td align="right"><b>Temperature:</b></td><td align="left"><font color="#00FF00">""" + str(row[0]) + " deg. Celsius<font></td></tr>"
        if float(row[5]) > 0.0:                
                print """<tr><td align="center"><img src="../cartoon_fire.gif" alt="Smoke" height="100" width="100"></td><td align="right"><b>Smoke:</b></td><td align="left"><font color="#FF0000">""" + str(row[1]) + " volts</font></td></tr>"
        else:
                print """<tr><td align="center"><img src="../cartoon_fire.gif" alt="Smoke" height="100" width="100"></td><td align="right"><b>Smoke:</b></td><td align="left"><font color="#00FF00">""" + str(row[1]) + " volts</font></td></tr>"
        if float(row[6]) > 0.0:
                print """<tr><td align="center"><img src="../flooded-house.png" alt="Fire" height="100" width="100"></td><td align="right"><b>Water:</b></td><td align="left"><font color="#FF0000">""" + str(row[2]) + " volts</font></td></tr>"
        else:
                print """<tr><td align="center"><img src="../flooded-house.png" alt="Fire" height="100" width="100"></td><td align="right"><b>Water:</b></td><td align="left"><font color="#00FF00">""" + str(row[2]) + " volts</font></td></tr>"
        print """<tr><td align="center"><img src="../lastupdate.jpeg" alt="Fire" height="100" width="100"></td><td align="right"><b>Last Updated:</b></td><td align="left">""" + str(row[3]) + "</td></tr>"
        print """</table><input type="submit" value="Back" name="Back"><input type="submit" value="Refresh" name="Refresh"></form>"""
    
# main function
# This is where the program starts 
def main():
    option = 0
    cgitb.enable()
    # get options that may have been passed to this script
    form=cgi.FieldStorage()
    if "Back" in form:
    	option = 1
    else:
    	option = 0 
    # get data from the database
    records = get_data()

    # print the HTTP header
    printHTTPheader(option)

    if len(records) == 0:
        print "No data found"
        return

    # start printing the page
    print "<html>"
    print "<head>"
    print "    <title>"
    print "R.E.D.M.A. Dashboard"
    print "    </title>"
    print """<style>
        table, th, td {
            border-collapse: collapse;
        }
        th, td {
            padding: 5px;
            text-align: left;
        }"""
    print """</style>"""
    print "</head>"
    
    # print the page body
    print "<body>"
    print """<img src="../redma_top.jpg" alt="REDMA" height="15%" width="25%">"""
    print_data_table(records)
    print "</body>"
    print "</html>"

    sys.stdout.flush()

if __name__=="__main__":
    main()

