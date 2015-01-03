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

    curs.execute("SELECT t1.rowid, t1.timestamp, t1.nodeID, t1.sensor_type, t1.sensor_val, t1.th_sensor, t1.email, t1.sentflag, t2.nodeID FROM table_notifications t1, table_node_configuration t2 where t1.nodeID=t2.nodeId order by timestamp desc limit 10")
    rows=curs.fetchall()
    
    conn.close()

    return rows

# print the data table
def print_data_table(records):

    print """<form action="/cgi-bin/viewnotifications.py" method="POST">"""
    print """<h2>Last 10 Notifications</h2><br>"""

    print"""
    <table>
    <tr style="color:White;background-color:#000084;font-weight:bold;">
    <th>Item</th>
    <th>Timestamp</th>
    <th>nodeID</th>
    <th>Sensor Type</th>
    <th>Sensor value</th>
    <th>Sensor Threshold</th>
    <th>E-mail Address</th>
    <th>Status</th>
    </tr>"""
    i=0
    stylex=""
    for row in records:
        i=i+1
        if i%2 == 0:
                stylex = """<tr style="color:Black;background-color:#EEEEEE;"><td>"""
        else:
                stylex = """<tr style="color:Black;background-color:Gainsboro;"><td>"""
        print stylex + str(row[0]) + "</td>"
        print "<td>" + str(row[1]) + "</td>"
        print "<td>" + str(row[2]) + "</td>"
        print "<td>" + str(row[3]) + "</td>"
        print "<td>" + str(row[4]) + "</td>"
        print "<td>" + str(row[5]) + "</td>"
        print "<td>" + str(row[6]) + "</td>"
        print "<td>" + str(row[7]) + "</td></tr>"
    print """</table><input type="submit" value="Back" name="Back"></form>"""
    
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
    print "R.E.D.M.A. Notifications Page"
    print "    </title>"
    print """<style>
        table, th, td {
            border: 1px solid black;
            border-collapse: collapse;
        }
        h2 {
           color:#000084;
        }
        th, td {
            padding: 5px;
            text-align: left;
        }"""
    print """</style>"""
    print "</head>"
    
    # print the page body
    print "<body>"
    #print "<h1>R.E.D.M.A. Notifications Page</h1>"
    print """<img src="../redma_top.jpg" alt="REDMA" height="10%" width="20%">"""
    print "<hr>"
    print_data_table(records)
    print "</body>"
    print "</html>"

    sys.stdout.flush()

if __name__=="__main__":
    main()

