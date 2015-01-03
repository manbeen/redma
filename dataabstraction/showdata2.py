#!/usr/bin/env python

import sqlite3
import sys
import cgi
import cgitb


# global variables
dbname='/home/pi/nodedb.db'

# print the HTTP header
def printHTTPheader(send_back):
    if send_back == 0:
        print "Content-type: text/html\n\n"
    else:
        print "Location: ../\r\n"

# print the HTML head section
# arguments are the page title and the table for the chart
def printHTMLHead(title, table, option2):
    print "<head>"
    print "    <title>"
    print title
    print "    </title>"
    print """<style>
        h2 {
           color:#000084;
        }"""
    print "</style>"
    
    print_graph_script(table, option2)

    print "</head>"

# get data from the database
# if an interval is passed, 
# return a list of records from the database
def get_data(interval, option2):

    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    x = int(option2)
    if x == 4: #temperature
        whichone = "sensor1" #temperature
    elif x == 3: #test
        whichone = "sensor4" #test
    elif x == 2: #water
        whichone = "sensor2" #water
    else: #x == 1 smoke
        whichone = "sensor3" #smoke

    if interval == None:
        curs.execute("SELECT timestamp, " + whichone + " FROM table_sensory_data")
    else:
        curs.execute("SELECT timestamp, " + whichone + " FROM table_sensory_data WHERE timestamp>datetime('now','localtime','-%s hours')" % interval)

    rows=curs.fetchall()

    conn.close()

    return rows


# convert rows from database into a javascript table
def create_table(rows):
    chart_table=""

    for row in rows[:-1]:
        rowstr="['{0}', {1}],\n".format(str(row[0]),str(row[1]))
        chart_table+=rowstr

    row=rows[-1]
    rowstr="['{0}', {1}]\n".format(str(row[0]),str(row[1]))
    chart_table+=rowstr

    return chart_table


# print the javascript to generate the chart
# pass the table generated from the database info
def print_graph_script(table, option2):

    x = int(option2)

    if x == 1:
        # google chart snippet
        chart_code="""
        <script type="text/javascript" src="https://www.google.com/jsapi"></script>
        <script type="text/javascript">
          google.load("visualization", "1", {packages:["corechart"]});
          google.setOnLoadCallback(drawChart);
          function drawChart() {
            var data = google.visualization.arrayToDataTable([['Time', 'Smoke'], %s]);
            var options = {title: 'Smoke'};
            var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
            chart.draw(data, options);
          }
        </script>"""
    elif x == 2:
        # google chart snippet
        chart_code="""
        <script type="text/javascript" src="https://www.google.com/jsapi"></script>
        <script type="text/javascript">
          google.load("visualization", "1", {packages:["corechart"]});
          google.setOnLoadCallback(drawChart);
          function drawChart() {
            var data = google.visualization.arrayToDataTable([['Time', 'Water'], %s]);
            var options = {title: 'Water'};
            var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
            chart.draw(data, options);
          }
        </script>"""
    elif x == 3:
        # google chart snippet
        chart_code="""
        <script type="text/javascript" src="https://www.google.com/jsapi"></script>
        <script type="text/javascript">
          google.load("visualization", "1", {packages:["corechart"]});
          google.setOnLoadCallback(drawChart);
          function drawChart() {
            var data = google.visualization.arrayToDataTable([['Time', 'Test'], %s]);
            var options = {title: 'Test'};
            var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
            chart.draw(data, options);
          }
        </script>"""
    else:
        # google chart snippet
        chart_code="""
        <script type="text/javascript" src="https://www.google.com/jsapi"></script>
        <script type="text/javascript">
          google.load("visualization", "1", {packages:["corechart"]});
          google.setOnLoadCallback(drawChart);
          function drawChart() {
            var data = google.visualization.arrayToDataTable([['Time', 'Temperature'], %s]);
            var options = {title: 'Temperature'};
            var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
            chart.draw(data, options);
          }
        </script>"""
    print chart_code % (table)




# print the div that contains the graph
def show_graph(option2):
    x = int(option2)
    if x == 1:
        print """<table><tr><td><img src="../cartoon_fire.gif" alt="Smoke" height="35" width="50"></td><td valign="middle"><b><font size="6" color="#000084">Smoke Sensor Chart</b></font></td></tr></table>"""
    elif x == 2:
        print """<table><tr><td><img src="../flooded-house.png" alt="Fire" height="50" width="50"></td><td valign="middle"><b><font size="6" color="#000084">Water Sensor Chart</b></font></td></tr><table>"""
    elif x == 3:
        print "<h2>Test Sensor Chart</h2>"
    else: #x == 4
        print """<table><tr><td><img src="../Earth_w_fever.jpg" alt="Temperature" height="50" width="50"></td><td valig="middle"><b><font size="6" color="#000084">Temperature Sensor Chart</b></font></td></tr></table>"""
        
    print '<div id="chart_div" style="width: 900px; height: 500px;"></div>'



def print_time_selector(option, option2):

    print """<form action="/cgi-bin/showdata2.py" method="POST">
        Show logs for  
        <select name="timeinterval">"""


    if option is not None:

        if option == "0.5":
            print "<option value=\"0.5\" selected=\"selected\">the last 30 minutes</option>"
        else:
            print "<option value=\"0.5\">the last 30 minutes</option>"

        if option == "6":
            print "<option value=\"6\" selected=\"selected\">the last 6 hours</option>"
        else:
            print "<option value=\"6\">the last 6 hours</option>"

        if option == "24":
            print "<option value=\"24\" selected=\"selected\">the last 24 hours</option>"
        else:
            print "<option value=\"24\">the last 24 hours</option>"

        if option == "48":
            print "<option value=\"48\" selected=\"selected\">the last 48 hours</option>"
        else:
            print "<option value=\"48\">the last 48 hours</option>"

    else:
        print """<option value="0.5">the last 30 minutes</option>
            <option value="6">the last 6 hours</option>
            <option value="24">the last 24 hours</option>
            <option value="48" selected="selected">the last 48 hours</option>"""

    print """        </select>
        Select a type of sensor  
        <select name="whichsensor">"""


    if option2 is not None:

        if option2 == "1":
            print "<option value=\"1\" selected=\"selected\">Smoke</option>"
        else:
            print "<option value=\"1\">Smoke</option>"

        if option2 == "2":
            print "<option value=\"2\" selected=\"selected\">Water</option>"
        else:
            print "<option value=\"2\">Water</option>"

        if option2 == "3":
            print "<option value=\"3\" selected=\"selected\">Test</option>"
        else:
            print "<option value=\"3\">Test</option>"

        if option2 == "4":
            print "<option value=\"4\" selected=\"selected\">Temperature</option>"
        else:
            print "<option value=\"4\">Temperature</option>"

    else:
        print """<option value="1">Smoke</option>
            <option value="2">Water</option>
            <option value="3">Test</option>
            <option value="4" selected="selected">Temperature</option>"""

    print """        </select>
        <input type="submit" value="Display" name="Display"><input type="submit" value="Back" name="Back">
    </form>"""


# main function
# This is where the program starts 
def main():

    cgitb.enable()
    send_back = 0

    # get options that may have been passed to this script
    form=cgi.FieldStorage()
    if "timeinterval" in form:
	option = form["timeinterval"].value
    else:
	option = str(0.5)
    
    if "whichsensor" in form:
	option2 = form["whichsensor"].value
    else:
	option2 = str(4)

    if "Back" in form:
        send_back = 1
    else:
        send_back = 0

    # get data from the database
    records=get_data(option, option2)

    # print the HTTP header
    printHTTPheader(send_back)

    if len(records) != 0:
        # convert the data into a table
        table=create_table(records)
    else:
        print "No data found"
        return

    # start printing the page
    print "<html>"
    # print the head section including the table
    # used by the javascript for the chart
    printHTMLHead("R.E.D.M.A. Sensor Data Viewer", table, option2)

    # print the page body
    print "<body>"
    #print "<h1>R.E.D.M.A. Sensor Data Viewer</h1>"
    print """<img src="../redma_top.jpg" alt="REDMA" height="10%" width="20%">"""
    print "<hr>"
    print_time_selector(option, option2)
    show_graph(option2)
    print "</body>"
    print "</html>"

    sys.stdout.flush()

if __name__=="__main__":
    main()




