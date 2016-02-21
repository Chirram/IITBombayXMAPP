# Create your views here.
from django.shortcuts import render
from django.db import models
from django.contrib.auth.models import User
from django.template import RequestContext,loader, Context
from django.http import HttpResponse
from django.shortcuts import render_to_response, render, get_object_or_404
import pymongo
#this method calculates the total number of emails between two specific dates provided by user
def emails_count_between_dates(ip,user,pwd,db,date1,date2):
	
     #!/usr/bin/python
      
      
      
	da1=date1
	da2=date2
     
#this variable connects the mysql database
	db = pymongo.connect(host=ip,user=user,passwd=pwd,db=db)
      #Create a cursor object using cursor method
    cursor = db.cursor()
	  #this will fetch the sql query
    query = "select count(*) as total from bulk_email_courseemail where date(created)>=\'"+ da1+"\' and date(created)<=\'"+da2+"\'"

    try:
	  #this will execute the query
        cursor.execute(query)
        data = cursor.fetchall()
        for row in data:
            count=row[0]   
    except: 
        print "Error: Unable to fetch data"

     
      
    db.close()
	return count
