from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
import MySQLdb
from collections import OrderedDict
import cStringIO as StringIO
#import ho.pisa as pisa
from django.template.loader import get_template
from django.template import Context,RequestContext,loader
from django.http import HttpResponse
from cgi import escape
from DatabaseConfig import DatabaseConfiguration

DATABASE=DatabaseConfiguration.DATABASE_NAME
USER=DatabaseConfiguration.USERNAME
PASSWORD=DatabaseConfiguration.PASSWORD
HOST=DatabaseConfiguration.HOST
PORT=DatabaseConfiguration.PORT

"""==========================================================================================================

The below function is to get the student's count by Gender				
	Input :	
	 	username: MySQL's Username
		db_name : Database's name
		password: MySQL database's Password
		host    : Host Address
	Output:
		Keys	:  Gender Category name
		values	:  Student's count
	Author : Rajesh Dappu
	email  : rajesh4.ramesh@gmail.com
	Date   : 18-06-2015
		
=========================================================================================================="""
def get_student_count_by_gender(username,db_name,password,host):
	try:
		db=MySQLdb.connect(user=username,db=db_name,passwd=password,host=host)	#connection to the MySQL Database
		cursor=db.cursor()
   		cursor.execute('select table1.gender, count(*) as no_students from (select gender from auth_userprofile where gender is not NULL) as table1 group by gender order by no_students desc;')				#Executing the MySQL Query
		student_count_by_gender=cursor.fetchall()				#fetching the data
	except:
   		print "Error: Unable to fetch data"					
	db.close()									#Closing the connection
	student_count_by_gender=dict(student_count_by_gender)				#converting the tuple into dictionary
	for key in student_count_by_gender.keys():
		student_count_by_gender[key]=int(student_count_by_gender[key])		#converting 'long' format to 'int' 
	return student_count_by_gender
	
	
	
	
"""==========================================================================================================

The below function is to get the student's count by a particular Gender Category name				
	Input :		
		gender: gender_id {Ex : f,m,o}	
	 	username: MySQL's Username
		db_name : Database's name
		password: MySQL database's Password
		host    : Host Address
	Output:
		Percentage of students for that particular gender category
	Author : Rajesh Dappu
	email  : rajesh4.ramesh@gmail.com
	Date   : 18-06-2015
		
=========================================================================================================="""
def get_student_percentage_by_gender_name(gender,username,db_name,password,host):
	try:
		db=MySQLdb.connect(user=username,db=db_name,passwd=password,host=host)	#connection to the MySQL Database
		cursor=db.cursor()
   		cursor.execute('select count(*) from auth_userprofile')			#Executing the MySQL Query
		total=cursor.fetchall()
	except:
   		print "Error: Unable to fetch data"
	total_students=float(total[0][0])						#converting 'long' format to 'float'
	try:
   		cursor.execute('select count(*)  from auth_userprofile where gender=\''+gender+'\';')
		students_with_specified_gender=cursor.fetchall()
	except:
   		print "Error: Unable to fetch data"
	
	students_with_specified_gender=float(students_with_specified_gender[0][0])	#converting 'long' format to 'float'
	percentage=(students_with_specified_gender*100)/total_students;			#calculating the percentage
	db.close()									#closing the connection
	return percentage
	
	
	
	
	
"""==========================================================================================================

The below function is to get the student's count by state				
	Input :		
	 	username: MySQL's Username
		db_name : Database's name
		password: MySQL database's Password
		host    : Host Address
	Output:
		Keys	:  state names
		values	:  Student's count
	Author : Rajesh Dappu
	email  : rajesh4.ramesh@gmail.com
	Date   : 18-06-2015
		
=========================================================================================================="""
def get_student_count_by_state(username,db_name,password,host):	
	try:
		db=MySQLdb.connect(user=username,db=db_name,passwd=password,host=host)	#connection to the MySQL Database
		cursor=db.cursor()
		cursor.execute('select table1.name as name, count(*) as no_students from (select name from student_mooc_person  JOIN student_mooc_state where student_mooc_person.state_id=student_mooc_state.id ) as table1 group by name order by no_students desc;')
											#Executing the MySQL Query
		states=cursor.fetchall()
	except:
   		print "Error: Unable to fetch data"
	db.close()
	states=dict(states)								#converting the tuple into dictionary
	for key in states.keys():
		states[key]=int(states[key])						#converting 'long' format to 'int' 
	return states




"""==========================================================================================================

The below function is to get the student's count by for particular state				
	Input :		
		state_id: state's id	
	 	username: MySQL's Username
		db_name : Database's name
		password: MySQL database's Password
		host    : Host Address
	Output:
		Number of students for that particular state
	Author : Rajesh Dappu
	email  : rajesh4.ramesh@gmail.com
	Date   : 18-06-2015
		
=========================================================================================================="""
def get_student_count_by_state_id(state_id,username,db_name,password,host):	
	try:							
		db=MySQLdb.connect(user=username,db=db_name,passwd=password,host=host)	#connection to the MySQL Database
		cursor=db.cursor()
		query="select count(*) from student_mooc_person where state_id="+str(state_id)
		cursor.execute(query)							#Executing the MySQL Query
		data=cursor.fetchall()
	except:
		print "Error: Unable to fetch data"
	no_of_students=int(data[0][0])							#converting 'long' format to 'int' 
	db.close()
	return no_of_students
	
	
	
"""==========================================================================================================

The below function is to get the student's count by their education				
	Input :			
	 	username: MySQL's Username
		db_name : Database's name
		password: MySQL database's Password
		host    : Host Address
	Output:
		A Dictionary Which contains,
			Keys	:  education category names [p, m, b, a, hs, jhs, el, none, other, p_se, p_oth]
			values	:  Student's count
	Author : Rajesh Dappu
	email  : rajesh4.ramesh@gmail.com
	Date   : 18-06-2015
		
=========================================================================================================="""

def get_student_count_by_level_of_education(username,db_name,password,host):						
	try:
		db=MySQLdb.connect(user=username,db=db_name,passwd=password,host=host)	#connection to the MySQL Database
		cursor=db.cursor()
		cursor.execute('select table1.level_of_education, count(*) as no_students from (select level_of_education from auth_userprofile where level_of_education is not NULL) as table1 group by level_of_education order by no_students desc;')
											#Executing the MySQL Query
		student_count_by_level_of_education=cursor.fetchall()
	except:
   		print "Error: Unable to fetch data"
	db.close()									#closing the connection
	student_count_by_level_of_education=dict(student_count_by_level_of_education)	#converting the tuple into dictionary
	for key in student_count_by_level_of_education.keys():
		student_count_by_level_of_education[key]=int(student_count_by_level_of_education[key])
											#converting 'long' format to 'int' 
	return student_count_by_level_of_education




"""==========================================================================================================

The below function is to get the student's count for particular education category			
	Input :			
		level_of_education : possible inputs are p, m, b, a, hs, jhs, el, none, other, p_se, p_oth 				    			username: MySQL's Username
		db_name : Database's name
		password: MySQL database's Password
		host    : Host Address
	Output:
		Number of students in that particular education category
	Author : Rajesh Dappu
	email  : rajesh4.ramesh@gmail.com
	Date   : 18-06-2015
		
=========================================================================================================="""
def get_student_count_by_level_of_education_id(level_of_education,username,db_name,password,host):	
	try:
		db=MySQLdb.connect(user=username,db=db_name,passwd=password,host=host)	#connection to the MySQL Database
		cursor=db.cursor()
		cursor.execute('select count(*) from auth_userprofile where level_of_education=\''+level_of_education+'\';')
											#Executing the MySQL Query
		no_of_students=cursor.fetchall()
	except:
   		print "Error: Unable to fetch data"
   		
	db.close()									#closing the connection
	no_of_students=int(no_of_students[0][0])					#converting 'long' format to 'int' 
	return no_of_students
	


"""==========================================================================================================

This function is to get the student's count by Age category				
	Input :														
		username: MySQL's Username
		db_name : Database's name
		password: MySQL database's Password
		host    : Host Address
	Output:
		A Dictionary Which contains,
			Keys	:  Age Categories
			values	:  Student count
		Example:{"less than 15":45,"15 to 25":12,"25 to 40":10,"40 to 60":12,"greater than 60":11}
	Author : Rajesh Dappu
	email  : rajesh4.ramesh@gmail.com
	Date   : 18-06-2015
		
=========================================================================================================="""
def get_student_age_category_list(username,db_name,password,host):
	import datetime									#
	now=datetime.datetime.now()							# Extracting present Year
	year=now.year									#
	try:
		db=MySQLdb.connect(user=username,db=db_name,passwd=password,host=host)	#connection to the MySQL Database
		cursor=db.cursor()
		cursor.execute('select year_of_birth from auth_userprofile where year_of_birth is not NULL;')
											#Executing the MySQL Query
		data=cursor.fetchall()
	except:
   		print "Error: Unable to fetch data"
   	students_by_age={"less than 15":0,"15 to 25":0,"26 to 40":0,"41 to 60":0,"greater than 60":0}
   	for ele in data:								
   		if ((year-int(ele[0]))>=0 and (year-int(ele[0]))<15):
   			students_by_age["less than 15"]=students_by_age["less than 15"]+1
   		elif ((year-int(ele[0]))>=15 and (year-int(ele[0]))<=25):
   			students_by_age["15 to 25"]=students_by_age["15 to 25"]+1
   		elif ((year-int(ele[0]))>25 and (year-int(ele[0]))<=40):
   			students_by_age["26 to 40"]=students_by_age["26 to 40"]+1
   		elif ((year-int(ele[0]))>40 and (year-int(ele[0]))<=60):
   			students_by_age["41 to 60"]=students_by_age["41 to 60"]+1
   		elif (year-int(ele[0]))>60:
   			students_by_age["greater than 60"]=students_by_age["greater than 60"]+1
	db.close()									#closing the connection
	return  students_by_age



"""==========================================================================================================

This function is to get the student's count by subject				
	Input :														
		username: MySQL's Username
		db_name : Database's name
		password: MySQL database's Password
		host    : Host Address
	Output:
		A Dictionary Which contains,
			Keys	:  Subject names
			values	:  Student count
		Example:{"Computer Science":12,"Maths":2}
	Author : Rajesh Dappu
	email  : rajesh4.ramesh@gmail.com
	Date   : 18-06-2015
		
=========================================================================================================="""
def get_student_count_by_subject(username,db_name,password,host):
	try:
		db=MySQLdb.connect(user=username,db=db_name,passwd=password,host=host)	#connection to the MySQL Database
		cursor=db.cursor()
		cursor.execute("select b.subject_name,SUM(no_of_students) as number_of_students from (select course_id, count(*) as no_of_students from student_courseenrollment group by course_id) a join (select subject_name,course_id  from  courseware_course_subject join courseware_subject where courseware_subject.id=courseware_course_subject.subject_id order by subject_name) b where a.course_id=b.course_id group by b.subject_name;")
											#Executing the MySQL Query
		sub_wise_student_count=cursor.fetchall()
	except:
   		print "Error: Unable to fetch data"
   	sub_wise_student_count=dict(sub_wise_student_count)
   	for key in sub_wise_student_count.keys():
   		sub_wise_student_count[key]=int(sub_wise_student_count[key])
	db.close()									#closing the connection
	return sub_wise_student_count
	







"""==========================================================================================================

This function is to get the courses list by subject				
	Input :														
		username: MySQL's Username
		db_name : Database's name
		password: MySQL database's Password
		host    : Host Address
	Output:
		A list of lists,
			1.Each list will contains 3 elements
			2.These are Subject name,Course ID, Course Name
		Example:[['Computer Science','IITBombayX/TCS101x/2015-16','Teacher CS'],['Maths','JournalistX/IM10/2015_IM','Introduction to Indian Media']]
	Author : Rajesh Dappu
	email  : rajesh4.ramesh@gmail.com
	Date   : 18-06-2015
		
=========================================================================================================="""
def get_course_list_by_subject(username,db_name,password,host):
	try:
		db=MySQLdb.connect(user=username,db=db_name,passwd=password,host=host)	#connection to the MySQL Database
		cursor=db.cursor()
		cursor.execute("select subject_name,course_id,course_name  from  courseware_course_subject join courseware_subject where courseware_subject.id=courseware_course_subject.subject_id order by subject_name;")
											#Executing the MySQL Query
		sub_wise_courses_tuple=cursor.fetchall()
	except:
   		print "Error: Unable to fetch data"
   	sub_wise_courses_list=[]
   	for ele in sub_wise_courses_tuple:	
   		sub_wise_courses_list.append(list(ele))
	db.close()									#closing the connection
	return sub_wise_courses_list





"""==========================================================================================================

This function is to get the list of subject names			
	Input :														
		username: MySQL's Username
		db_name : Database's name
		password: MySQL database's Password
		host    : Host Address
	Output:
		A sorted list of Subject names ,
		Example:['Computer Science','Maths']
	Author : Rajesh Dappu
	email  : rajesh4.ramesh@gmail.com
	Date   : 18-06-2015
		
=========================================================================================================="""
def get_subject_list(username,db_name,password,host):
	try:
		db=MySQLdb.connect(user=username,db=db_name,passwd=password,host=host)	#connection to the MySQL Database
		cursor=db.cursor()
		cursor.execute("select subject_name  from  courseware_course_subject join courseware_subject where courseware_subject.id=courseware_course_subject.subject_id group by subject_name;")		#Executing the MySQL Query
		sub_list_tuple=cursor.fetchall()
	except:
   		print "Error: Unable to fetch data"
   	sub_list=[]
   	for key in sub_list_tuple:
   		sub_list.append(key[0])
   	sub_list.sort()
	db.close()									#closing the connection
	return sub_list

	
	
def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html  = template.render(context)
    result = StringIO.StringIO()
    #print context
    #print result
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")), result)
    #print result.getvalue()
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))

def myview(request):
    title='Statewise Distribution of Students'
    return render_to_pdf(
        'convert_to_pdf.html',
        {
            'pagesize':'A4',
            'mylist': get_student_count_by_state(USER,DATABASE,PASSWORD,HOST),
	    'title': title,
        }
    )
def genderwise(request):
	return render(request,'theme/gender.html',{'student_count_by_gender':get_student_count_by_gender(USER,DATABASE,PASSWORD,HOST)})
def statewise(request):
	return render(request,'theme/by_state.html',{'student_count_by_state':get_student_count_by_state(USER,DATABASE,PASSWORD,HOST)})
def educationwise(request):
	return render(request,'theme/by_level_of_education.html',{'student_count_by_level_of_education':get_student_count_by_level_of_education(USER,DATABASE,PASSWORD,HOST)})
def agewise(request):
	return render(request,'theme/age.html',{'student_list_by_age':get_student_age_category_list(USER,DATABASE,PASSWORD,HOST)})
def index(request):
	return render(request,'theme/index.html',{'student_count_by_level_of_education':get_student_count_by_level_of_education(USER,DATABASE,PASSWORD,HOST),'student_list_by_age':get_student_age_category_list(USER,DATABASE,PASSWORD,HOST),'student_count_by_gender':get_student_count_by_gender(USER,DATABASE,PASSWORD,HOST),'student_count_by_state':get_student_count_by_state(USER,DATABASE,PASSWORD,HOST)})



def subjectwise(request):
	return render(request,'theme/subject.html',{'subwise_courses_list':get_course_list_by_subject(USER,DATABASE,PASSWORD,HOST),'subwise_student_count':get_student_count_by_subject(USER,DATABASE,PASSWORD,HOST),'subject_list':get_subject_list(USER,DATABASE,PASSWORD,HOST)})

