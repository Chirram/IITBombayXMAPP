from django.shortcuts import render
from django.db import models
from django.contrib.auth.models import User 
from django.template import RequestContext,loader
from django.http import HttpResponse
from django.shortcuts import render_to_response

def get_all_stu_registrations(ip,user,pwd,db):
	#!/usr/bin/python
    import MySQLdb
#Establish connection to database
    db=MySQLdb.connect(host=ip,user=user,passwd=pwd,db=db)
    

#Create a cursor object using cursor method
    cursor=db.cursor()

#SQL query to fetch list of students registered to a course
    query="select date(date_joined) as day,count(*) as regs from auth_user group by date(date_joined) order by date(date_joined); "
    try:
	#execute SQL query
        cursor.execute(query)
	#fetch all rows from table
		#result=cursor.fetchall() #list of lists
	        #for row in result:
			#day=row[0]
			#count=row[1]
		
		#print fetched result
			#print "Day=%s,count=%d " % \
             			#( day,count )
        columns=[column[0] for column in cursor.description]
        results={}
        for i in range(cursor.rowcount):
            row=cursor.fetchone()
            
           # print "ok2"         
            results[str(row[0])]=row[1]  
            
       # print "ok2"          

    except:
        print "Error from stureg api:Unable to fetch data"
    return results


	
