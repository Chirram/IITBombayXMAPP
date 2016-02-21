#IMPORTING DEPENDENCIES

from inputs import DatabaseConfig

import MySQLdb



# FUNCTION TO GET LIST OF COURSES OF A FACULTY 	
def get_courses_faculty(faculty_id):
	try:
		db = MySQLdb.connect(DatabaseConfig.MYSQL_HOST,DatabaseConfig.MYSQL_USER,DatabaseConfig.MYSQL_PWD,DatabaseConfig.MYSQL_DB )
		try:	
			organization_cursor = db.cursor()
			query = "select org_id"
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
	
	
	

