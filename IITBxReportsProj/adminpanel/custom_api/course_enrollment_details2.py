#this function gives no. of enrollments datewise
import pymongo
def courseenrolled_datewise(ip,user,pwd,db):
    db = pymongo.connect(host=ip,user=user,passwd=pwd,db=db) 
    cur = db.cursor()
    cur.execute("SELECT count(*) as c,date(created) as d FROM student_courseenrollment group by date(created)")
    columns=[column[0] for column in cur.description]
    results={}
    for i in range(cur.rowcount):
        row=cur.fetchone() 
        print "ok2"         
        results[str(row[1])]=row[0]  
        #print str(row[0])
        #print str(row[1])
    return results


#this function will return total number of enrollments
def courseenrolled_in_total(ip,user,pwd,db):
    db = pymongo.connect(host=ip,user=user,passwd=pwd,db=db) 
    cur = db.cursor()
    cur.execute("SELECT count(*) as c FROM student_courseenrollment")
    columns=[column[0] for column in cur.description]
    count={}
    for i in range(cur.rowcount):
        row=cur.fetchone() 
        #print "ok2"         
        count[str(row[0])]=row[1]  
        #print str(row[0])
        #print str(row[1])
    return count

#this function will give the courses which are enrolled between two dates
def courseenrolled_between_dates(ip,user,pwd,db,fromdate,todate):
    results= {}
    fdate = fromdate
    edate = todate
    if fdate>edate:
        t=fdate
        fdate=edate
        edate=t 
    db = pymongo.connect(host=ip, user=user,passwd=pwd, db=db) 
    cur = db.cursor() 
    cur.execute("SELECT count(*) as c FROM student_courseenrollment where date(created)>=\'"+fdate+"\' and date (created)<=\'"+edate+"\' ")
    columns=[(column[0]) for column in cur.description]
    for i in range(cur.rowcount):
        row=cur.fetchone() 
        results[str(row[0])]=row[1]  
    return results


#this function will return courses which are enrolled on a particular day
def courseenrolled_per_day(ip,user,pwd,db,date0):
    date1=date0
    date2=date1
    date1=date1.strip(' \t\n\r')
    list1=date1.split(" ")
    w=list1[0]
    w1=w[:3]
    list1[0]=w1
    date1=' '.join(list1)    
    #date is changed to proper format to extract query
    date=datetime.datetime.strptime(date1, "%b %d, %Y").strftime("%Y-%m-%d")
    db = pymongo.connect(host=ip,user=user,passwd=pwd,db=db) 
    cur = db.cursor() 
    results= {}
    cur.execute("SELECT count(*) as c ,course_id as d FROM student_courseenrollment where date(created)=\'"+date+"\' group by course_id")
    columns=[(column[0]) for column in cur.description]
    for i in range(cur.rowcount):
        row=cur.fetchone() 
        results[str(row[0])]=row[1] 
    return results
