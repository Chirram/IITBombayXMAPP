# IMPORTING modules

import pymongo
import MySQLdb
from pymongo import MongoClient
from inputs import DatabaseConfig
'''
Description : This method calculates the total number of discussions, answered questions and unanswered questions for all the courses a faculty has been assigned to 

INPUT PARAMETERS :
facultyid : The user_id of the user who has been assigned the role of instructor

OUTPUT PARAMETRS :
result : It has the data type- list of lists which is of the form
		[
			[COURSE_1,TOTAL COMMENT_THREADS_COUNT_1,QUESTIONS_COUNT_1,UNANSWERED_QUESTIONS_COUNT_1,DISCUSSIONS_COUNT_1],
			[COURSE_2,TOTAL COMMENT_THREADS_COUNT_2,QUESTIONS_COUNT_2,UNANSWERED_QUESTIONS_COUNT_2,DISCUSSIONS_COUNT_2],
			.....
		]

Author : NITISH DEO
Email id : nitishdeo1194@gmail.com	
Date of Created : 20/06/2015

'''
def get_discussion_forum_report(studentid):
	
	# ESTABLISHING CONNECTION WITH DATABASE
	try:
		db = MySQLdb.connect(DatabaseConfig.MYSQL_HOST,DatabaseConfig.MYSQL_USER,DatabaseConfig.MYSQL_PWD,DatabaseConfig.MYSQL_DB )
	except: 
		print "Unable to connect to MYSQL database 111"
	try:
		client = MongoClient(DatabaseConfig.MONGO_HOST, DatabaseConfig.MONGO_PORT)
	except:
		print "Unable to connect to MongoDB 111 "

	# SELECTING DATABASE
	try:
		discussion_db = client.cs_comments_service_development
	except: 
		print "Unable to select MongoDB database"
	try:
		discussion_coll = discussion_db.contents
	except:
		print "Unable to select MongoDB collection"
	
	try:    # EXECUTING MYSQL QUERIES
		
                cursor = db.cursor()
		query = "select distinct(course_id) from student_courseenrollment  where is_active=1 and user_id= " + str(studentid)  
		cursor.execute(query)
	except:
		print "Unable to execute queries 111"
	try:   		
		data=cursor.fetchall()
	except : 
		print "Unable to fetch data 111"
                # CREATING EMPTY LIST TO STORE RESULT TO BE RETURNED TO TEMPLATE 
	result=[]		
        sid=str(studentid)
	for element in data:
		try:
			total= discussion_coll.find({"_type" : "CommentThread" ,"author_id" : sid , "course_id" : element[0]}).count()
       	       		questions = discussion_coll.find({"_type" : "CommentThread" ,"author_id" : sid, "course_id" : element[0],"thread_type" : "question"}).count()
			discussions = discussion_coll.find({"_type" : "CommentThread" ,"author_id" : sid, "course_id" : element[0],"thread_type" : "discussion"}).count()
        	        unanswered_questions = discussion_coll.find({"_type" : "CommentThread" ,"author_id" : sid, "thread_type" : "question","comment_count" : 0 , "course_id" : element[0],}).count()

        	        #APPENDING THE QUERY RESULTS TO THE RESULT LIST 
			result.append([element[0],total,questions,unanswered_questions,discussions]);
	 	       	
		except:
	        
   			print "Error: Unable to fetch data"

	#DB CLOSE
        db.close()
        print result
	return result 
	
