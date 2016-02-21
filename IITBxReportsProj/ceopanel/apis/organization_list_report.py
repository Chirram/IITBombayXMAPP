#IMPORTING DEPENDENCIES

from inputs import DatabaseConfig
import MySQLdb



# FUNCTION TO GET LIST OF COURSES OF A FACULTY 	
def get_organization_list():
	try:
		db = MySQLdb.connect(DatabaseConfig.MYSQL_HOST,DatabaseConfig.MYSQL_USER,DatabaseConfig.MYSQL_PWD,DatabaseConfig.MYSQL_DB )
	except:
		print "Unable to connect to MYSQL database : get_organization_list"
	try:	
		cursor = db.cursor()
		query = "select org_id from courseware_organization"
		cursor.execute(query)
	except:
		print "Unable to execute query : get_organization_list"
	try:
		results = cursor.fetchall()
	except:
		print "Unable to fetch data : get_organization_list"
	try:
		organizations=[]
		for row in results:
			 organizations.append(str(row[0]))
		#print courses
	except:
		print "Unable to Dump to json object : get_organization_list"
	try:
		#DB close	
		db.close()
		return organizations
	except:
		print "Unable to respond : get_organization_list"
	

