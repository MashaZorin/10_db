import sqlite3   #enable control of an sqlite database
import csv       #facilitates CSV I/O

f="discobandit.db"

db = sqlite3.connect(f) #open if f exists, otherwise create
c = db.cursor()#facilitate db ops
e = db.cursor()

def print_grades():
    current_student = ""
    print "printing student's grades"
    for display in c.execute("SELECT name, code, mark FROM courses, peeps WHERE peeps.id = courses.id"):
        if(display[0] != current_student):
            current_student = display[0]
            print "\n" + current_student + "'s classes"
        print str(display[1]) + ":" + str(display[2])
    print ""

print_grades()

def calc_peeps_avg():
    c.execute("CREATE table IF NOT EXISTS peeps_avg(id INTEGER, average REAL)")
    for ids in c.execute("SELECT id FROM peeps"):
        grades = e.execute("SELECT mark FROM courses WHERE courses.id = %s" % (ids[0]))
        x = ()
        for grade in grades:
            x += grade
        #e.execute("UPDATE peeps_avg SET average = %s WHERE %s = peeps_avg.id" % (float(sum(x))/len(x), ids))
        e.execute("INSERT INTO peeps_avg VALUES(%s, %s)" % (ids[0], sum(x)/len(x)))

for status in e.execute("SELECT count(*) FROM sqlite_master WHERE type = 'table' AND name = 'peeps_avg'"):
    if(status[0] != 1):
        calc_peeps_avg()
        
def add(code, mark, ids):
    c.execute("INSERT INTO courses VALUES('%s', %s, %s)" % (code, mark, ids))
    x = ()
    for grade in c.execute("SELECT mark FROM courses WHERE %s = courses.id" % (ids)):
        x += grade
    c.execute("UPDATE peeps_avg SET average = %s WHERE %s = peeps_avg.id" % (float(sum(x)) / len(x), ids))

#==========================================================
db.commit() #save changes
db.close()  #close database
