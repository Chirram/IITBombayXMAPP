
from django.shortcuts import render
from django.db import models
from django.contrib.auth.models import User 
from django.template import RequestContext,loader
from django.http import HttpResponse
from django.shortcuts import render_to_response

#This method displays total number of registrations for each day
def reg_count(ip,user,pwd,db):
	#!/usr/bin/python

	import MySQLdb

#Establish connection to database
	db=MySQLdb.connect(host=ip,user=user,passwd=pwd,db=db)

#Create a cursor object using cursor method
	cursor=db.cursor()

#SQL query to fetch number of registrations
	query="select date(date_joined) as day,count(*) as regs from auth_user group by date(date_joined); "

	try:
	#execute SQL query
		cursor.execute(query)
	
		columns=[column[0] for column in cursor.description]
		results=[]
		for row in cursor.fetchall():
			results.append(dict(zip(columns,row)))

	except:
		print "Error:Unable to fetch data"
	
	return results

#Disconnect from server
	db.close()

	
