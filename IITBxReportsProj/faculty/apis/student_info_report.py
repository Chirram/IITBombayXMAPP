#IMPORTING DEPENDENCIES

from inputs import DatabaseConfig

import MySQLdb
import pymongo
from pymongo import MongoClient



def get_student_course_attendance(student_id,course_id):
	print course_id
	print student_id
	# Establish database connection
	
	try: 
		db = MySQLdb.connect(DatabaseConfig.MYSQL_HOST,DatabaseConfig.MYSQL_USER,DatabaseConfig.MYSQL_PWD,DatabaseConfig.MYSQL_DB)  #Getting MySQL Database Connection
		cursor = db.cursor()
	except:
	# Create a cursor object using cursor() method 
		print "Error, in estabilishing MySQL Connection"
		raise Exception,err;

	
	#Query to fetch course id and no of course components visited by the user
	query='select count(*) as total_visited from courseware_studentmodule where (module_type="video" OR module_type="problem") and course_id="'+course_id+'"  and student_id='+str(student_id)+';'	
	try:
		#Executing query
		cursor.execute(query)
		#Fetch all the records
		data=cursor.fetchall()
		db.close()
	except Exception,err:
		print "Error, in fetching student attendance(While executing query to fetch data from MySQL database)"
		print Exception,err
		raise Exception,err;
	try:
		connection=MongoClient(DatabaseConfig.MONGO_HOST,DatabaseConfig.MONGO_PORT)		#Acquiring Connection from mongo database
	except Exception,err:
		print "Error in getting Mongo Connection"
		raise Exception,err;
	total_components=0
	try:
		database=connection[DatabaseConfig.MONGO_DATABASE1]	#edxapp is mongo database containg all the course in modulestore collection
		cursor=database[DatabaseConfig.MDC1].aggregate([{"$match":{"_id.course":course_id.split("/")[-2],"_id.category":"vertical","_id.revision":{"$ne":"draft"}}},{"$project":{"no":{"$size":"$definition.children"}}}]);
		
		#print document
		for document in cursor["result"]:
			print document
			total_components=total_components+document["no"]
		connection.close()
	except Exception,err:
		print "Error, in iterating mongo documents"
		print Exception,err
		#raise Exception,err;
	return [data[0][0],total_components]

