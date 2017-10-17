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
c = db.cursor()#facilitate db ops
e = db.cursor()

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

current_student = ""
print "printing student's grades"
for display in c.execute("SELECT name, code, mark FROM courses, peeps WHERE peeps.id = courses.id"):
    if(display[0] != current_student):
        current_student = display[0]
        print "\n" + current_student + "'s classes"
    print str(display[1]) + ":" + str(display[2])

c.execute("CREATE TABLE peeps_avg(id INTEGER, average REAL)")

for ids in c.execute("SELECT id FROM peeps"):
    grades = e.execute("SELECT mark FROM courses WHERE courses.id = %s" % (ids[0]))
    x = ()
    for grade in grades:
        x += grade
    #print float(sum(x))/len(x)
    e.execute("INSERT INTO peeps_avg VALUES(%s, %s)" % (ids[0], sum(x)/len(x)))

def add(code, mark, ids):
    c.execute("INSERT INTO courses VALUES('%s', %s, %s)" % (code, mark, ids))
    x = ()
    for grade in c.execute("SELECT mark FROM courses WHERE %s = courses.id" % (ids)):
        x += grade
    c.execute("UPDATE peeps_avg SET average = %s WHERE %s = peeps_avg.id" % (float(sum(x)) / len(x), ids))

for printing in c.execute("SELECT * FROM peeps_avg"):
    print(printing)

add("life", 100, 4)
add("life", 3, 8)

for printing in c.execute("SELECT * FROM peeps_avg"):
    print(printing)

current_student = ""
print "printing student's grades"
for display in c.execute("SELECT name, code, mark FROM courses, peeps WHERE peeps.id = courses.id"):
    if(display[0] != current_student):
        current_student = display[0]
        print "\n" + current_student + "'s classes"
    print str(display[1]) + ":" + str(display[2])

#==========================================================
db.commit() #save changes
db.close()  #close database

