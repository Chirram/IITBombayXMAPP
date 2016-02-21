"""
Description : This is the main file which calls all the methods of different apis.
Parent Method : index(request,facultyid)
		if the credentials matches with faculty it will redirect to this method
		inputs: facultyid,request
		outputs: render to html page with the outputs of the following methos in json format
			get_discussion_forum(facultyid)
			get_courses_faculty(facultyid)
			getall_courses_grades(facultyid)
Authors : Nitish Deo
	  email: nitishdeo1194@gmail.com
	  
	  Dileep Kumar Dora
	  email: dileepdora.iiit@gmail.com 
Date of Creation : 18/06/2015
"""
# IMPORTING DEPENDENCIES

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext,loader
from django.http import HttpResponse,HttpResponseRedirect
import json
import pymongo
import MySQLdb
from pymongo import MongoClient
from inputs import DatabaseConfig

	
#IMPORTING CUSTOM APIS
from .apis.course_grading_summary_report import getall_course_grades 
from .apis.faculty_course_enrollment_summary_report import get_courses_faculty
from .apis.discussion_forum_summary_report import get_discussion_forum_report
from .apis.course_unanswered_questions_report import get_unanswered_questions_report
from .apis.course_answered_questions_report import get_answered_questions_report
from .apis.course_discussions_report import get_discussions_report
from .apis.course_list_report import get_course_list
from .apis.grades_report import getall_course_grades
from .apis.grades_report import get_course_grades
from .apis.grades_report import getall_student_grades
from .apis.grades_report import get_student_course_grades
from .apis.cohort_report import get_faculty_courses_cohort_count
from .apis.cohort_course_list_report import get_cohort_course_list
from .apis.student_info_report import get_student_course_attendance
from .apis.newapi import get_each_student_grade
from django.contrib.auth.decorators import login_required



def instructor_login_required(f):
        def wrap(request, *args, **kwargs):
                #this check the session if userid key exist, if not it will redirect to login page
                if 'user_id' not in request.session.keys():
                        return HttpResponseRedirect(request.build_absolute_uri('/'))
                elif request.session["usertype"]!="instructor":
                	return HttpResponseRedirect(request.build_absolute_uri('/'))
                return f(request, *args, **kwargs)
        wrap.__doc__=f.__doc__
        wrap.__name__=f.__name__
        return wrap
#-----------------------------------------------------------------------------------------------------------------
# PARENT METHOD FOR SUMMARY TAB
@instructor_login_required
def index(request) :
	facultyid=str(request.session['user_id'])
	print request.session["username"]
	return render_to_response('faculty/index.html',{'data':json.dumps(get_discussion_forum_report(facultyid)) , 'data2':json.dumps(get_courses_faculty(facultyid)), 'data3' :json.dumps(getall_course_grades(facultyid)),'cohort_data':json.dumps(get_faculty_courses_cohort_count(facultyid)), 'fid' : facultyid,'uname': str(request.session["username"])})
	#return HttpResponse(json.dumps(get_discussion_forum_report(facultyid)))

#---------------------------------------------------------------------------------------------------------------------

"""
Description: 	This function  gives all the courses that the given faculty can access
It returns a list containing all the courses no_of_entriesof the faculty
Input: 
1. faculty_id : unique user_id of faculty
Output:
1. courses list : A list of courses which faculty cancrslist access
2. faculty_id   : The faculty id which was given as input

Author		 : 	Mohammed Zubairuddin
Date of creation : 	18/06/2015  
email		 :      wisestofall@gmail.com
ex:['Admin/RDM101/2015_16','IIT_BOBMAY/RDM1031/2014_T1']
"""
@instructor_login_required
def students_of_course(request):
	# Establish database connection and create a handle
	db = MySQLdb.connect(DatabaseConfig.MYSQL_HOST,DatabaseConfig.MYSQL_USER,DatabaseConfig.MYSQL_PWD,DatabaseConfig.MYSQL_DB )  
	cursor = db.cursor()		
        facultyid=str(request.session['user_id'])
	


	#query to get the list of all accessible courses for the given faculty. These couses will be displayed in the drop-down menu
	crslist_query="select DISTINCT course_id from student_courseaccessrole where user_id="+facultyid+" and role='instructor' ;";		
	try:	
		
		# Execute SQL query and Fetch the courses list
		cursor.execute(crslist_query)
		crslist = cursor.fetchall()	
		#return courselist and faculty_id to be used on the html page
		
		#close database connection
		db.close()	#Kill the boy
		
		print request.session["username"]
		return render_to_response('faculty/students_of_course.html',{'crslist': crslist , 'fid': facultyid,'uname': str(request.session["username"])})
	except:
		print "Error: Unable to fetch data111" #Something is terribly wrong 	



"""
Description: 	This function returns the list of the student of a given course
It also returns a list containing all the courses the faculty can access. This list will be displayed in the drop-down menu
Input: 
1. faculty_id : unique user_id of faculty
2. Full course name : Organization name, coursename, semester
Output:
1. student list : A list of students of the given course
2. courses list : A list of courses which faculty can access
3. faculty_id   : The faculty id which was given as input
4. Total_records : Total No. of records
5. Page_No	 : The page number which was given as input
6. No_of_entries : The number of entries which was given as input

Author		 : 	Mohammed Zubairuddin
Email		 :      wisestofall@gmail.com
Date of creation : 	18/06/2015  
"""


#If this comment is removed, the program will blow up
@instructor_login_required
def students_of_course_result_display(request,orgname,coursename,semester,page_no,no_of_entries,search):
	faculty_id=str(request.session['user_id'])	
	#Removes extra trailing slashes(/) from the 'faculty_id'. Sometimes they comes along with the input
	# Don't mind these lines, you wont get it. It's an internal operation, just move on
	index=faculty_id.find('/',0,len(faculty_id))
	if(index!=-1):
		faculty_id=faculty_id[0:index]
	cname=orgname+"/"+coursename+"/"+semester;

	# Establish database connection and create two cursor object
	db = MySQLdb.connect(DatabaseConfig.MYSQL_HOST,DatabaseConfig.MYSQL_USER,DatabaseConfig.MYSQL_PWD,DatabaseConfig.MYSQL_DB )	
	cursor = db.cursor()
	cursor1 = db.cursor()
	cursor2 = db.cursor()
	
	# verify whether the user is authorization over the course
	validation_query="SELECT count(*) as count FROM student_courseaccessrole WHERE course_id='"+cname+"' and user_id="+faculty_id+" and (role='instructor' or role='staff')";
	try:
		# Execute SQL query and fetch the data
		cursor.execute(validation_query)
		data = cursor.fetchall()	
		count=data[0][0]

		########################################	This is a well commented line!		

		if(count==0): # user is not authorized to access the course
			print "Error! Not Authorized! "
			return render_to_response('mis/students_of_course_result_display.html', {'data':(), 'cname':'Unauthorized Access!','total_records':0, 'crslist': (),'fac_id':faculty_id,'page_no':page_no, "total_pages": 0,"no_of_entries":no_of_entries,"search":""})
		else:	# user is authorized to access the course details
			# A little bit of calculations for pagination process. if you dont get it, just move on
			count_records_query="";
			if(search=="$$$"):
				print "$$$"		
				count_records_query="select count(*) as count from student_courseenrollment where course_id='"+cname+"' and is_active=1;";
			else :
				# search query
				count_records_query="""SELECT count(*) FROM (SELECT Table2.user_id, Table2.username, auth_userprofile.name FROM auth_userprofile RIGHT JOIN (SELECT Table1.user_id, auth_user.username FROM auth_user INNER JOIN (SELECT user_id FROM student_courseenrollment WHERE course_id = '"""+cname+"""' AND is_active=1) AS Table1 ON auth_user.id=Table1.user_id) As Table2 ON Table2.user_id=auth_userprofile.user_id) AS Table3 WHERE (Table3.user_id LIKE '%"""+search+""""%' OR Table3.username LIKE '%"""+search+"""%' OR Table3.name LIKE '%"""+search+"""%');""";
				
			total_records=0;
			try:		
				cursor2.execute(count_records_query)
				count_records = cursor2.fetchall()	
				total_records=count_records[0][0];
			except:
				print "unable to fetch data :: breaking point-1 "#This should never happen

			print total_records;

			#you are not meant to understand this. Just remember that it calculates offset to be used in sql for pagination	
			offset=0;			
			total_pages=1;
			if(no_of_entries>total_records):	
				total_pages=-(-(int(total_records))/(int(no_of_entries)))
				offset=int(no_of_entries)*(int(page_no)-1);
				if(offset>total_records):
					offset=0
					page_no=1
						
			# query to get the list of the courses user can access inorder to display it in the drop-down menu
			courses_list_query="select DISTINCT course_id from student_courseaccessrole where user_id='"+faculty_id+"' and (role='instructor' );";
			query="""""";
			# query to get the list of students of the course
			if(search=="$$$"):	
				query = """SELECT Table2.user_id, Table2.username, auth_userprofile.name FROM auth_userprofile RIGHT JOIN (SELECT Table1.user_id, auth_user.username FROM auth_user INNER JOIN (SELECT user_id FROM student_courseenrollment WHERE course_id = '"""+cname+"""' AND is_active=1 ORDER BY user_id LIMIT """+str(no_of_entries)+""" OFFSET """+str(offset)+""") AS Table1 ON auth_user.id=Table1.user_id) As Table2 ON Table2.user_id=auth_userprofile.user_id ORDER BY Table2.username""";
			else:
					
				query="""SELECT Table3.user_id,Table3.username, Table3.name FROM (SELECT Table2.user_id, Table2.username, auth_userprofile.name FROM auth_userprofile RIGHT JOIN (SELECT Table1.user_id, auth_user.username FROM auth_user INNER JOIN (SELECT user_id FROM student_courseenrollment WHERE course_id = '"""+cname+"""' AND is_active=1) AS Table1 ON auth_user.id=Table1.user_id) As Table2 ON Table2.user_id=auth_userprofile.user_id) AS Table3 WHERE (Table3.user_id LIKE '%"""+search+""""%' OR Table3.username LIKE '%"""+search+"""%' OR Table3.name LIKE '%"""+str(search)+"""%') ORDER BY Table3.username LIMIT """+str(no_of_entries)+""" OFFSET """+str(offset)+""";""";	
			try:
				
				# Execute SQL queries and fetch the courses list
				cursor1.execute(courses_list_query)
				crslist = cursor1.fetchall()
				cursor.execute(query)		
				data = cursor.fetchall()
				ar=str(cname).split("/")
				c_id=ar[1]
				grades_list=[]
				for i in data:
					
					stud_grade=round(get_student_course_grades(str(i[0]),c_id),2)
					print "here"
					if stud_grade== -1:
						stud_grade="NA"
					grades_list.append([str(i[0]),str(i[1]),str(i[2]),stud_grade])	
				# return the course list, student list, total count, faculty id

				return render_to_response('faculty/students_of_course_result_display.html', {'data':grades_list,'grades_list':grades_list,'cname':cname,'total_records':total_records, 'crslist': crslist,'fac_id':faculty_id,'page_no':page_no, 'total_pages': total_pages, 'no_of_entries':no_of_entries,"search":search,'uname': str(request.session["username"]),'coursename' :coursename,'orgname':orgname,'semester' :semester})
			except:
				print "Error: Unable to fetch data :: breaking point-2"	# Something's gone crazy
				
	except:
		print "Error: Unable to fetch data :: breaking point-3"	#If this happens, then prepare yourself for the wrost 
	# Disconnect from server	
	db.close()

		
#-----------------------------------------------------------------------------------------------------------------
# PARENT METHOD FOR DISCUSSION FORUM DETAILED REPORT TAB : unanswered questions
"""
Description: 	This method calls the get_unanswered_questions_report(facultyid,course) 
		and takes the output from there and renders to course_unanswered_questions_report.html page
Input: 
1. facultyid : unique user_id of faculty
2. request : Http Request from webpage

Output:
	course_list : List of all courses for a faculty
	output of method get_unsanswered_questions_report(faculty,course) i.e list of unanswered questions for a course
	 
Author		 : 	Nitish Deo
			email:nitishdeo1194@gmail.com
Date of creation : 	18/06/2015  
"""
def course_unanswered_questions(request) :
	facultyid=str(request.session['user_id'])
        #python list containing all the courses
        course_list=get_course_list(facultyid)
        if request.method == 'POST':
        	course =str(request.POST.get('courseid'))
        	courseid=course.split('/')[1]
        	      	
        else:
      		course = ""
      		courseid=""
        print course
	return render_to_response('faculty/course_unanswered_questions_report.html',{'data':get_unanswered_questions_report(facultyid,course) ,'course_list' : course_list, 'fid' : facultyid, 'uname': str(request.session["username"]),'crs': course,'courseid':courseid })



#-----------------------------------------------------------------------------------------------------------------
# PARENT METHOD FOR DISCUSSION FORUM DETAILED REPORT TAB : discussions 
"""
Description: 	This method calls the get_discussion_report(facultyid,course) 
		and takes the output from there and renders to course_discussions_report.html page
Input: 
1. facultyid : unique user_id of faculty
2. request : Http Request from webpage

Output:
	course_list : List of all courses for a faculty
	output of method get_discussion_report(faculty,course) i.e list of discussions for a course
	 
Author		 : 	Nitish Deo
			email:nitishdeo1194@gmail.com
Date of creation : 	18/06/2015  
"""
@instructor_login_required
def course_discussions(request) :
	facultyid=str(request.session['user_id'])
        #python list containing all the courses
        course_list=get_course_list(facultyid)
        if request.method == 'POST':
        	course =str(request.POST.get('courseid'))
        	courseid=course.split('/')[1]
        	      	
        else:
      		course = ""
      		courseid=""
	return render_to_response('faculty/course_discussions_report.html',{'data':get_discussions_report(facultyid,course) ,'course_list' : course_list, 'fid' : facultyid,'uname': str(request.session["username"]),'crs': course,'courseid' :courseid })

#---------------------------------------------------------------------------------------------------------------------
# PARENT METHOD FOR DISCUSSION FORUM DETAILED REPORT TAB : answered questions 
"""
Description: 	This method calls the get_answered_questions_report(facultyid,course) 
		and takes the output from there and renders to course_answered_questions_report.html page
Input: 
1. facultyid : unique user_id of faculty
2. request : Http Request from webpage

Output:
	course_list : List of all courses for a faculty
	output of method get_answered_questions_report(faculty,course) i.e list of answered questions for a course
	 
Author		 : 	Nitish Deo
			email:nitishdeo1194@gmail.com
Date of creation : 	18/06/2015  
"""
@instructor_login_required
def course_answered_questions(request) :
	facultyid=str(request.session['user_id'])
        #python list containing all the courses
        course_list=get_course_list(facultyid)
        if request.method == 'POST':
        	course =str(request.POST.get('courseid'))
        	courseid=course.split('/')[1]
        	     	
        else:
      		course = ""
      	        courseid=""
	return render_to_response('faculty/course_answered_questions_report.html',{'data':get_answered_questions_report(facultyid,course) ,'course_list' : course_list, 'fid' : facultyid,'uname': str(request.session["username"]),'crs': course,'courseid':courseid })



#-----------------------------------------------------------------------------------------------------------------
# PARENT METHOD FOR SECOND LEVEL GRADE REPORT
@instructor_login_required
def students_grade_courselevel(request,courseid) :
	
	facultyid=str(request.session['user_id'])
	course_list=get_course_list(facultyid)
        
        if courseid == 'selectcourse':
        	courseid=course_list[1].split('/')[1]
        	
        (newlist1,newlist2)=getall_student_grades(courseid)
	#if len(newlist2)==0:	
		#return HttpResponse("This course does not have grading policy defined")
	return render_to_response('faculty/courselevel_grades.html',{'data':newlist1,'data1':newlist2 ,'courseid' : courseid ,'fid' : facultyid ,'uname': str(request.session["username"]),'course_list' : course_list})

#-----------------------------------------------------------------------------------------------------------------
# PARENT METHOD FOR THIRD LEVEL GRADE REPORT
@instructor_login_required
def students_grade_attendence(request,course_id,student_id) :
	facultyid=str(request.session['user_id'])
        print course_id+"hhjjgfgg"
        print student_id+"kkk"
        course=course_id.split('/')[1]
	attendance=get_student_course_attendance(str(student_id),course_id)
	per=((float(attendance[0]))/attendance[1])*100
	per=str(round(per,2))	
	return render_to_response('faculty/quizlevel_grades.html',{'data':json.dumps(get_each_student_grade(str(student_id),course)) ,'attendance_dict':attendance,'fid' : facultyid ,'uname': str(request.session["username"]),'course':course,'sid':student_id,'per':per})
	
	
@instructor_login_required
def cohort_details(request):
	facultyid=request.session["user_id"]
	db = MySQLdb.connect(DatabaseConfig.MYSQL_HOST,DatabaseConfig.MYSQL_USER,DatabaseConfig.MYSQL_PWD,DatabaseConfig.MYSQL_DB )
	cursor=db.cursor()
	print request.GET.get("course_id")
	querystr="select name,count(a.id),a.id no_of_students from (select id,name from course_groups_courseusergroup where group_type='cohort' and course_id='"+str(request.GET.get("course_id"))+"') a inner join course_groups_courseusergroup_users b on a.id=b.courseusergroup_id group by name;"
	cursor.execute(querystr)
	data=cursor.fetchall()
	db.close()
	print data
	cohort_count=[]
	cohort_names=[]
	cohort_group_ids=[]
	cohort_discussion_details=[]
	cohort_total=[]
	cohort_discussions=[]
	cohort_answered=[]
	cohort_unanswered=[]
	for key in data:
		cohort_names.append(key[0])
		cohort_count.append(int(key[1]))
		cohort_group_ids.append(int(key[2]))
	cohort_details=[cohort_names,cohort_count,cohort_group_ids]
	client = MongoClient(DatabaseConfig.MONGO_HOST, DatabaseConfig.MONGO_PORT)
	discussion_db=discussion_db = client.cs_comments_service_development
	discussion_coll = discussion_db.contents
	for i in range(len(cohort_group_ids)):
		index=cohort_group_ids[i]
		total= discussion_coll.find({"_type" : "CommentThread" , "course_id" : request.GET.get("course_id"),"group_id":index}).count()
		questions = discussion_coll.find({"_type" : "CommentThread" , "course_id" : request.GET.get("course_id"),"thread_type" : "question","group_id":index}).count()
		discussions = discussion_coll.find({"_type" : "CommentThread" , "course_id" : request.GET.get("course_id"),"thread_type" : "discussion","group_id":index}).count()
        	unanswered_questions = discussion_coll.find({"_type" : "CommentThread" , "thread_type" : "question","comment_count" : 0 , "course_id" : request.GET.get("course_id"),"group_id":index}).count()
		answered_questions=questions-unanswered_questions
		cohort_total.append(total)
		cohort_discussions.append(discussions)
		cohort_answered.append(answered_questions)
		cohort_unanswered.append(unanswered_questions)
		cohort_discussion_details=[cohort_group_ids,cohort_names,cohort_total,cohort_discussions,cohort_answered,cohort_unanswered]
	print cohort_discussion_details
	client.close()
	print facultyid
	cohort_course_list=get_cohort_course_list(facultyid)
	print cohort_course_list
	return render_to_response('faculty/course_cohort_students_count.html',{'cohort_details':cohort_details,'cohort_discussion_details':cohort_discussion_details,'fid': facultyid,'uname': str(request.session["username"]) , 'course_list' : cohort_course_list})
	
@instructor_login_required
def cohort_detailed_discussions(request):
	facultyid=request.session["user_id"]
	client = MongoClient(DatabaseConfig.MONGO_HOST, DatabaseConfig.MONGO_PORT)
	discussion_db=discussion_db = client.cs_comments_service_development
	discussion_coll = discussion_db.contents
	unans_ques = discussion_coll.find({"_type" : "CommentThread" ,"group_id":int(request.GET.get("cohort_group_id")), "thread_type" : "discussion" } , {"body" : 1,"title" : 1})
	result=[]
	for i in unans_ques:
		result.append([i['title'],i['body']])
	client.close()			
	print result
	return render_to_response('faculty/cohort_discussions_report.html',{'data':result,'fid': facultyid,'uname': str(request.session["username"])})
	#return HttpResponse(request.GET.get("cohort_group_id"))
@instructor_login_required
def cohort_detailed_answered(request):
	facultyid=request.session["user_id"]
	client = MongoClient(DatabaseConfig.MONGO_HOST, DatabaseConfig.MONGO_PORT)
	discussion_db=discussion_db = client.cs_comments_service_development
	discussion_coll = discussion_db.contents
	unans_ques = discussion_coll.find({"_type" : "CommentThread" ,"group_id":int(request.GET.get("cohort_group_id")), "thread_type" : "question" , "comment_count" : {"$gt" : 0 }} , {"body" : 1,"title" : 1})
	result=[]
	for i in unans_ques:
		result.append([i['title'],i['body']])
	client.close()			
	print result
	return render_to_response('faculty/cohort_answered_questions_report.html',{'data':result,'fid': facultyid,'uname': str(request.session["username"])})
	#return HttpResponse(request.GET.get("cohort_group_id"))
@instructor_login_required
def cohort_detailed_unanswered(request):
	facultyid=request.session["user_id"]
	client = MongoClient(DatabaseConfig.MONGO_HOST, DatabaseConfig.MONGO_PORT)
	discussion_db=discussion_db = client.cs_comments_service_development
	discussion_coll = discussion_db.contents
	unans_ques = discussion_coll.find({"_type" : "CommentThread" ,"group_id":int(request.GET.get("cohort_group_id")), "thread_type" : "question" , "comment_count" : 0} , {"body" : 1,"title" : 1})
	result=[]
	for i in unans_ques:
		result.append([i['title'],i['body']])
	client.close()			
	print result
	return render_to_response('faculty/cohort_unanswered_questions_report.html',{'data':result,'fid': facultyid,'uname': str(request.session["username"])})
	#return HttpResponse(request.GET.get("cohort_group_id"))	

@instructor_login_required
def cohort_students_list(request):
	facultyid=request.session["user_id"]
	db = MySQLdb.connect(DatabaseConfig.MYSQL_HOST,DatabaseConfig.MYSQL_USER,DatabaseConfig.MYSQL_PWD,DatabaseConfig.MYSQL_DB )
	cursor=db.cursor()
	query="select user_id,username,email from (select user_id from course_groups_courseusergroup_users where courseusergroup_id="+request.GET.get("cohort_group_id")+") a inner join auth_user b on a.user_id=b.id;"
	cursor.execute(query)
	result=cursor.fetchall()
	print result
	studentlist=[]
	db.close()
	return render_to_response('faculty/cohort_list.html',{'data':result,'fid': facultyid,'uname': str(request.session["username"])})
	
