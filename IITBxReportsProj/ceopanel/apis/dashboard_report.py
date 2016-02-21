#IMPORTING DEPENDENCIES

from inputs import DatabaseConfig

import MySQLdb



# FUNCTION TO GET LIST OF COURSES OF A FACULTY 	
def get_organization_registrations():
	try:
		db = MySQLdb.connect(DatabaseConfig.MYSQL_HOST,DatabaseConfig.MYSQL_USER,DatabaseConfig.MYSQL_PWD,DatabaseConfig.MYSQL_DB )
		try:	
			cursor = db.cursor()
			collation_query_table_1=" select COLLATION_NAME from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='courseware_organization' AND COLUMN_NAME = 'org_id';"
			cursor.execute(collation_query_table_1)
			coll1=cursor.fetchall()
			collation_query_table_2=" select COLLATION_NAME from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='student_courseenrollment' AND COLUMN_NAME = 'course_id';"
			cursor.execute(collation_query_table_2)
			coll2=cursor.fetchall()
			if coll1[0][0] is coll2[0][0]:
				collation=''
			else:
				collation= 'collate ' + coll1[0][0] 
			query = "select org.org_id,sum(c.total) from courseware_organization org inner join (select substring_index(course_id,"+"'/'"+",1) course ,count(*) total from student_courseenrollment where is_active=1 group by course_id) as c on org.org_id=c.course " + collation+" group by org.org_id;"

			
	   		cursor.execute(query)
	   		try:
				org=cursor.fetchall()
				#print cursor.description
				try:
					result=[]
					for row in org:
						result.append([row[0],int(row[1])])
					print result
									
					try:
						#DB close	
						db.close()
						
						return result
					except:
						print "Unable to close : get_organization_registrations"
		
				except:
					print "Unable to Dump to json object : get_organization_registrations"
			except:
				print "Unable to fetch data :get_organization_registrations"
		except:
			print "Unable to execute query : get_organization_registrations"
			#DB close	
			db.close()
	except:
		print "Unable to connect to MYSQL database :get_organization_registrations"
	
	
	

