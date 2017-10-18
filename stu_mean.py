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

#print_grades()


#run this only if the table does not exist
#needs this because of INSERT, we call INSERT multiple times which means we have 5 rows of the same averages
#add try, catch (ok try catch works)
#ok it didn't work, but now it works because before INSERT was try, which meant it went to except
#when the two were switched, [0] was missing at ids which meant it was adding (5,) instead of 5, causing it to fail each time
#ok it didn't work, UPDATE works but doesn't do anything
'''
for status in e.execute("SELECT count(*) FROM sqlite_master WHERE type = 'table' AND name = 'peeps_avg'"):
    if(status[0] != 1):
        calc_peeps_avg()
'''

'''
#this is broken, my mind is falling alseep
def calc_check():
    for status in e.execute("SELECT count(*) FROM sqlite_master WHERE type = 'table' AND name = 'peeps_avg'"):
        return (status[0] == 1)
    print "stopped"
    calc_peeps_avg()
'''        

#this version works
def calc_peeps_avg():
    for status in e.execute("SELECT count(*) FROM sqlite_master WHERE type = 'table' AND name = 'peeps_avg'"):
        if(status[0] == 1):
            #print "this is broken"
            return False;

    #print "it gets here"
    c.execute("CREATE table IF NOT EXISTS peeps_avg(id INTEGER, average REAL)")
    for ids in c.execute("SELECT id FROM peeps"):
        grades = e.execute("SELECT mark FROM courses WHERE courses.id = %s" % (ids[0]))
        grade_list = ()
        for grade in grades:
            grade_list += grade
        e.execute("INSERT INTO peeps_avg VALUES(%s, %s)" % (ids[0], sum(grade_list)/len(grade_list)))
        '''
        try:
            #print "UPDATE peeps_avg SET average = %s WHERE %s = peeps_avg.id" % (float(sum(x))/len(x), ids[0])
            e.execute("UPDATE peeps_avg SET average = %s WHERE %s = peeps_avg.id" % (float(sum(grade_list))/len(grade_list), ids[0]))
            print "this is working"
        except:
            e.execute("INSERT INTO peeps_avg VALUES(%s, %s)" % (ids[0], sum(grade_list)/len(grade_list)))
            print "this is nOT working"
        '''

#ok this is redundant because we can just call calc_peeps_avg() again, but this is for singlar ones
#edit, we can't
#this is not redundant anymore
def add(code, mark, ids):
    print "added '%s', %s, %s" % (code, mark, ids)
    #inserted new course
    c.execute("INSERT INTO courses VALUES('%s', %s, %s)" % (code, mark, ids))
    x = ()
    for grade in c.execute("SELECT mark FROM courses WHERE courses.id = %s" % (ids)):
        x += grade
    print_average(ids)
    #updated average
    print("updating average")
    c.execute("UPDATE peeps_avg SET average = %s WHERE %s = peeps_avg.id" % (float(sum(x)) / len(x), ids))
    print_average(ids)

def print_average(ids):
    for grade in c.execute("SELECT average FROM peeps_avg WHERE peeps_avg.id = %s" % (ids)):
        print "grade: " + str(grade[0])
        
#wrapper for add
def add_new_rows():
    with open('data/courses.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            existing = e.execute("SELECT count(*) FROM courses WHERE code = '%s' AND mark = %s AND id = %s" % (row["code"], row["mark"], row['id'])).fetchall()
            for num in existing:
                if (num[0] != 1):
                    add(row["code"], row["mark"], row['id'])

def testing():
    calc_peeps_avg()
    print_grades()
    add("life", 10000, 8)
    add_new_rows()

testing()

#==========================================================
db.commit() #save changes
db.close()  #close database
