# IMPORTING DEPENDENCIES

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext,loader
from django.http import HttpResponse
import json
from inputs import DatabaseConfig
import MySQLdb
import math

#IMPORTING CUSTOM APIS
from .apis.dashboard_report import get_organization_registrations 
from .apis.organization_grilldown_report import get_organizationwise_course_enrollments
from .apis.organization_list_report import get_organization_list
from .apis.certificate_summary_report import get_certificate_count



#-----------------------------------------------------------------------------------------------------------------
# PARENT METHOD FOR SUMMARY TAB
def index(request) :
	#print get_organization_registrations_report() 
	
	return render_to_response('ceopanel/index.html',{'data1':json.dumps(get_organization_registrations()),  'data':get_institutewise_cerificates_report()  })

#---------------------------------------------------------------------------------------------------------------------


#-----------------------------------------------------------------------------------------------------------------
# PARENT METHOD FOR ORGANIZATION COURSE ENROLLMENT TAB
def organizationwise_courses_enrollment(request,orgid) :
	organizations= get_organization_list()
	print organizations
	print orgid +" hello"
	return render_to_response('ceopanel/organizationwise_course_enrollment.html',{'data':json.dumps(get_organizationwise_course_enrollments(orgid)) ,'organization_list' : organizations,'org_id' : json.dumps(orgid),'org' :orgid })

#---------------------------------------------------------------------------------------------------------------------





#-----------------------------------------------------------------------------------------------------------------
# PARENT METHOD FOR SUMMARY TAB
'''
def institute_wise(request) :
	return render_to_response('ceopanel/institutewise_certificates_index.html',{'data':get_institutewise_cerificates_report() })
'''
def course_wise(request) :
	InstituteId=str(request.GET.get("InstituteId"))
	organizations= get_organization_list()
	return render_to_response('ceopanel/coursewise_certificates.html',{'data':get_coursewise_cerificates_report(str(InstituteId)),'organization_list' : organizations })

#---------------------------------------------------------------------------------------------------------------------

def get_institutewise_cerificates_report():
	#try:
	db = MySQLdb.connect(DatabaseConfig.MYSQL_HOST,DatabaseConfig.MYSQL_USER,DatabaseConfig.MYSQL_PWD,DatabaseConfig.MYSQL_DB )

	cursor = db.cursor()
	#cursor.execute("select org_id,sum(no_of_verified_certi) verified from (select count(*) no_of_verified_certi,course_id from certificates_generatedcertificate where mode='verified' group by course_id ) a join (select org_id from courseware_organization) b where a.course_id like concat(b.org_id,'%') group by org_id;")
	cursor.execute("select COLLATION_NAME from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='certificates_generatedcertificate' and COLUMN_NAME='course_id';")
	collation1=cursor.fetchall()[0][0]
	cursor.execute("select COLLATION_NAME from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='courseware_organization' and COLUMN_NAME='org_id';")
	collation2=cursor.fetchall()[0][0]
	if(collation1 is collation2):
		collation=''
	else:
		collation='collate '+collation1
	cursor.execute("select b.org_id,sum(a.no_of_verified_certi) verified from (select count(*) no_of_verified_certi,course_id,substring_index(course_id,'/',1) course from certificates_generatedcertificate where mode='verified' group by course_id ) a join (select org_id from courseware_organization) b where a.course = b.org_id "+collation+" group by b.org_id;")
	verified=cursor.fetchall()
	#cursor.execute("select org_id,sum(no_of_honor_certi) honor from (select count(*) no_of_honor_certi,course_id from certificates_generatedcertificate where mode='honor' group by course_id ) a join (select org_id from courseware_organization) b where a.course_id like concat(b.org_id,'%') group by org_id;")
	cursor.execute("select b.org_id,sum(a.no_of_honor_certi) verified from (select count(*) no_of_honor_certi,course_id,substring_index(course_id,'/',1) course from certificates_generatedcertificate where mode='honor' group by course_id ) a join (select org_id from courseware_organization) b where a.course = b.org_id "+collation+" group by b.org_id;")
	honor=cursor.fetchall()
	cursor.execute("select org_id from courseware_organization;")
	all_institutes=cursor.fetchall()
	institutes_list=[]
	for institute in all_institutes:
		institutes_list.append(institute[0])
	honor=dict(honor)
	verified=dict(verified)
	#except:
	#	print "Unable to execute the query"
	institutes=[]
	honor_list=[]
	verified_list=[]
	for key in institutes_list:
		institutes.append(key)
		if key in honor.keys():
			honor_list.append(int(honor[key]))
		else:
			honor_list.append(0)
		if key in verified.keys():
			verified_list.append(int(verified[key]))
		else:
			verified_list.append(0)
	total_list=[institutes,honor_list,verified_list]
	print total_list
	return total_list





def get_coursewise_cerificates_report(institute_id):
	try:
		db = MySQLdb.connect(DatabaseConfig.MYSQL_HOST,DatabaseConfig.MYSQL_USER,DatabaseConfig.MYSQL_PWD,DatabaseConfig.MYSQL_DB )

		cursor = db.cursor()
		cursor.execute("select course_id,count(*) no_of_verified_certi from certificates_generatedcertificate where mode='verified' and  course_id like '"+institute_id+"%' group by course_id;")
		verified=cursor.fetchall()
		cursor.execute("select course_id,count(*) no_of_honor_certi from certificates_generatedcertificate where mode='honor' and  course_id like '"+institute_id+"%' group by course_id;")
		honor=cursor.fetchall()
		cursor.execute("select course_id from certificates_generatedcertificate where course_id like '"+institute_id+"%' group by course_id;")
		all_courses=cursor.fetchall()
		courses_list=[]
		for course in all_courses:
			courses_list.append(course[0])
	except:
		print "Unable to execute the query"
	courses=[]
	honor_list=[]
	verified_list=[]
	honor=dict(honor)
	verified=dict(verified)
	for key in courses_list:
		courses.append(key[len(institute_id)+1:])
		if key in honor.keys():
			honor_list.append(int(honor[key]))
		else:
			honor_list.append(0)
		if key in verified.keys():
			verified_list.append(int(verified[key]))
		else:
			verified_list.append(0)
	total_list=[institute_id,courses,honor_list,verified_list]
	return total_list


	



def fac_first(request):
	db = MySQLdb.connect(DatabaseConfig.MYSQL_HOST,DatabaseConfig.MYSQL_USER,DatabaseConfig.MYSQL_PWD,DatabaseConfig.MYSQL_DB )
	cursor = db.cursor()
	cursor.execute("select course_id from auth_user join student_courseaccessrole where auth_user.id=user_id  group by course_id order by course_id;")
	data=cursor.fetchall()
	institutes=[]
	courses=[]
	for a in data:
		if a[0].split('/')[0] not in institutes:
			institutes.append(a[0].split('/')[0])
		courses.append(a[0])
	return render_to_response('ceopanel/main_index.html',{'data':get_faculty_list_by_institue_and_course('all','all','all',1,100)[1],'institutes':institutes,'selected_institute':'Select Institute','selected_course':'Select Course','page_no':1,'page_count':int(get_faculty_list_by_institue_and_course('all','all','all',1,100)[0]),'per_page':100})
	



def fac_second(request):
	db = MySQLdb.connect(DatabaseConfig.MYSQL_HOST,DatabaseConfig.MYSQL_USER,DatabaseConfig.MYSQL_PWD,DatabaseConfig.MYSQL_DB )
	cursor = db.cursor()
	institute=str(request.GET.get("data").split(',')[0])
	course_id=str(request.GET.get("data").split(',')[1])
	page_no=int(request.GET.get("data").split(',')[2])
	no_of_records=int(request.GET.get("data").split(',')[3])
	print institute
	cursor.execute("select course_id from auth_user join student_courseaccessrole where auth_user.id=user_id  group by course_id order by course_id;")
	data=cursor.fetchall()
	institutes=[]
	courses=[]
	for a in data:
		if a[0].split('/')[0] not in institutes:
			institutes.append(a[0].split('/')[0])
	cursor.execute("select course_id from auth_user join student_courseaccessrole where auth_user.id=user_id  group by course_id order by course_id;")
	data=cursor.fetchall()
	for a in data:
		if str(a[0].split('/')[0]) == str(institute):
			courses.append(a[0])
	if institute == 'all':
		return render_to_response('ceopanel/main_index.html',{'data':get_faculty_list_by_institue_and_course('all','all','all',page_no,no_of_records)[1],'institutes':institutes,'courses':courses,'selected_institute':'Select Institute','selected_course':'Select Course','page_no':page_no,'page_count':int(get_faculty_list_by_institue_and_course('all','all','all',page_no,no_of_records)[0]),'per_page':no_of_records})
	elif course_id == 'all' :
		return render_to_response('ceopanel/main_index.html',{'data':get_faculty_list_by_institue_and_course(institute,'all','all',page_no,no_of_records)[1],'institutes':institutes,'courses':courses,'selected_institute':institute,'selected_course':'Select Course','page_no':page_no,'page_count':int(get_faculty_list_by_institue_and_course(institute,'all','all',page_no,no_of_records)[0]),'per_page':no_of_records})
	else :
		return render_to_response('ceopanel/main_index.html',{'data':get_faculty_list_by_institue_and_course(institute,course_id,'all',page_no,no_of_records)[1],'institutes':institutes,'courses':courses,'selected_institute':institute,'selected_course':course_id,'page_no':page_no,'page_count':int(get_faculty_list_by_institue_and_course(institute,course_id,'all',page_no,no_of_records)[0]),'per_page':no_of_records})
	
	
	

"""==========================================================================================================

This function is to get the faculty list by partner-state and course_id			
	Input :														
		institute_name:Name Of the Institute ex.IITBombayX
		course_id : Course ID
		role: 'staff','beta-testers','instructor'
		page_no    : Page Number
		records_per_page: Number of records per page
	Output:
		A list of two elements
			1.First element will give the number of total pages(in Pagination)
			2.Selcond element is again a list of lists
				->In this each list will contain faculty_name,email,course_id,role,record_number(according to pagination)
	Author : Rajesh Dappu
	email  : rajesh4.ramesh@gmail.com
	Date   : 01-07-2015
		
=========================================================================================================="""
def get_faculty_list_by_institue_and_course(institute_name,course_id,role,page_no,records_per_page):
 	db = MySQLdb.connect(DatabaseConfig.MYSQL_HOST,DatabaseConfig.MYSQL_USER,DatabaseConfig.MYSQL_PWD,DatabaseConfig.MYSQL_DB )
	cursor = db.cursor()
	if role is 'all':
		role_condition=" like '%%' "
	else:
		role_condition="='"+role+"' "
	if institute_name is 'all':
		institute_condition="'%%'"
	else:
		institute_condition="'"+institute_name+"/%'"
	if course_id is 'all':
		course_condition=" like '%%' "
	else:
		course_condition="='"+course_id+"' "
	query_total="select username,course_id,role from auth_user join student_courseaccessrole where auth_user.id=user_id and role"+role_condition+" and course_id"+course_condition+" and course_id like "+institute_condition+" order by username;"
	i=1
	cursor.execute(query_total)
        total=len(cursor.fetchall())
        total_pages=int(math.ceil(float(total)/float(records_per_page)))
        print total_pages
        skip=records_per_page*(page_no-1)
        query="select username,email,course_id,role from auth_user join student_courseaccessrole where auth_user.id=user_id and role"+role_condition+" and course_id"+course_condition+" and course_id like "+institute_condition+" order by course_id limit "+str(skip)+","+str(records_per_page)
        cursor.execute(query)
        data=cursor.fetchall()
        faculty_list=[]
        total_list=[]
        i=skip+1
        total_list.append(total_pages)
        for a in data:
        	array=list(a)
        	array.append(i)
        	i=i+1
        	faculty_list.append(array)
        total_list.append(faculty_list)
        return total_list
	


