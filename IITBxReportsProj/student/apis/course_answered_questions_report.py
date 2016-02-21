# IMPORTING LIBRARIES
from inputs import DatabaseConfig
import pymongo
import MySQLdb
from pymongo import MongoClient

# ESTABLISHING CONNECTION WITH DATABASE

client = MongoClient(DatabaseConfig.MONGO_HOST, DatabaseConfig.MONGO_PORT)

# SELECTING DATABASE
discussion_db = client.cs_comments_service_development
discussion_coll = discussion_db.contents


'''
Description : This method returns a list of all the answered questions for a particular course assigned to the faculty 

INPUT PARAMETERS :
facultyid : The user_id of the user who has been assigned the role of instructor
courseid : The course_id for a parrticular course 

OUTPUT PARAMETRS :
result : It has the data type- list of lists which is of the form
		[
			[Title_of_the_question_1,Body_of_the_question_1],
			[Title_of_the_question_2,Body_of_the_question_2],
			.....
		]

Author : NITISH DEO
Email id : nitishdeo1194@gmail.com	
Date of Created : 20/06/2015

'''

def get_answered_questions_report(studentid,courseid) :

	try:    
		result=[]
		discussion_db = client.cs_comments_service_development
		discussion_coll = discussion_db.contents
		ans_ques = discussion_coll.find({"_type" : "CommentThread" , "thread_type" : "question" ,"author_id" : studentid,"course_id" : courseid, "comment_count" : {"$gt" : 0 }} ,  {"_id" : 1,"body" : 1,"title" : 1,"commentable_id" : 1,"comment_count" :1,"author_username" : 1})
		for i in ans_ques:
			result.append([i['title'],i['body'],str(i['commentable_id']),str(i['_id']),i['comment_count'],i['author_username']])
		client.close()
		print result
		return result
	except:
		print "Unable to execute query : answered questions"
	

	


