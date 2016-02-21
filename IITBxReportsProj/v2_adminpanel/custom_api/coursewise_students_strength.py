#author : Anjay Abhishek
#date last modified : 19-Jun-15
#---------------------------------------------------------------------------------------------------------
from django.shortcuts import render
from django.db import models
from django.contrib.auth.models import User 
from django.template import RequestContext,loader
from django.http import HttpResponse
from django.shortcuts import render_to_response
import MySQLdb
#systems using MySQLdb drivers should replace all 'pymysql' in this code by MySQLdb
#sample function call : coursewise_strength=get_student_count_coursewise(ip=__MYSQL_SERVER_IP,user=__USER,pwd=__PASSWORD,db=__DATABASE)
#coursewise_strength is dictionary and all arguments are taking in string variables 
#return type is dictionary containing course id as key and corresponding number of students as its value
def get_student_count_coursewise(ip,user,pwd,db): # ip = "database_host_ip" , user = "username" , pwd = "password" , db = "database_name   
#Establish connection to database
    db=MySQLdb.connect(host=ip,user=user,passwd=pwd,db=db)
#Create a cursor object using cursor method
    cursor=db.cursor()
#SQL query to fetch list of students registered to a course
    query="select course_id,count(*) from student_courseenrollment group by course_id order by count(*) desc; "
    try:
	#execute SQL query
        cursor.execute(query)
        results={}
        for i in range(cursor.rowcount):
            row=cursor.fetchone()
            results[str(row[0])]=row[1]  #store result in dictionary (eg: result["CS101"]=10  meaning 10 students in CS101)
    #course id must be unique as dictionary expects unique key --> result[key] --> key is unique
    except:
        print "coursewise_students_strength api error : Unable to fetch data" #remove parenthesis for python 2.7 , python 3 expects paranthesis
    db.close()
    return results
