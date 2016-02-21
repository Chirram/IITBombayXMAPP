# Create your views here.
from django.shortcuts import render
from django.db import models
from django.contrib.auth.models import User
from django.template import RequestContext,loader, Context
from django.http import HttpResponse
from django.shortcuts import render_to_response, render, get_object_or_404
import math

'''
Description: 	This function  gives the emais count of all  courses
		It returns a list containing all the courses no_of_emails and the subject list
	Input Parameters :
		ip : IP address of database
		user : user name of the database
		pwd : password of the database
		db : database name in the mysql database
		page_no : the page on which user want the data
		no_of_entries :the data limit per page

	Output Parameters : A dictionary of key(course_id), value(email_count) pairs
		course_id : unique id of the course
		email_count : no of emails of each course
		subject:subject in particular course
		total_emails :total number of emails of all courses
		total_pages :total number of pages required for given no_of entries

	Author : Divyanshu Agrawal
	Date of Created : 22/06/2015

'''
#this function used to display the course_id,subject and emails_count
def emais_count_coursewise(ip,user,pwd,db,page_no,no_of_entries):
	
     #!/usr/bin/python
	 #here the dates are hardcoded .If it is passed as parameter then remove these dates.
        date1='1995-01-01'
        date2='2100-01-01'
		
        import MySQLdb		
	  # Establish database connection and create 2 cursor object
        db = MySQLdb.connect(host=ip,user=user,passwd=pwd,db=db)
        cursor = db.cursor()
        cursor1=db.cursor()
        try:
	# This calculation is done for pagination process.
          email_count_query="select count(distinct course_id) as count,count(*) as total_emails from bulk_email_courseemail where date(created)>='"+date1+"' and date(created)<='"+date2+"';";
	      total_emails=0;
		  count=0
            try:	
              cursor1.execute(email_count_query)
              count = cursor1.fetchall()
		     # for key in count:
			  #  count=list(key)
		     # print count
		     # total_emails=count[1]
		      #total_pages=int(math.ceil(float(count[0])/float(no_of_entries)))
            except:
		      print "unable to fetch data :: breaking point-1 "
	       offset=0;			
    	   total_pages=1;
           if(no_of_entries>=count[0][0]):
				total_pages=-(-(int(count[0][0]))/(int(no_of_entries)))
				offset=int(no_of_entries)*(int(page_no)-1);
				if(offset>count[0][0]):
					offset=0
					page_no=1	
		# Execute SQL queries and fetch the course_id ,subject,emails_count coursewise	
	        cursor.execute("SELECT course_id, count(*) as total,subject from bulk_email_courseemail where date(created)>='"+date1+"' and date(created)<='"+date2+"'"+" group by course_id limit "+str(no_of_entries)+" offset "+str(offset)+" ;")
	        data=cursor.fetchall();
	        print data
	        results=[]					#a list to store all data
	        results.append(int(total_emails))			#this is appending the total number of emails in results.
	        results.append(total_pages)				#this is appending the total number of pages required.
	        for element in data:
	   	       results.append(list(element))			#this is appending the actual data like course_id,subject,emails_count coursewise
	        print results
        except: 
            print "Error: Unable to fetch data"   
		# return the course_id,  emais_count, subject	
        return results		
      # Disconnect from server
	 
