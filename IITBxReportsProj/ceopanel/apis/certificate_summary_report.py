#IMPORTING DEPENDENCIES

from inputs import DatabaseConfig

import MySQLdb



# FUNCTION TO GET LIST OF COURSES OF A FACULTY 	
def get_certificate_count():
	try:
		db = MySQLdb.connect(DatabaseConfig.MYSQL_HOST,DatabaseConfig.MYSQL_USER,DatabaseConfig.MYSQL_PWD,DatabaseConfig.MYSQL_DB )
		try:	
			cursor = db.cursor()
			honor_count_query = " select o.org_id,count(c.user_id) from certificates_generatedcertificate c inner join courseware_organization o on c.course_id like concat(o.org_id,"+ "'%'" +") where c.mode=" + "honor" +" group by o.org_id;"
			verified_count_query = " select o.org_id,count(c.user_id) from certificates_generatedcertificate c inner join courseware_organization o on c.course_id like concat(o.org_id," + "'%'" + ") where c.mode=" + "verified" +" group by o.org_id;"
			
	   		cursor.execute(honor_count_query)
	   		try:
				honor=cursor.fetchall()
				
				try:
					verified=cursor.execute(verified_count_query)
				except:
					print "Unable to exeecute  query for verified certificates"
				try:
					result=[]
					for honor_row,verified_row in honor,verified :
						result.append([honor_row[0],int(honor_row[1]),int(verified_row[1])])
					print result
									
					try:
						#DB close	
						db.close()
						
						return result
					except:
						print "Unable to close : get_certificate_count"
		
				except:
					print "Unable to Dump to json object : get_certificate_count"
			except:
				print "Unable to fetch data : get_certificate_count"
		except:
			print "Unable to execute query : get_certificate_count"
			#DB close	
			db.close()
	except:
		print "Unable to connect to MYSQL database : get_certificate_count"
	
	
	

