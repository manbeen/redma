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

    curs.execute("SELECT rowid, subscriberID, description, email FROM table_subscriber")
    rows=curs.fetchall()
    
    conn.close()

    return rows

# print the data table
def print_data_table(records, send_error_msg):

    print """<form action="/cgi-bin/setconfig.py" method="POST">"""
    if send_error_msg == 4:
        print """<h2>Cannot delete all subscribers</h2><br>"""
    else:
        print """<h2>Subscriber Configuration Data</h2><br>"""

    print"""
    <table>
    <tr style="color:White;background-color:#000084;font-weight:bold;">
    <th>Item</th>
    <th>SubscriberID</th>
    <th>Description</th>
    <th>E-mail address</th>
    <th>Edit</th>
    <th>Delete</th>
    </tr>"""
    i=0
    for row in records:
        i=i+1
        if i%2 == 0:
            print "<tr style=\"color:Black;background-color:#EEEEEE;\">"
        else:
            print "<tr style=\"color:Black;background-color:Gainsboro;\">"
        print "<td>"""+str(row[0])+"""</td>
        <td>"""+str(row[1])+"""</td>
        <td>"""+str(row[2])+"""</td>
        <td>"""+str(row[3])+"""</td>
        <td><input type="submit" value=""" + str(row[0]) + """ name="Edit""" + str(i) +""""</td>
        <td><input type="submit" value=""" + str(row[0]) + """ name="Delete""" + str(i) +""""></td></tr>"""        
        
    print """</table><input type="submit" value="Add" name="Add"><input type="submit" value="Back" name="Back"></form>"""

def print_add_data_table(send_error_msg):
    if send_error_msg == 1:
        print """<h2>Invalid SubscriberID</h2>"""
    elif send_error_msg == 2:
        print """<h2>Invalid Description</h2>"""
    elif send_error_msg == 3:
        print """<h2>SubscriberID must be unique</h2>"""
    elif send_error_msg == 5:
        print """<h2>Maximum of 4 subscribers per node</h2>"""
    elif send_error_msg == 6:
        print """<h2>Invalid E-mail Address</h2>"""
    else:
        print """<h2>Add a New Subscriber</h2><br>"""

    print """<form action="/cgi-bin/setconfig.py" method="POST">    
    <table>
    <tr style="color:White;background-color:#000084;font-weight:bold;">
    <th>SubscriberID</th>
    <th>Description</th>
    <th>E-mail Address</th>
    </tr>
    <tr style=\"color:Black;background-color:#EEEEEE;\">
    <td><input type="text" value="" name="subscriberID"></td>
    <td><input type="text" value="" name="description"></td>
    <td><input type="text" value="" name="email"></td></tr></table>"""
    
    print """<input type="submit" name="AddNewSubscriber" value="Add New Subscriber"><input type="submit" value="Back" name="Back"></form>"""

# store new subscriber in the database
def add_data(subscriberID, description, email):
    x = 1
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    query="SELECT * FROM table_subscriber WHERE subscriberID=\"" + subscriberID + "\""
    curs.execute(query)
    rows=curs.fetchall()
    if len(rows) == 0:
        query="SELECT * FROM table_subscriber"
        curs.execute(query)
        rows=curs.fetchall()
        if len(rows) <= 3:
            curs.execute("INSERT INTO table_subscriber VALUES((?), (?), (?))", (subscriberID,description,email))
            # commit the changes
            conn.commit()
            conn.close()
            x = 0
        else:
            x = 2 # max. of 4 subscribers per node
    else:
        conn.close()
        x = 1; # cannot add duplicate subscriber

    return x

# store new subscriber in the database
def del_data(rowID):
    x = 1
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    query="SELECT * FROM table_subscriber"
    curs.execute(query)
    rows=curs.fetchall()
    if len(rows) >= 2:
        curs.execute("DELETE FROM table_subscriber WHERE rowid="+str(rowID))

        # commit the changes
        conn.commit()
        x = 0
    else:
        x = 1

    conn.close()
    return x

# print the data table
def edit_data(rowID, send_error_msg):
    print """<form action="/cgi-bin/setconfig.py" method="POST">"""
    if send_error_msg == 1:
        print """<h2>Invalid SubscriberID</h2>"""
    elif send_error_msg == 2:
        print """<h2>Invalid Description</h2>"""
    elif send_error_msg == 3:
        print """<h2>SubscriberID must be unique</h2>"""
    elif send_error_msg == 6:
        print """<h2>Invalid E-mail Address</h2>"""
    else:
        print """<h2>Edit Configuration Data</h2><br>"""
    print"""
    <table>
    <tr style="color:White;background-color:#000084;font-weight:bold;">
    <th>Item</th>
    <th>SubscriberID</th>
    <th>Description</th>
    <th>E-mail Address</th>
    </tr>"""

    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    curs.execute("SELECT rowid, subscriberID, description, email FROM table_subscriber WHERE rowid="+str(rowID))
    rows=curs.fetchall()

    for row in rows:
        print "<tr style=\"color:Black;background-color:#EEEEEE;\">"
        print "<td>"+str(row[0])+"</td>"
        print "<input type=\"hidden\" value=\"" + str(row[0]) + "\" name=\"rowID\">"
        print "<td><input type=\"text\" size=\"40\" value=\"" + html_escape(str(row[1])) + "\" name=\"subscriberID\"></td>"
        print "<td><input type=\"text\" size=\"60\" value=\"" + html_escape(str(row[2])) + "\" name=\"description\"></td>"
        print "<td><input type=\"text\" size=\"60\" value=\"" + html_escape(str(row[3])) + "\" name=\"email\"></td></tr>"        
        
    print """</table><input type="submit" value="Update" name="Update"><input type="submit" value="Back" name="Back"></form>"""

# store new subscriber in the database
def update_data(rowID, subscriberID, description,email):
    x = 1
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    query="SELECT * FROM table_subscriber WHERE subscriberID=\"" + subscriberID + "\" AND rowID !=" + rowID
    curs.execute(query)
    rows=curs.fetchall()
    if len(rows) == 0:
        query = "UPDATE table_subscriber SET subscriberID=?, description=?, email=? WHERE rowID=?"
        curs.execute(query,(subscriberID,description,email,rowID))
        # commit the changes
        conn.commit()    
        x = 0
    else:
        x = 1; # cannot add duplicate subscriber

    conn.close()
    return x

# main function
# This is where the program starts 
def main():

    cgitb.enable()

    # get options that may have been passed to this script
    form=cgi.FieldStorage()
    send_error_msg = 0 #all good
    rowID = 0
    send_back = 0
    x = 0
    if "Delete1" in form:
	#delete row 1
        rowID = form["Delete1"].value
        x = del_data(rowID)
        if x == 0:
            send_error_msg = 0
        else:
            send_error_msg = 4 #can't delete last remaining row in table
        showadd = 0
    elif "Delete2" in form:
        #delete row 2
        rowID = form["Delete2"].value
        x = del_data(rowID)
        if x == 0:
            send_error_msg = 0
        else:
            send_error_msg = 4 #can't delete last remaining row in table
        showadd = 0
    elif "Delete3" in form:
        #delete row 3
        rowID = form["Delete3"].value
        x = del_data(rowID)
        if x == 0:
            send_error_msg = 0
        else:
            send_error_msg = 4 #can't delete last remaining row in table
        showadd = 0
    elif "Delete4" in form:
        #delete row 4
        rowID = form["Delete4"].value
        x = del_data(rowID)
        if x == 0:
            send_error_msg = 0
        else:
            send_error_msg = 4 #can't delete last remaining row in table
        showadd = 0
    elif "Edit1" in form:
        #edit row 1
        rowID = form["Edit1"].value
        showadd = 2
    elif "Edit2" in form:
        #edit row 2
        rowID = form["Edit2"].value
        showadd = 2
    elif "Edit3" in form:
        #edit row 3
        rowID = form["Edit3"].value
        showadd = 2
    elif "Edit4" in form:
        #edit row 4
        rowID = form["Edit4"].value
        showadd = 2
    elif "Update" in form:
        if "subscriberID" in form:
            sID = form["subscriberID"].value
        else:
            sID = ""
        if "description" in form:
            desc = form["description"].value
        else:
            desc = ""
        if "email" in form:
            email = form["email"].value
        else:
            email = ""
        if "rowID" in form:
            rowID = form["rowID"].value
        else:
            rowID = 0
        if len(sID) != 40:
            send_error_msg = 1 #bad subscriberID
            showadd = 2
        else:
            if len(desc) == 0:
                send_error_msg = 2 #bad description
                showadd = 2
            elif len(desc) > 255:
                send_error_msg = 2 #bad description
                showadd = 2
            elif len(email) == 0:
                send_error_msg = 6 #bad email
                showadd = 2
            elif len(email) > 255:
                send_error_msg = 6 #bad email
                showadd = 2
            else:
                #good data
                x = update_data(rowID, sID, desc, email)
                if x == 0:
                    send_error_msg = 0
                    showadd = 0
                else: # x == 1
                    send_error_msg = 3 #Duplicate subscriberID
                    showadd = 2
    elif "Add" in form:
        showadd = 1
    elif "AddNewSubscriber" in form:
        if "subscriberID" in form:
            sID = form["subscriberID"].value
        else:
            sID = ""

        if "description" in form:
            desc = form["description"].value
        else:
            desc = ""

        if "email" in form:
            email = form["email"].value
        else:
            email = ""
    
        if len(sID) != 40:
            send_error_msg = 1 #bad subscriberID
            showadd = 1
        else:
            if len(desc) == 0:
                send_error_msg = 2 #bad description
                showadd = 1
            elif len(desc) > 255:
                send_error_msg = 2 #bad description
                showadd = 1
            elif len(email) == 0:
                send_error_msg = 6 #bad email
                showadd = 1
            elif len(email) > 255:
                send_error_msg = 6 #bad email
                showadd = 1
            else:
                #good data
                x = add_data(sID, desc, email)
                if x == 0:
                    send_error_msg = 0
                    showadd = 0
                elif x == 2:
                    send_error_msg = 5 #Max of 4 subscriberIDs
                    showadd = 1
                else: # x == 1
                    send_error_msg = 3 #Duplicate subscriberID
                    showadd = 1
        
    elif "Back" in form:
    	send_back = 1
    else:
        send_back = 0
        showadd = 0

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
    print "R.E.D.M.A. Subscriber Configuration Page"
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
    #print "<h1>R.E.D.M.A. Subscriber Configuration Page</h1>"
    print """<img src="../redma_top.jpg" alt="REDMA" height="10%" width="20%">"""
    print "<hr>"
    if showadd == 0:
        print_data_table(records, send_error_msg)
    elif showadd == 2:
        edit_data(rowID, send_error_msg)
    else:
        print_add_data_table(send_error_msg)
        
    print "</body>"
    print "</html>"

    sys.stdout.flush()

if __name__=="__main__":
    main()




