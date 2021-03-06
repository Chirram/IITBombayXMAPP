from django.http import HttpResponse
from django.template import Context, loader
from django.template import RequestContext
from django.shortcuts import render_to_response, render, get_object_or_404
#from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
import datetime
'''
Description: 
	This function gives a) number of students enrolled datewise b) total number of enrollments
    Input parameters: 
	@ip: ip address of MySQL server
	@user: username
	@pwd: password
	@db: database name 
    Output: 
	@results : returns number of students datewise 
	@count :returns total number of students enrolled till date 
    Output format :
	@ output_list = [collection of results(index=0), max_page(index=1),records_per_page(2),page_no(3)]. 
		max_page : it gives the total number of pages required to display the result (used for the purpose of pagination) .
    Author:
	Gunjan Kulkarni and Nikhita Begani
    Date of creation:
	18/06/2015
'''
def get_course_enrollment_body(ip,user,pwd,db,page_no,records_per_page,startdate,enddate):	#declaration function
    import math
    import MySQLdb	#importing the database
    output_list=[]	#declaring an empty list
    try :
        db = MySQLdb.connect(host=ip,user=user,passwd=pwd,db=db)	#connectiong to the database
        cursor = db.cursor()
        offset=(page_no-1)*records_per_page	#number: of records to skip to reach the present required page
        query="select date(created) as dt , count(*) as ct  from student_courseenrollment where date(created)>=\'"+startdate+"\' and date(created) <= \'"+enddate+"\' group by date(created) limit " + str(offset) + "," + str(records_per_page)		#query for number of students enrolled datewise run on selected set of records
        cursor.execute(query)		#query execution
        result=cursor.fetchall()	#fetch the records selected
        query="select count(*) as ct  from student_courseenrollment where date(created)>=\'"+startdate+"\' and date(created) <= \'"+enddate+"\' group by date(created)"
        cursor.execute(query)
        total_page=math.ceil(float(cursor.rowcount)/float(records_per_page))	#calculating total number of pages required for the records
        output_list.append(result)		# 0th index : data for number of students enrolled datewise
        output_list.append(int(total_page))		# 1st index : maximum pages required for displaying the query
        output_list.append(records_per_page)    # 2nd index : number of records per page returned
        output_list.append(page_no)		# 3rd index : page number
        db.close()	#closing the database connection
    except :
        print "Error in establishing database connection"  #exception 
    return output_list		#return all the values as list
