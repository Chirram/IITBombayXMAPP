#IMPORTING DEPENDENCIES

from inputs import DatabaseConfig
import pymongo
import MySQLdb
from pymongo import MongoClient


# FUNCTION TO GET LIST OF COURSES OF A FACULTY 	
def get_course_list(facultyid):
	try:
		db = MySQLdb.connect(DatabaseConfig.MYSQL_HOST,DatabaseConfig.MYSQL_USER,DatabaseConfig.MYSQL_PWD,DatabaseConfig.MYSQL_DB )
	except:
		print "Unable to connect to MYSQL database : get_course_list"
	try:	
		cursor = db.cursor()
		query = "select course_id from student_courseaccessrole  where user_id="+ facultyid +" and role = 'instructor'"
   		cursor.execute(query)
	except:
		print "Unable to execute query : get_course_list"
	try:
		results = cursor.fetchall()
	except:
		print "Unable to fetch data : get_course_list"
	try:
		courses=[]
		for row in results:
			 courses.append(row[0])
		#print courses
	except:
		print "Unable to Dump to json object : get_course_list"
	try:
		#DB close	
		db.close()
		return courses
	except:
		print "Unable to respond : get_cours_list"
	

