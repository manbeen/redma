#!/usr/bin/python

import sqlite3

#globals
dbname='/home/pi/nodedb.db'

#connect to DB
conn=sqlite3.connect(dbname)
curs=conn.cursor()

#remove data older than 48 hours
query = "DELETE FROM table_sensory_data WHERE timestamp < datetime('now','localtime','-2 days')"
curs.execute(query)

#commit the changes
conn.commit()
conn.close()
