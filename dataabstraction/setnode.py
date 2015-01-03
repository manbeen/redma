#!/usr/bin/env python

import sqlite3
import sys
import cgi
import cgitb


# global variables
dbname='/home/pi/nodedb.db'

html_escape_table = {"&": "&amp;",'"': "&quot;","'": "&apos;",">": "&gt;","<": "&lt;"}

def html_escape(text):
    """Produce entities within text."""
    return "".join(html_escape_table.get(c,c) for c in text)

# print the HTTP header
def printHTTPheader(send_back):
    if send_back == 0:
        print "Content-type: text/html\n\n"
    else:
        print "Location: ../\r\n"

# get data from the database
def get_data():

    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    #order of sensors: 1:temperature, 2:water, 3:smoke, 4:test, 5:na, 6:na
    curs.execute("SELECT nodeID, location, polling_rate, th_sensor1, th_sensor2, th_sensor3, th_sensor4, th_sensor5, th_sensor6, email FROM table_node_configuration")
    rows=curs.fetchall()
    
    conn.close()

    return rows

# print the data table
def print_data_table(records):

    print """<form action="/cgi-bin/setnode.py" method="POST">"""
    print """<h2>Node Configuration Data</h2><br>"""

    print"""
    <table>
    <tr style="color:White;background-color:#000084;font-weight:bold;">
    <th>Parameter</th>
    <th>Value</th>
    </tr>"""
    for row in records:
        print "<tr style=\"color:Black;background-color:#EEEEEE;\"><td>NodeID</td><td>" + str(row[0]) + "</td></tr>"
        print "<tr style=\"color:Black;background-color:Gainsboro;\"><td>Location</td><td>" + str(row[1]) + "</td></tr>"
        print "<tr style=\"color:Black;background-color:#EEEEEE;\"><td>Polling Rate</td><td>" + str(row[2]) + " seconds</td></tr>"
        print "<tr style=\"color:Black;background-color:Gainsboro;\"><td>Temperature Sensor Threshold</td><td>" + str(row[3]) + " deg. Celsius</td></tr>"
        print "<tr style=\"color:Black;background-color:#EEEEEE;\"><td>Water Sensor Threshold</td><td>" + str(row[4]) + " volts</td></tr>"
        print "<tr style=\"color:Black;background-color:Gainsboro;\"><td>Smoke Sensor Threshold</td><td>" + str(row[5]) + " volts</td></tr>"
        print "<tr style=\"color:Black;background-color:#EEEEEE;\"><td>Test Sensor Threshold</td><td>" + str(row[6]) + " volts</td></tr>"
        print "<tr style=\"color:Black;background-color:Gainsboro;\"><td>TBD Sensor Threshold</td><td>" + str(row[7]) + "</td></tr>"
        print "<tr style=\"color:Black;background-color:#EEEEEE;\"><td>TBD Sensor Threshold</td><td>" + str(row[8]) + "</td></tr>"
        print "<tr style=\"color:Black;background-color:Gainsboro;\"><td>Administrator's notification e-mail address</td><td>" + str(row[9]) + "</td></tr>"
        
    print """</table><input type="submit" value="Edit" name="Edit"><input type="submit" value="Back" name="Back"></form>"""

# print an editable configuration data table
def edit_data(send_error_msg):
    print """<form action="/cgi-bin/setnode.py" method="POST">"""
    if send_error_msg == 1:
        print """<h2>Invalid NodeID</h2>"""
    elif send_error_msg == 2:
        print """<h2>Invalid Location</h2>"""
    elif send_error_msg == 3:
        print """<h2>Polling rate out of bounds</h2>"""
    elif send_error_msg == 4:
        print """<h2>Temperature sensor threshold out of bounds</h2>"""
    elif send_error_msg == 5:
        print """<h2>Water sensor threshold out of bounds</h2>"""
    elif send_error_msg == 6:
        print """<h2>Smoke sensor threshold out of bounds</h2>"""
    elif send_error_msg == 7:
        print """<h2>Test sensor threshold out of bounds</h2>"""
    elif send_error_msg == 8:
        print """<h2>TBD sensor threshold out of bounds</h2>"""
    elif send_error_msg == 9:
        print """<h2>TBD sensor threshold out of bounds</h2>"""
    elif send_error_msg == 10:
        print """<h2>Invalid notification e-mail address</h2>"""
    else:
        print """<h2>Edit Configuration Data</h2><br>"""
    print"""
    <table>
    <tr style="color:White;background-color:#000084;font-weight:bold;">
    <th>Parameter</th>
    <th>Value</th>
    </tr>"""

    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    curs.execute("SELECT nodeID, location, polling_rate, th_sensor1, th_sensor2, th_sensor3, th_sensor4, th_sensor5, th_sensor6, email FROM table_node_configuration")
    rows=curs.fetchall()

    for row in rows:
        nodeID = int(row[0])
        print "<tr style=\"color:Black;background-color:#EEEEEE;\"><td>NodeID</td><td><select name=\"nodeID\">"
        if nodeID == 1:
            print "<option value=\"1\" selected=\"selected\">Node 1</option>"
        else:
            print "<option value=\"1\">Node 1</option>"
        if nodeID == 2:
            print "<option value=\"2\" selected=\"selected\">Node 2</option>"
        else:
            print "<option value=\"2\">Node 2</option>"
        if nodeID == 3:
            print "<option value=\"3\" selected=\"selected\">Node 3</option>"
        else:
            print "<option value=\"3\">Node 3</option>"
        if nodeID == 4:
            print "<option value=\"4\" selected=\"selected\">Node 4</option>"
        else:
            print "<option value=\"4\">Node 4</option>"
        print "</select></td></tr>"
        print "<tr style=\"color:Black;background-color:Gainsboro;\"><td>Location</td><td><input type=\"text\" size=\"60\" value=\"" + html_escape(str(row[1])) + "\" name=\"location\"></td></tr>"
        polling_rate = int(row[2])
        print "<tr style=\"color:Black;background-color:#EEEEEE;\"><td>Polling Rate</td><td><select name=\"polling_rate\">"
        if polling_rate == 5:
            print "<option value=\"5\" selected=\"selected\">5 seconds</option>"
        else:
            print "<option value=\"5\">5 seconds</option>"
        if polling_rate == 60:
            print "<option value=\"60\" selected=\"selected\">60 seconds</option>"
        else:
            print "<option value=\"60\">60 seconds</option>"
        if polling_rate == 300:
            print "<option value=\"300\" selected=\"selected\">300 seconds</option>"
        else:
            print "<option value=\"300\">300 seconds</option>"
        if polling_rate == 600:
            print "<option value=\"600\" selected=\"selected\">600 seconds</option>"
        else:
            print "<option value=\"600\">600 seconds</option>"
        print "</select></td></tr>"
        print "<tr style=\"color:Black;background-color:Gainsboro;\"><td>Temperature Sensor Threshold</td><td><input type=\"text\" size=\"10\" value=\"" + html_escape(str(row[3])) + "\" name=\"th_sensor1\"> deg. Celsius [Range 0.0-50.0 deg.C]</td></tr>"
        print "<tr style=\"color:Black;background-color:#EEEEEE;\"><td>Water Sensor Threshold</td><td><input type=\"text\" size=\"10\" value=\"" + html_escape(str(row[4])) + "\" name=\"th_sensor2\"> Volts [Range 0.1 - 3.3V]</td></tr>"
        print "<tr style=\"color:Black;background-color:Gainsboro;\"><td>Somke Sensor Threshold</td><td><input type=\"text\" size=\"10\" value=\"" + html_escape(str(row[5])) + "\" name=\"th_sensor3\"> Volts [Range 0.1 - 3.3V]</td></tr>"
        print "<tr style=\"color:Black;background-color:#EEEEEE;\"><td>Test Sensor Threshold</td><td><input type=\"text\" size=\"10\" value=\"" + html_escape(str(row[6])) + "\" name=\"th_sensor4\"> Volts [Range 1.64 - 1.66V]</td></tr>"
        print "<tr style=\"color:Black;background-color:Gainsboro;\"><td>TBD Sensor Threshold</td><td><input type=\"text\" size=\"10\" value=\"" + html_escape(str(row[7])) + "\" name=\"th_sensor5\"> Volts [Range 0.1 - 3.3V] </td></tr>"
        print "<tr style=\"color:Black;background-color:#EEEEEE;\"><td>TBD Sensor Threshold</td><td><input type=\"text\" size=\"10\" value=\"" + html_escape(str(row[8])) + "\" name=\"th_sensor6\"> Volts [Range 0.1 - 3.3V]</td></tr>"
        print "<tr style=\"color:Black;background-color:Gainsboro;\"><td>Administrator's notification e-mail address</td><td><input type=\"text\" size=\"20\" value=\"" + html_escape(str(row[9])) + "\" name=\"email\"></td></tr>"
        
    print """</table><input type="submit" value="Update" name="Update"><input type="submit" value="Back" name="Back"></form>"""

# store updated configuration data in the database
def update_data(nodeID, location, polling_rate, th_sensor1, th_sensor2, th_sensor3, th_sensor4, th_sensor5, th_sensor6, email):
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    query = "UPDATE table_node_configuration SET nodeID=?, location=?, polling_rate=?, th_sensor1=?, th_sensor2=?"
    query = query + ", th_sensor3=?, th_sensor4=?, th_sensor5=?, th_sensor6=?, email=?"
    curs.execute(query, (nodeID, location, polling_rate, th_sensor1, th_sensor2, th_sensor3, th_sensor4, th_sensor5, th_sensor6, email))
    # commit the changes
    conn.commit()    
    conn.close()

# check if a string is number
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    
    return False
    
# main function
# This is where the program starts 
def main():

    cgitb.enable()
    send_error_msg = 0
    showedit = 0
    send_back = 0
    nodeID = 0
    location = ""
    polling_rate = 0
    th_sensor1 = 0.0
    th_sensor2 = 0.0
    th_sensor3 = 0.0
    th_sensor4 = 0.0
    th_sensor5 = 0.0
    th_sensor6 = 0.0
    email = ""
    # get options that may have been passed to this script
    form=cgi.FieldStorage()
    if "Edit" in form:
        #edit request by user
        showedit = 1
    elif "Update" in form:
        if "nodeID" in form:
            nodeID = int(form["nodeID"].value)
        else:
            nodeID = 0
        if "location" in form:
            location = form["location"].value
        else:
            location = ""
        if "polling_rate" in form:
            polling_rate = int(form["polling_rate"].value)
        else:
            polling_rate = 0
        if "th_sensor1" in form:
            th_sensor1 = str(form["th_sensor1"].value)
            if not(is_number(th_sensor1)):
                th_sensor1 = -100.0
            else:
                th_sensor1 = round(float(th_sensor1),2)
        else:
            th_sensor1 = -100.0
        if "th_sensor2" in form:
            th_sensor2 = str(form["th_sensor2"].value)
            if not(is_number(th_sensor2)):
                th_sensor2 = -1.0
            else:
                th_sensor2 = round(float(th_sensor2),2)
        else:
            th_sensor2 = -1.0
        if "th_sensor3" in form:
            th_sensor3 = str(form["th_sensor3"].value)
            if not(is_number(th_sensor3)):
                th_sensor3 = -1.0
            else:
                th_sensor3 = round(float(th_sensor3),2)
        else:
            th_sensor3 = -1.0
        if "th_sensor4" in form:
            th_sensor4 = str(form["th_sensor4"].value)
            if not(is_number(th_sensor4)):
                th_sensor4 = -1.0
            else:
                th_sensor4 = round(float(th_sensor4),2)
        else:
            th_sensor4 = -1.0
        if "th_sensor5" in form:
            th_sensor5 = str(form["th_sensor5"].value)
            if not(is_number(th_sensor5)):
                th_sensor5 = -1.0
            else:
                th_sensor5 = round(float(th_sensor5),2)
        else:
            th_sensor5 = -1.0
        if "th_sensor6" in form:
            th_sensor6 = str(form["th_sensor6"].value)
            if not(is_number(th_sensor6)):
                th_sensor6 = -1.0
            else:
                th_sensor6 = round(float(th_sensor6),2)
        else:
            th_sensor6 = -1.0
        if "email" in form:
            email = form["email"].value
        else:
            email = ""
        if nodeID <= 0:
            send_error_msg = 1 #invalid nodeID
        elif nodeID > 4:
            send_error_msg = 1 #invalid nodeID
        if len(location) == 0:
            send_error_msg = 2 #invalid location
        elif len(location) > 255:
            send_error_msg = 2 #invalid location
        if polling_rate != 5 and polling_rate != 60 and polling_rate != 300 and polling_rate != 600:
            send_error_msg = 3 #invalid polling_rate
        if th_sensor1 < 0.0 or th_sensor1 > 50.0:
            send_error_msg = 4 #temperature threshold out of bounds
        if th_sensor2 < 0.1 or th_sensor2 > 3.3:
            send_error_msg = 5 #water threshold out of bounds
        if th_sensor3 < 0.1 or th_sensor3 > 3.3:
            send_error_msg = 6 #smoke threshold out of bounds
        if th_sensor4 < 1.64 or th_sensor4 > 1.66:
            send_error_msg = 7 #test threshold out of bounds
        if th_sensor5 < 0.0 or th_sensor5 > 3.3:
            send_error_msg = 8 #TBD threshold out of bounds
        if th_sensor6 < 0:
            send_error_msg = 9 #TBD threshold out of bounds
        elif th_sensor6 > 3.3:
            send_error_msg = 9 #TBD threshold out of bounds
        if len(email) == 0:
            send_error_msg = 10 #invalid email
        elif len(email) > 255:
            send_error_msg = 10 #invalid location
        if send_error_msg == 0:
            update_data(nodeID, location, polling_rate, th_sensor1, th_sensor2, th_sensor3, th_sensor4, th_sensor5, th_sensor6, email)
            showedit = 0
        else:
            showedit = 1
    elif "Back" in form:
        send_back = 1
    else:
        showedit = 0
        send_back = 0

    # get data from the database
    records=get_data()

    # print the HTTP header
    printHTTPheader(send_back)

    if len(records) == 0:
        print "No data found"
        return

    # start printing the page
    print "<html>"
    print "<head>"
    print "    <title>"
    print "R.E.D.M.A. Node Configuration Page"
    print "    </title>"
    print """<style>
        table, th, td {
            border: 1px solid black;
            border-collapse: collapse;
        }
        th, td {
            padding: 5px;
            text-align: left;
        }"""
    #Change color of h2 when there is an error message to be displayed
    if send_error_msg != 0:
        print """h2   {color:red}"""
    else:
        print """h2   {color:#000084}"""
    print """</style>"""
    print "</head>"
    
    # print the page body
    print "<body>"
    #print "<h1>R.E.D.M.A. Node Configuration Page</h1>"
    print """<img src="../redma_top.jpg" alt="REDMA" height="10%" width="20%">"""
    print "<hr>"
    if showedit == 0:
        print_data_table(records)
    else: #showedit == 1
        edit_data(send_error_msg)
        
    print "</body>"
    print "</html>"

    sys.stdout.flush()

if __name__=="__main__":
    main()

