import sqlite3
import smtplib
import time

#send email notification
def send_email(msgtxt, email):
    fromaddr = 'redma.alerts@gmail.com'
    subject = 'REDMA Alert'
    message = 'Subject: %s\n\n%s' % (subject, msgtxt)

    # Credentials (if needed)
    username = 'redma.alerts'
    password = 'abcD1234'

    # The actual mail send
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(username,password)
        server.sendmail(fromaddr, email, message)
        server.quit()
        return True
    except:
        return False

# get current email value from DB
def get_email():
    
    email = ""
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    #Administrator's email address
    curs.execute("SELECT email FROM table_node_configuration limit 1")
    rows=curs.fetchall()
    for row in rows:
        email = email + str(row[0]) + "\n"

    #Subscriber account email addresses
    curs.execute("SELECT email FROM table_subscriber")
    rows=curs.fetchall()
    for row in rows:
        email = email + str(row[0]) + "\n"

    email = email.split()
    conn.close()
    return email

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

def get_moving_avg(sensornum, num_samples, nodeID):
    sensor_avg = 0.0
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    query = "SELECT sensor" + str(sensornum) + " FROM table_sensory_data WHERE nodeID="
    query = query +  str(nodeID) + " order by timestamp desc limit " + str(num_samples)
    curs.execute(query)
    rows=curs.fetchall()
    for row in rows:
      sensor_avg = sensor_avg + float(row[0])

    sensor_avg = round(sensor_avg/num_samples,2)
    conn.close()
    return sensor_avg

def get_last_val(sensornum, nodeID):
    last_val = 0.0
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    query = "SELECT sensor" + str(sensornum) + " FROM table_sensory_data WHERE nodeID="
    query = query + str(nodeID) + " order by timestamp desc limit 1"
    curs.execute(query)
    rows=curs.fetchall()
    for row in rows:
      last_val = round(float(row[0]),2)

    conn.close()
    return last_val

def get_threshold(sensornum, nodeID):
    th_sensor = 0.0
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    query = "SELECT th_sensor" + str(sensornum) + " FROM table_node_configuration WHERE nodeID="
    query = query +  str(nodeID)
    curs.execute(query)
    rows=curs.fetchall()
    for row in rows:
      th_sensor = float(row[0])

    conn.close()
    return th_sensor

# store notification data in the database
def log_data(nodeID,sensor_val,th_sensor,email,sentflag,sensor_type):

    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    emailtmp = ',\n'.join(email)
    
    query="INSERT INTO table_notifications VALUES (datetime('now', 'localtime'), (?), (?), (?), (?), (?), (?))"

    curs.execute(query, (nodeID,sensor_val,th_sensor,emailtmp,sentflag,sensor_type))

    # commit the changes
    conn.commit()

    conn.close()

#globals
nodeID = 0
delay = 5
email = ""
num_samples = 10
dbname='/home/pi/nodedb.db'
diff_sensor1 = 1.5 #deg. C
diff_sensor2 = 0.5 #volt
diff_sensor3 = 0.5 #volt
sensor1_tripped = 0
sensor2_tripped = 0
sensor3_tripped = 0
#working locals
sensornum = 1
current_avg1 = 0.0
last_val1 = 0.0
th_sensor1 = 0.0
notify1 = 0
current_state1 = 0
next_state1 = 0
current_avg2 = 0.0
last_val2 = 0.0
th_sensor2 = 0.0
notify2 = 0
current_state2 = 0
next_state2 = 0
current_avg3 = 0.0
last_val3 = 0.0
th_sensor3 = 0.0
notify3 = 0
current_state3 = 0
next_state3 = 0
while True:
    nodeID = get_nodeID()
    email = get_email()
    ################# Sensor 1
    sensornum = 1
    th_sensor1 = get_threshold(sensornum, nodeID)
    current_avg1 = get_moving_avg(sensornum, num_samples, nodeID)
    last_val1 = get_last_val(sensornum, nodeID)
    if last_val1 >= th_sensor1:
        if (last_val1 - current_avg1) >= diff_sensor1:
            notify1 = 1
        else:
            notify1 = 0
    else:
        notify1 = 0
    if notify1 == 0:
        next_state1 = 0
    elif notify1 == 1:
        next_state1 = 1
        if current_state1 == 0:
            sensor1_tripped = 1
            now = time.strftime("%c")
            msgtxt = "REDMA Temperature Sensor Alert NodeID=" + str(nodeID) + ", temp=" + str(last_val1)
            msgtxt = msgtxt + "deg. C, threshold=" + str(th_sensor1) + "deg. C, timestamp=" + str(now)
            if not(send_email(msgtxt, email)):
                print "Error sending Sensor 1 email notification @ " + str(now)
                log_data(nodeID,last_val1,th_sensor1,email,0,"Temperature")
            else:
                print "Sensor 1 Email notification sent successfully @ " + str(now)
                log_data(nodeID,last_val1,th_sensor1,email,1,"Temperature")
        else:
            sensor1_tripped = 0
    current_state1 = next_state1
    ################# Sensor 2
    sensornum = 2
    th_sensor2 = get_threshold(sensornum, nodeID)
    current_avg2 = get_moving_avg(sensornum, num_samples, nodeID)
    last_val2 = get_last_val(sensornum, nodeID)
    if last_val2 >= th_sensor2:
        if (last_val2 - current_avg2) >= diff_sensor2:
            notify2 = 1
        else:
            notify2 = 0
    else:
        notify2 = 0
    if notify2 == 0:
        next_state2 = 0
    elif notify2 == 1:
        next_state2 = 1
        if current_state2 == 0:
            sensor2_tripped = 1
            now = time.strftime("%c")
            msgtxt = "REDMA Water Sensor Alert NodeID=" + str(nodeID) + ", sensor voltage=" + str(last_val2)
            msgtxt = msgtxt + "volts, threshold=" + str(th_sensor2) + "volts, timestamp=" + str(now)
            if not(send_email(msgtxt, email)):
                print "Error sending Sensor 2 email notification @ " + str(now)
                log_data(nodeID,last_val2,th_sensor2,email,0,"Water")
            else:
                print "Sensor 2 Email notification sent successfully @ " + str(now)
                log_data(nodeID,last_val2,th_sensor2,email,1,"Water")
        else:
            sensor2_tripped = 0
    current_state2 = next_state2
    ################# Sensor 3
    sensornum = 3
    th_sensor3 = get_threshold(sensornum, nodeID)
    current_avg3 = get_moving_avg(sensornum, num_samples, nodeID)
    last_val3 = get_last_val(sensornum, nodeID)
    if last_val3 >= th_sensor3:
        if (last_val3 - current_avg3) >= diff_sensor3:
            notify3 = 1
        else:
            notify3 = 0
    else:
        notify3 = 0
    if notify3 == 0:
        next_state3 = 0
    elif notify3 == 1:
        next_state3 = 1
        if current_state3 == 0:
            sensor3_tripped = 1
            now = time.strftime("%c")
            msgtxt = "REDMA Smoke Sensor Alert NodeID=" + str(nodeID) + ", sensor voltage=" + str(last_val3)
            msgtxt = msgtxt + "volts, threshold=" + str(th_sensor3) + "volts, timestamp=" + str(now)
            if not(send_email(msgtxt, email)):
                print "Error sending Sensor 3 email notification @ " + str(now)
                log_data(nodeID,last_val3,th_sensor3,email,0,"Smoke")
            else:
                print "Sensor 3 Email notification sent successfully @ " + str(now)
                log_data(nodeID,last_val3,th_sensor3,email,1,"Smoke")
        else:
            sensor3_tripped = 0
    current_state3 = next_state3
    #print str(current_avg3) + "," + str(last_val3) + "," + str(notify3) + "," + str(sensor3_tripped)

    # Wait before repeating loop
    delay = get_polling_rate()
    time.sleep(delay)
