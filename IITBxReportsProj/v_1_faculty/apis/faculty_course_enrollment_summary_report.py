#IMPORTING DEPENDENCIES

from inputs import DatabaseConfig

import pymongo
import MySQLdb
from pymongo import MongoClient


# FUNCTION TO GET LIST OF COURSES OF A FACULTY 	
def get_courses_faculty(faculty_id):
	try:
		db = MySQLdb.connect(DatabaseConfig.MYSQL_HOST,DatabaseConfig.MYSQL_USER,DatabaseConfig.MYSQL_PWD,DatabaseConfig.MYSQL_DB )
		try:	
			cursor = db.cursor()
			query = "select b.course_id,count(*) no_of_students from student_courseenrollment a inner join student_courseaccessrole b on a.course_id=b.course_id where a.is_active=1 and b.user_id= "+ faculty_id +" and b.role='instructor' group by b.course_id"
	   		cursor.execute(query)
	   		try:
				cursor.fetchall()
				
				try:
					result=[]
					columns=tuple([d[0].decode('utf8') for d in cursor.description])
					for row in cursor:
						result.append(dict(zip(columns, row)))
						#print result
					try:
						#DB close	
						db.close()
						return result
					except:
						print "Unable to close : get_courses_faculty"
		
				except:
					print "Unable to Dump to json object : get_courses_faculty"
			except:
				print "Unable to fetch data : get_courses_faculty"
		except:
			print "Unable to execute query : get_courses_faculty"
			#DB close	
			db.close()
	except:
		print "Unable to connect to MYSQL database : get_courses_faculty"
	
	
	

