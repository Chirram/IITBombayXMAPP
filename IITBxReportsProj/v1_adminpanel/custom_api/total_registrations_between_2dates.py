
from django.shortcuts import render
from django.db import models
from django.contrib.auth.models import User
from django.template import RequestContext,loader, Context
from django.http import HttpResponse
from django.shortcuts import render_to_response, render, get_object_or_404

#This method calculates the total number of registrations between two specific dates provided by the user
def registration_between_specific_dates(ip,user,pwd,db,date1,date2):

	
     #!/usr/bin/python
      
      import MySQLdb
      
      da1=date1
      da2=date2
      #Establish connection to database
      db = MySQLdb.connect(host=ip,user=user,passwd=pwd,db=db)

      #Create a cursor object using cursor method
      cursor = db.cursor()
 
      #SQL query to fetch the total number of registrations between the two dates
      query = "select count(*) as count from auth_user where date(date_joined)>=\'"+ da1+"\' and date(date_joined)<=\'"+da2+"\'"
      
      try:
           #execute SQL query
           cursor.execute(query)
           
           #fetches the result into data variable
           data = cursor.fetchall()
           for row in data:
                    count=row[0]
	   
      except: 
           print "Error: Unable to fetch data"

      db.close()
      return count
      
