
from django.shortcuts import render
from django.db import models
from django.contrib.auth.models import User
from django.template import RequestContext,loader, Context
from django.http import HttpResponse
from django.shortcuts import render_to_response, render, get_object_or_404
'''
Description : this method calculates the total number of registrations between two specific dates provided by user

Input Parameters :
ip : IP address of database
user : user name of the database
pwd : password of the database
db : database name in the mysql database
date1: starting date
date2 : end date given by the user

Output Parameters :
count : it stores the count of total number of registration happened between two dates provided by the user 

Author : Manisha Yadav
Date of Created : 20/06/2015

'''


def registration_specific_dates(ip,user,pwd,db,date1,date2):

	
     #!/usr/bin/python
      
      import MySQLdb
      
      day1=date1
      day2=date2
      #Establish connection to database
      db = MySQLdb.connect(host=ip,user=user,passwd=pwd,db=db)

      #Create a cursor object using cursor method
      cursor = db.cursor()
 
      #SQL query to fetch the total number of registrations between the two dates
      query = "select count(*) as count from auth_user where date(date_joined)>=\'"+ day1+"\' and date(date_joined)<=\'"+day2+"\'"
      
      try:
           #execute SQL query
           cursor.execute(query)
           
           #fetches the result into data variable
           data = cursor.fetchall()
           for row in data:
                    count=row[0]
	   
      except: 
           print"Error: Unable to fetch data"

      db.close()
      return count #returns the count of total registration
      

'''
Description : this method prints the details of the registrations occurred between two specific days.It prints the date on which registrations happened and prints the userid and username.

Input Parameters :
ip : IP address of database
user : user name of the database
pwd : password of the database
db : database name in the mysql database
date1: starting date
date2 : end date given by the user

Output Parameters :
results : details of the user who registered between the given two dates.It returns the day on which the user has registered,the username and his userid.

Author : Manisha Yadav
Date of Created : 20/06/2015

'''

def details_of_registration_between_dates(ip,user,pwd,db,page_no,records_per_page,date1,date2):
	
     #!/usr/bin/python
      print("called reg")
      fdate1=date1
      fdate2=date2
      import MySQLdb
      import math
      #Establish connection to database
      db = MySQLdb.connect(host=ip,user=user,passwd=pwd,db=db)

      #Create a cursor object using cursor method
      cursor = db.cursor()
      skip=records_per_page*(page_no-1)
       #SQL query to fetch the total number of registrations between the two dates
      query = "select date(date_joined) from auth_user where date(date_joined)>=\'"+ fdate1+"\' and date(date_joined)<=\'"+fdate2+"\'"
      query1 = "select date(date_joined) as Day,id as UserId,username as UserName from auth_user where date(date_joined)>=\'"+ fdate1+"\' and date(date_joined)<=\'"+fdate2+"\' limit "+str(skip)+","+str(records_per_page) 
      try:
           #execute SQL query
           cursor.execute(query)
           total=math.ceil(float(cursor.rowcount)/float(records_per_page))
           total_rows=cursor.rowcount
           cursor.execute(query1)
		   #fetches the result into data variable
           data = cursor.fetchall()
      except: 
           print "Error: Unable to fetch data"
      #closing the database connection
      db.close()
      output=[]
      output.append(data)
      output.append(int(total))
      output.append(page_no)
      output.append(records_per_page)
      output.append(total_rows)
	  
      return output #returns the fields day,userid and username.
      
