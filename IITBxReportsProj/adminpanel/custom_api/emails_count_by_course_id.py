from django.http import HttpResponse
from django.template import Context, loader
from django.template import RequestContext
from django.shortcuts import render_to_response, render, get_object_or_404

import MySQLdb

#this method calculates the number of emails coursewise	
def get_emails_count_by_course_id(ip,user,pwd,db):
#this variable connects the mysql database    
    db = MySQLdb.connect(host=ip, user=user,passwd=pwd, db=db) 
    #Create a cursor object using cursor method
    cursor = db.cursor() 
    try:
	#this will fetch and execute the sql query
        cursor.execute("SELECT count(*) as total,course_id from bulk_email_courseemail group by course_id")
        columns=[column[0] for column in cursor.description]
        number_of_emails={}
        for i in range(cursor.rowcount):
            row=cursor.fetchone()
            
#print ("api prints",str(row[1]),row[0])         
            number_of_emails[str(row[1])]=row[0] 
    except:
        print "Error:Unable to fetch data"
    db.close()
    return number_of_emails
