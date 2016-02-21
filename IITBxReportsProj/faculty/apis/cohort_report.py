from inputs import DatabaseConfig

import pymongo
import MySQLdb
from pymongo import MongoClient


# FUNCTION TO GET NO OF COHORTS OF COURSES OF A FACULTY 	
def get_faculty_courses_cohort_count(faculty_id):
	try:
		db = MySQLdb.connect(DatabaseConfig.MYSQL_HOST,DatabaseConfig.MYSQL_USER,DatabaseConfig.MYSQL_PWD,DatabaseConfig.MYSQL_DB )
		try:	
			cursor = db.cursor()
			query = "select d.course_id,d.cohort_count from (select count(*) as cohort_count,course_id from course_groups_courseusergroup where group_type='cohort' group by course_id) d inner join ( select course_id from student_courseaccessrole where user_id="+faculty_id+" and role='instructor') c on d.course_id=c.course_id;"
	   		cursor.execute(query)
	   		try:
				cursor.fetchall()
				
				try:
					cohorts_count=[]
					columns=tuple([d[0] for d in cursor.description])
					for row in cursor:
						cohorts_count.append(dict(zip(columns, row)))
						print cohorts_count
					try:
						#DB close	
						db.close()
						return cohorts_count
					except:
						print "Unable to close : get_faculty_courses_cohort_count"
		
				except:
					print "Unable to Dump to json object : get_faculty_courses_cohort_count"
			except:
				print "Unable to fetch data : get_faculty_courses_cohort_count"
		except:
			print "Unable to execute query : get_faculty_courses_cohort_count"
			#DB close	
			db.close()
	except:
		print "Unable to connect to MYSQL database : get_faculty_courses_cohort_count"
