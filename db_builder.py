import sqlite3   #enable control of an sqlite database
import csv       #facilitates CSV I/O

#==========================================================
#testing DictReader
#creates a dictionary for each line with column names corresponding to values
'''
with open("courses.csv") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(row)

with open("peeps.csv") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(row)
'''
#==========================================================        

f="discobandit.db"

db = sqlite3.connect(f) #open if f exists, otherwise create
c = db.cursor()    #facilitate db ops

#==========================================================

create_course_table = "CREATE TABLE courses(code TEXT, mark INTEGER, id INTEGER)"
c.execute(create_course_table)

with open("data/courses.csv") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        add_course_row = "INSERT INTO courses VALUES('%s', %s, %s)" % (row["code"], row["mark"], row["id"])
        #print add_course_row
        c.execute(add_course_row)

create_peeps_table = "CREATE TABLE peeps(name TEXT, age INTEGER, id INTEGER)"
c.execute(create_peeps_table)

with open("data/peeps.csv") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        add_peeps_row = "INSERT INTO peeps VALUES('%s', %s, %s)" % (row["name"], row["age"], row["id"])
        #print add_peeps_row
        c.execute(add_peeps_row)

#==========================================================
db.commit() #save changes
db.close()  #close database

