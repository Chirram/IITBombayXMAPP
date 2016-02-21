'''
Description : Course Enrollment details on a date.
Input : 
	@ip: ip of database server,
	@user: username,
	@paswd: password,
	@db: database name,
	@page_no: starting page number of the table "Courwise Enrollment Count on a date",
	@records_per_page: Number of records per page for the table "Courwise Enrollment Count on a date",
	@date: date for which records are required
Output : 
	@output_list :a list containing the following elements::
		output_list[0] : dictionary "results" of the table "Courwise Enrollment Count on a date",
		output_list[1] : max_page
		output_list[2] : page_no
		output_list[3] : records_per_page
Author :
	Nikhita Begani and Gunjan Kulkarni
Date :
	24/06/2015

'''


def get_course_enrollment_detail_coursewise_on_a_date(ip,user,paswd,db,page_no,records_per_page,date):
    #transforming the date format .Eg-Jan. 4, 2015 => 2015-01-04
    import MySQLdb
    import datetime
    #print "Date in .py",date
    date=date.strip(' \t\n\r')         
    date=date.replace(".",'')
    list_date=date.split(' ')
    w=list_date[0]
    w1=w[:3]
    list_date[0]=w1
    date=' '.join(list_date)
    date=datetime.datetime.strptime(date, "%b %d, %Y").strftime("%Y-%m-%d")
    #limiting the query for pagination purpose
    skip=records_per_page*(page_no-1)
    import math
    #creating database connection and fetching data from database
    try :
        db = MySQLdb.connect(ip,user,paswd,db) 
        cur = db.cursor() 
        results= []
        query_total="SELECT count(*) FROM student_courseenrollment where date(created)=\'"+date+"\' group by course_id"
        cur.execute(query_total)
        total=len(cur.fetchall())
        max_page=math.ceil(float(total)/float(records_per_page))
        query="SELECT count(*) as c ,course_id as d FROM student_courseenrollment where date(created)=\'"+date+"\' group by course_id limit "+str(skip)+","+str(records_per_page)
        cur.execute(query)
        columns=[(column[0]) for column in cur.description]
        results=cur.fetchall()
        print "result fetched",results #dictionary formed for the table "Courwise Enrollment Count on a date"
        db.close()
    except :
        print "Error in establishing MySQL connection"        #when database could not be reached
    output_list=[]
    output_list.append(results)			#output_list[0] : dictionary "results" of the table "Courwise Enrollment Count on a date",
    output_list.append(int(max_page))		#output_list[1] : max_page
    output_list.append(page_no)			#output_list[2] : page_no
    output_list.append(records_per_page)	#output_list[3] : records_per_page 
    #print "About to return" 
    return output_list



'''
Description : Course Enrollment details on a date.
Input : 
	@ip: ip of database server,
	@user: username,
	@paswd: password,
	@db: database name,
	@page_no: starting page number of the table "Student details who Enrollment on a date",
	@records_per_page: Number of records per page for the table "Student details who Enrollment on a date",
	@date: date for which records are required
Output : 
	@output_list :a list containing the following elements::
		output_list[0] : dictionary "results" of the table "Student details who Enrollment on a date",
		output_list[1] : max_page
		output_list[2] : page_no
		output_list[3] : records_per_page
Author :
	Nikhita Begani and Gunjan Kulkarni
Date :
	24/06/2015

'''
def get_course_enrollment_detail_on_a_date(ip,user,paswd,db,page_no,records_per_page,date):
    #transforming the date format .Eg-Jan. 4, 2015 => 2015-01-04
    import MySQLdb
    import datetime
    date=date.strip(' \t\n\r')         
    date=date.replace(".",'')
    list_date=date.split(' ')
    w=list_date[0]
    w1=w[:3]
    list_date[0]=w1
    date=' '.join(list_date)
    date=datetime.datetime.strptime(date, "%b %d, %Y").strftime("%Y-%m-%d")
    #limiting the query for pagination purpose
    skip=records_per_page*(page_no-1)
    import math
    #creating database connection and fetching data from database
    try :
        db = MySQLdb.connect(ip,user,paswd,db) 
        cur = db.cursor() 
        results= []               #empty list declared
        cur = db.cursor() 
        query_total="select a.course_id from student_courseenrollment as a, auth_user as b,auth_userprofile as c where a.user_id=b.id and a.user_id=c.user_id and date(a.created)=\'"+date+"\'"
        cur.execute(query_total)
        total=len(cur.fetchall())
        max_page=math.ceil(float(total)/float(records_per_page))
        query="select a.course_id as course,a.user_id as student_id,c.name as student_name,b.username as student_username from student_courseenrollment as a, auth_user as b,auth_userprofile as c where a.user_id=b.id and a.user_id=c.user_id and date(a.created)=\'"+date+"\' limit "+str(skip)+","+str(records_per_page)     
        cur.execute(query)                                #MySQL query
        rows=cur.fetchall()        #all the data fetch
        #list is created for the table "Student details who Enrollment on a date"
        for row in rows:         #takes each row in the data	
            results.append([row[0],row[1],row[2],row[3]])         #a list is created and appended in the parent list
        db.close()            #connection closed
    except :
        print "Error in establishing MySQL connection"        #when database could not be reached
    output_list=[]
    output_list.append(results)    	#output_list[0] : dictionary "results" of the table "Student details who Enrollment on a date",
    output_list.append(int(max_page))		#output_list[1] : max_page
    output_list.append(page_no)			#output_list[2] : page_no
    output_list.append(records_per_page)	#output_list[3] : records_per_page    
    return output_list
