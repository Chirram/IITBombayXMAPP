#!/usr/bin/python
from django.shortcuts import render_to_response
from django.http import HttpResponse
from pymongo import MongoClient
from inputs import DatabaseConfig
import json
import MySQLdb
#####Grades imports
from django.shortcuts import render
from django.template import RequestContext,loader
from django.utils.safestring import mark_safe
import pymongo			
'''
DatabaseConfig.MYSQL_HOST="10.105.24.33"
DatabaseConfig.MONGO_PORT=27017
DatabaseConfig.MYSQL_USER="root"
DatabaseConfig.MYSQL_PASSWORD="edx"
database="edxapp"'''




#only used while logging in to insert cookie and functionality is same as get_student_all_courses_attendance().
'''
	Description: This function is to find the attendance of a student in all courses
	Input parameters:
	request : It is an http request sent from the browser 
	student_id : unique user_id of student
	Output:
	response: response object containing attendance dictionary rendered in student_dash.html
	Author:
	Chirram Kumar and Devesh Kumar
	e-mail:chkumariiit123@gmail.com
	Date of creation:
	18/06/2015  
	attendance dictionary:{"CS101":[22,226],"CS742":[5,44]} -- student has completed 22 components out of 226 in the course CS101
'''
def student_home(request):
	
	student_id=str(request.session["user_id"])
	#print student_id
	try:
		course_list=get_student_enrolled_courses(student_id)   		#Get all courses enrolled by student as a list
	except Exception,err:
		print Exception,err
		return HttpResponse("Error,Unable to fetch course details.")	
	attendance_dict={}
	try:											#Dictionary to store attendance coursewise
		for course in course_list:
			#getting attendance for each course(splitting course_id IITBombay/CS101/2015_2016 TO GET CS101)
			attendance_dict[course.split("/")[-2]]=get_student_course_attendance(student_id,course)
	except Exception,err:
		print Exception,err
		return HttpResponse("Error,Unable to fetch attendance for a course from mongodatabase.")
	try:
		response=render_to_response('mis/student_dash.html',{'attendance_dict':attendance_dict,'course_count':len(course_list),'data':get_student_allcourses_grade(student_id),'uname':request.session["username"]});
		response.set_cookie('student_id',student_id)				#storing username in cookies so can be used in navigation
	except Exception,err:
		print Exception,err
		return HttpResponse("Problem in rendering the template.")	
		
	return response;

	



'''
	Description: This function is to find the attendance of a student in all courses
	Input parameters:
	request : It is an http request sent from the browser 
	student_id : unique user_id of student
	Output:
	response: response object containing attendance dictionary rendered in student_dash.html
	Author:
	Chirram Kumar and Devesh Kumar
	Date of creation:
	18/06/2015  
	attendance dictionary:{"CS101":[22,226],"CS742":[5,44]} -- student has completed 22 components out of 226 in the course CS101
'''

def get_student_all_courses_attendance(request):        

	if(request.COOKIES.has_key('student_id')):
		student_id=(request.COOKIES['student_id'])
	else:
		return HttpResponse("Your Session has expired. Please re-login.")
	try:
		course_list=get_student_enrolled_courses(student_id)   		#Get all courses enrolled by student as a list
	except Exception,err:
		print Exception,err
		return HttpResponse("Error,Unable to fetch course details.")	
	attendance_dict={}
	try:											#Dictionary to store attendance coursewise
		for course in course_list:
			#getting attendance for each course(splitting course_id IITBombay/CS101/2015_2016 TO GET CS101)
			attendance_dict[course.split("/")[-2]]=get_student_course_attendance(student_id,course)
	except Exception,err:
		print Exception,err
		return HttpResponse("Error,Unable to fetch attendance for a course from mongodatabse.")
	try:
		response=render_to_response('mis/student_dash.html',{'attendance_dict':attendance_dict,'course_count':len(course_list),'data':get_student_allcourses_grade(str(student_id))});
	except Exception,err:
		print Exception,err
		return HttpResponse("Problem in rendering the template.")			
	return response;





'''
	Description: This function  gives all the courses that he is enrolled and active.
	It returns a list containing all the courses enrolled by the student
	Input parameters: 
	student_id : unique user_id of student
	Output:
	courses_list: A list of courses in which student is enrolled
	Author:
	Chirram Kumar and Devesh Kumar
	Date of creation:
	18/06/2015  
	ex:['Admin/RDM101/2015_16','IIT_BOBMAY/RDM1031/2014_T1']
'''
def get_student_enrolled_courses(student_id):

	try:
		#Getting mysql connection 
		db = MySQLdb.connect(DatabaseConfig.MYSQL_HOST,DatabaseConfig.MYSQL_USER,DatabaseConfig.MYSQL_PASSWORD,DatabaseConfig.MYSQL_DATABASE)  #Getting MySQL Database Connection
		cursor = db.cursor()
		#Executing query
		cursor.execute("select course_id as course from student_courseenrollment where user_id='"+str(student_id)+"' and is_active=1;")
		#Fetching data using cursor object
		data=cursor.fetchall()	
		courses_list=[column[0] for column in data]	
		#closing database connection
		db.close();	
	except Exception,err:
															
		print "Error, in estabilishing MySQL Connection"
		print Exception,err
		raise Exception,err;


	return courses_list
	
'''
	Description: This function is to find the attendance of a student in a course
	Input parameters:
	student_id : unique user_id of student
	course_id : unique id of each course

	Output:
	attendance_list: [a,b] representing student has completed "a" course components(problems/videos ..etc) out of "b".
	Author:
	Chirram Kumar and Devesh Kumar
	Date of creation:
	18/06/2015  
'''
def get_student_course_attendance(student_id,course_id):

	# Establish database connection
	
	try: 
		db = MySQLdb.connect(DatabaseConfig.MYSQL_HOST,DatabaseConfig.MYSQL_USER,DatabaseConfig.MYSQL_PASSWORD,DatabaseConfig.MYSQL_DATABASE)  #Getting MySQL Database Connection
		cursor = db.cursor()
	except:
	# Create a cursor object using cursor() method 
		print "Error, in estabilishing MySQL Connection"
		raise Exception,err;

	
	#Query to fetch course id and no of course components visited by the user
	query='select count(*) as total_visited from courseware_studentmodule where (module_type="video" OR module_type="problem") and course_id="'+course_id+'"  and student_id='+str(student_id)+';'	
	try:
		#Executing query
		cursor.execute(query)
		#Fetch all the records
		data=cursor.fetchall()
		db.close()
	except Exception,err:
		print "Error, in fetching student attendance(While executing query to fetch data from MySQL database)"
		print Exception,err
		raise Exception,err;
	try:
		connection=MongoClient(DatabaseConfig.MONGO_HOST,DatabaseConfig.MONGO_PORT)		#Acquiring Connection from mongo database
	except Exception,err:
		print "Error in getting Mongo Connection"
		raise Exception,err;
	total_components=0
	try:
		database=connection[DatabaseConfig.MONGO_DATABASE1]	#edxapp is mongo database containg all the course in modulestore collection
		cursor=database[DatabaseConfig.MDC1].aggregate([{"$match":{"_id.course":course_id.split("/")[-2],"_id.category":"vertical","_id.revision":{"$ne":"draft"}}},{"$project":{"no":{"$size":"$definition.children"}}}]);
		
		for document in cursor["result"]:
			total_components=total_components+document["no"]
		connection.close()
	except Exception,err:
		print "Error, in iterating mongo documents"
		print Exception,err
		raise Exception,err;
	return [data[0][0],total_components]
########################################## Course Structure Starts here ##############################



def get_bootstrap(request):
	if(request.COOKIES.has_key('student_id')):
		student_id=(request.COOKIES['student_id'])
	else:
		return HttpResponse("Your Session has expired. Please re-login.")
	courses_lst = get_student_enrolled_courses(str(student_id))
	course_lst = []
	for data in courses_lst:
		data = data.split('/')
		course_lst.append(data[1])

	return render(request,'mis/bootstrap-grid.html', {'course_lst':course_lst, 'lst_size':range(len(course_lst)), 'uname':request.session['username'] })


def get_course_structure(request):
    '''
        Following function return mapping of course with sequential section,
        sequential section with vertical section, vertical section with
        their respective sub-components and sub-components with units
        in final_data dictionary for representing course structure.
        Input :
              Nothing
        Output:
              final_data dictionary
        Author:
             Ankit (ankit93100@gmail.com)
        Last Edited On:
             1 July 2015
    '''
    '''
    if 'user_id' in request.session:
        print "user"
    else:
        print "not user"
    '''         
    #print "called"
    
    course_num = str(request.GET.get('course_num'))
    #print course_num
    final_data = dict()
    connection = MongoClient(DatabaseConfig.MONGO_HOST, DatabaseConfig.MONGO_PORT)
    
    database = connection[DatabaseConfig.MONGO_DATABASE1]
    
    cur = database[DatabaseConfig.MDC1].find({"_id.course":course_num,"_id.category":"course" })
    
    for data in cur:
        course_id = data["_id"]["org"] + "/" + data["_id"]["course"] + "/" + data["_id"]["name"]
        
    cursor = database[DatabaseConfig.MDC1].aggregate([{ "$match": {"_id.course":course_num, "_id.category":"chapter","_id.revision":{"$ne":"draft"}} }, 
                                             { "$project": { "metadata": 1, "definition": 1, "edit_info" : 1 } },
                                             { "$sort" : { "edit_info.published_date" : 1  }  } ])
    #print cursor
    chapter = []
    lst_chapter = []
    for data in cursor['result']:
        chapter.append(data)
        lst_chapter.append(data['metadata']['display_name'])
    
    final_data[course_num] = lst_chapter
    #print final_data
    sequential = []
    for data in chapter:
        lst_children = data['definition']['children']
        
        lst_seq = {}
        for child in lst_children:
            child = child.split('/')[-1]
            
            cur = database[DatabaseConfig.MDC1].aggregate([{ "$match": {"_id.name":child,"_id.revision":{"$ne":"draft"}} },
                                                 { "$project": { "metadata": 1, "definition": 1 } } ])
            for rec in cur['result']:
                
                sequential.append(rec)
                lst_seq[child] = rec['metadata']['display_name']
        
        final_data[data['metadata']['display_name']] = lst_seq
    #print final_data, "\n"
    vertical = []
    for data in sequential:
        lst_children = data['definition']['children']
        lst_ver = {}
        for child in lst_children:
            child = child.split('/')[-1]
            
            cur = database[DatabaseConfig.MDC1].aggregate([{ "$match": {"_id.name":child,"_id.revision":{"$ne":"draft"}} },
                                                 { "$project": { "metadata": 1, "definition": 1 } } ])
            for rec in cur['result']:
                vertical.append(rec)
                lst_ver[child] = rec['metadata']['display_name']
        
        final_data[data['metadata']['display_name']] = lst_ver
    #print final_data, "\n"
    unit = []
    #match_lst = []
    for data in vertical:
        lst_children = data['definition']['children']
        
        lst_unit = {}
        for child in lst_children:
            ch1 = child
            ch1 = ch1.split('/')[-1]
            #print ch1
            cur = database[DatabaseConfig.MDC1].find({"_id.course":course_num,"_id.name":ch1 })
            #print cur
            name = ""
            category = ""
            for dta in cur:
                category =  dta["_id"]["category"]
                if category == 'html' or category == 'discussion':
                    break					
                try:
                    name = dta['metadata']['display_name']
                    #print name
                except:
                    pass
            if category == 'html' or category == 'discussion':
                break            
            #print category        
            if name != "":
    	        child= name
            else:
                child = child.split('/')[-2]	
            #print ch1
            lst_unit[ch1] = child
        final_data[data['metadata']['display_name']] = lst_unit
    #print final_data, "\n"
    #print course_id
    #print request.session['user_id']
    lst = get_list(request.session['user_id'], course_id)
    #print lst
    final_data["check_id"] = lst
    #print final_data
    return HttpResponse(json.dumps(final_data), content_type='application/javascript')

def get_list(student_id,course_id):
	
	# Establish database connection
	try: 
		db = MySQLdb.connect(DatabaseConfig.MYSQL_HOST,DatabaseConfig.MYSQL_USER,DatabaseConfig.MYSQL_PASSWORD,DatabaseConfig.MYSQL_DATABASE)  #Getting MySQL Database Connection
		cursor = db.cursor()
	except:
	# Create a cursor object using cursor() method 
		print "Error, in estabilishing MySQL Connection"
		raise Exception,err;

	#Query to fetch course id and no of course components visited by the user
	query='select module_id from courseware_studentmodule where course_id="'+course_id+'"  and student_id='+str(student_id)+';'	
	try:
		#Executing query
		cursor.execute(query)
		#Fetch all the records
		data=cursor.fetchall()
		#print data
		db.close()
	except Exception,err:
		print "Error, in fetching student attendance(While executing query to fetch data from MySQL database)"
		print Exception,err
		raise Exception,err;
	req_id = []	
	for item in data:
		itm = item[0].split('/')
		if itm[-2] == 'video' or itm[-2] == 'problem':
			req_id.append(itm[-1])
		#print itm[-2], itm[-1]
	return req_id





########################################## Grades Section Starts Here #################################################################


#This function is to get a list of students enrolled in a course

'''
	Description: This function is to find the list of students in a course
	Input parameters:
	course_id : unique id of each course

	Output:
	student_list: [5,10,20....] list of student ids
	Author:
	Amanpreet Kang and Chirram Kumar
	Date of creation:
	18/06/2015  
'''


def get_student_lst(course_id):
    try: 
        db = MySQLdb.connect(DatabaseConfig.MYSQL_HOST,DatabaseConfig.MYSQL_USER,DatabaseConfig.MYSQL_PASSWORD,DatabaseConfig.MYSQL_DATABASE)  #Getting MySQL Database Connection
        # Create a cursor object using cursor() method
        cursor = db.cursor()
        cursor.execute("select user_id from student_courseenrollment where course_id like '"+str(course_id)+"' and is_active = 1;")
        data=cursor.fetchall()
        db.close()    
    except Exception,err:
        print "Error, in estabilishing MySQL Connection"
        print Exception,err
    #course_id = 'iitb/t101/2015-2016'
    student_lst=[column[0] for column in data]
    return student_lst

'''
	Description: This function is to find avg,max and student marks per each quiz in a course
	Input parameters:
	course_id : unique id of each course ---but it is sent as a parameter through GET method
	request: HttP request object
	Output:
	avg_max_marks_list: A list Containing avg marks list, max marks list and student marks list per each quiz
	Author:
	Amanpreet Kang and Chirram Kumar
	Date of creation:
	18/06/2015  
'''

def get_avg_max_marks_list(request):#student_id,course_id

	if(request.COOKIES.has_key('student_id')):
		student_id=(request.COOKIES['student_id'])
	else:
		return HttpResponse("Your Session has expired. Please re-login.")
	course_id=str(request.GET["course_id"]);
	#course_id=course_id.split('/')[-2]
	student_list=get_student_lst(course_id);
	avg_marks_list=get_student_course_grade(str(student_id),str(course_id));
	max_marks_list=[]
	temp_avg_marks=[]
	student_marks_list=[]
	number_of_students=len(student_list)
	for item in avg_marks_list:
		max_marks_list.append(item[:])
		student_marks_list.append(item[:])
	for student in student_list:
		temp_avg_marks=get_student_course_grade(student,course_id);
		for quiz_no in range(len(temp_avg_marks)):
			avg_marks_list[quiz_no][2]=(avg_marks_list[quiz_no][2])+(temp_avg_marks[quiz_no][2])
			if((temp_avg_marks[quiz_no][2])>(max_marks_list[quiz_no][2])):
				(max_marks_list[quiz_no][2])=temp_avg_marks[quiz_no][2]

	for quiz_no in range(len(avg_marks_list)):		
		avg_marks_list[quiz_no][2]=(avg_marks_list[quiz_no][2])/float(number_of_students);
	avg_max_marks_list=[]
	avg_max_marks_list.append(avg_marks_list);
	avg_max_marks_list.append(max_marks_list);
	avg_max_marks_list.append(student_marks_list);
	print "\navg_max_marks_list\n"#avg_max_marks_list;
	for i in avg_max_marks_list:
		print i
	#return avg_max_marks_list;
	return render_to_response('mis/course_quizes.html',{'data':avg_max_marks_list})
			
'''
	Description: This function is to find student marks per each quiz in a course
	Input parameters:
	student_id : unique id of student
	course_id : unique id of each course 
	
	
	Output:
	student_marks_list: A list Containing avg marks list, max marks list and student marks list per each quiz
	Author:
	Samridhi and Sneha
	Date of creation:
	18/06/2015  
'''
def get_student_course_grade(student_id,course_id):
	results_list=[]		#A list to store the final results
	sub_results_list=[]		#A list which shall be embedded within the results_list list
	highchart_list=[]       #List to be returned for highcharts
        try:
                client=pymongo.MongoClient(DatabaseConfig.MYSQL_HOST,DatabaseConfig.MONGO_PORT) 	#Establishing MongoDB connection
        except:
                print "MongoDB connection not established"
                return HttpResponse("MongoDB connection not established")
        try:
                db_mysql=MySQLdb.connect(DatabaseConfig.MYSQL_HOST,DatabaseConfig.MYSQL_USER,DatabaseConfig.MYSQL_PASSWORD,DatabaseConfig.MYSQL_DATABASE)  #Getting MySQL Database Connection
        except:
                print "MySQL connection not established"                #Establishing MySQL connection
                return HttpResponse("MySQL connection not established")
	db_mongo=client[DatabaseConfig.MONGO_DATABASE1]		#Getting the object for edxapp database of MongoDB
	mongo_cur=db_mongo[DatabaseConfig.MDC1].find({'_id.course':course_id,'_id.category':'course'},{'definition.data.grading_policy.GRADER':1,'_id':0})		#Query to get the grading policy of a partticular course
	try:
                strquery="Select grade,max_grade from courseware_studentmodule where max_grade is not null and grade is not null and student_id=\'"+str(student_id)+"\' and module_id=%s"
		i=mongo_cur[0]
		stud_avg_tot=0			
		list1=i['definition']['data']['grading_policy']['GRADER']		#Getting the GRADER list which stores the different formats and their weights in a course
		for j in range(len(list1)):      				#iterating over the formats
			best_score_list=[]					#This list will store the final scores for the particular format
			drop_count=list1[j]['drop_count']			#Gives number of droppable sections for that problem
			type=list1[j]['type']				#Gives the type of the format i.e. Quiz, Final Exam etc.
			weight=list1[j]['weight']			#Gives the weights of the formats 
			min_count=list1[j]['min_count']	#Gives the minimum number of sections of that type present in the course
			sub_results_list=[]		#initializing the sub_results to an empty list
			mongo_cur2=db_mongo[DatabaseConfig.MDC1].find({'_id.course':course_id,'_id.category':'sequential','metadata.format':type,'metadata.graded':True},{'metadata':1,'definition.children':1})            
			#Query to find the different sequentials having the format 'type' 
			sequential_coun=0		#intializing sequential count to zero
			for k in mongo_cur2:	
				sequential_coun+=1				
				avg_score_sequential=0		
				sum_avg_prob_score=0		
                                sum_prob_score_obt=0
                                sum_tot_prob_score=0
				coun_prob=0					#Initializing problem count as zero
				list2=k['definition']['children']		#Getting the children list of the sequential, this will consist of vertical ids
				for m in range(len(list2)):				#Iterating over the list of vertical ids
					child_id=list2[m]			#Getting the vertical id
					arr=child_id.split('/')							#Splitting the vertical id to get the _id.name field for the vertical
					vertical_id=arr[len(arr)-1]						#Getting the vertical's _id.name
					mongo_cur3=db_mongo[DatabaseConfig.MDC1].find({'_id.name':vertical_id,'_id.course':course_id,'_id.category':'vertical'},{'definition.children':1}).limit(1)
					#query to get the vertical document with the _id.name as vertical id
					n=mongo_cur3[0]			
					list3=n['definition']['children']                       #getting the children array for this vertical, consisiting of list of component ids
					for o in range(len(list3)):                                     #Iterating over the list of component ids
						comp_id=list3[o]  #Getting the component id
						arr2=comp_id.split('/')                         #Splitting the component id to get the _id.name field for the problem
						component_id=arr2[len(arr2)-1]          #Getting the component's _id.name
						mongo_cur4=db_mongo[DatabaseConfig.MDC1].find({'_id.name':component_id,'_id.course':course_id,'_id.category':'problem'},{'metadata.weight':1}).limit(1)
						#query to get the problem document with the _id.name as problem id and category as problem.
						try:
							p=mongo_cur4[0]
							problem_id=comp_id                              #Getting the module_id for that problem
							mysql_cur=db_mysql.cursor()                     #Getting MySQL cursor object
							#query="Select grade,max_grade from courseware_studentmodule where student_id=\'"+student_id+"\' and module_id=\'"+problem_id+"\' and max_grade is not null and grade is not null" 
                                                        
							#Query to get the grades for the student for that particular problem
							mysql_cur.execute(strquery,(str(problem_id),))                #Executing query
							row=mysql_cur.fetchone()                #Fetching the row returned, only one row shall be returned
							try:
								grade=row[0]                            #Getting the grade of the student for this problem
								maxgrade=row[1]                         #Getting the max_grade of the student for this problem
								try:
									weight_of_problem=p['metadata']['weight']                      #Getting the weight of the problem      
								except:
									weight_of_problem=maxgrade                              #If no weight is defined, weight=maxgrade
					
								score_obt=grade*weight_of_problem/maxgrade              #Weighted score obtained for this problem
								tot_score=weight_of_problem                             #Weighted total score for this problem
								sum_prob_score_obt+=score_obt
								sum_tot_prob_score+=tot_score
							except:
								try:
									weight_of_problem=p['metadata']['weight']
								except: 
									weight_of_problem=0             #If weight is not defined and the problem has not been attempted
								sum_tot_prob_score+=weight_of_problem
						except:
							continue
                                                                
		
                                if sum_tot_prob_score>0:
					avg_score_sequential=sum_prob_score_obt/sum_tot_prob_score		#Calculating avg score of this sequential
                                else:
                                        avg_score_sequential=0
				sub_results_list.append([sequential_coun,avg_score_sequential])			
				highchart_list.append([str(type),str(sequential_coun),(avg_score_sequential)])
				best_score_list.append(avg_score_sequential)		#Adding the sequential score to best_score_list
			best_score_list.sort(reverse=True)  #Sorting the scores list for that format in descending order
			sum_score_format=0			#Initializing sum score of format to 0
			for q in range(sequential_coun-drop_count):		#Getting the sum of best scores in the format
				sum_score_format+=best_score_list[q]
			if sequential_coun-drop_count>0:
                                avg_score_format=sum_score_format/(sequential_coun-drop_count)		#Getting average score of the format      
                                sub_results_list.append(['Avg',avg_score_format])				#Appending values to list
                                results_list.append([type,sub_results_list])
                                stud_avg_tot+=avg_score_format*weight
                        else:
                                avg_score_format=0
					#Getting total student average score
                
                if len(results_list)>0:
                        sub_results_list=[]
                        sub_results_list.append([1,stud_avg_tot])			#Appending final results in list
                        results_list.append(['Total',sub_results_list])
                        highchart_list.append(['Total',str(""),float(stud_avg_tot)])
	except:
		result_list=[]
	client.close()
	db_mysql.close();print highchart_list;
        #print highchart_list
        return highchart_list
	#return render_to_response('newindex3.html',{'data':highchart_list})


'''
def get_student_course_grade2(student_id,course_id,db_mysql,client):
	
	db_mongo=client.edxapp		#Getting the object for edxapp database of Mongo
	try:
                mongo_cur=db_mongo[DatabaseConfig.MDC1].find({'_id.course':course_id,'_id.category':'course'},{'definition.data.grading_policy.GRADER.':1,'_id':0}) #Query to get the grading policy of a partticular course
		
		try:
                        
			i=mongo_cur[0]
                        stud_avg_tot=0			#initializing the student total marks for the course as zero
                        list=i['definition']['data']['grading_policy']['GRADER']		#Getting the GRADER list which stores the different formats and their weights in a course
                        for j in range(len(list)):				#iterating over the formats
                                best_score_list=[]					#This list will store the final scores for the particular format
                                drop_count=i['definition']['data']['grading_policy']['GRADER'][j]['drop_count']			#Gives number of droppable sections for that problem
                                type=i['definition']['data']['grading_policy']['GRADER'][j]['type']				#Gives the type of the format i.e. Quiz, Final Exam etc.
                                weight=i['definition']['data']['grading_policy']['GRADER'][j]['weight']			#Gives the weights of the formats 
                                min_count=i['definition']['data']['grading_policy']['GRADER'][j]['min_count']	#Gives the minimum number of sections of that type present in the course
                                try:
                                        mongo_cur2=db_mongo[DatabaseConfig.MDC1].find({'_id.course':course_id,'_id.category':'sequential','metadata.format':type,'metadata.graded':True},{'metadata':1,'definition.children':1})
                                        # Getting the sequentials of a  particular format
                                        sequential_coun=0		#intializing sequential count to zero
                                        for k in mongo_cur2:	#Iterating over the sequentials of format 'type'
                                                sequential_coun+=1		#Incrementing sequential count		
                                                avg_score_sequential=0		#Initializing average score of sequential as zero
                                                sum_avg_prob_score=0		#Initializing sum of average problem scores as zero
                                                sum_prob_score_obt=0
                                                sum_tot_prob_score=0
                                                coun_prob=0					#Initializing problem count as zero
                                                list2=k['definition']['children']		#Getting the children list of the sequential, this will consist of vertical ids
                                                for m in range(len(list2)):				#Iterating over the list of vertical ids
                                                        child_id=k['definition']['children'][m]			#Getting the vertical id
                                                        arr=child_id.split('/')							#Splitting the vertical id to get the _id.name field for the vertical
                                                        vertical_id=arr[len(arr)-1]						#Getting vertical's _id.name 
                                                        mongo_cur3=db_mongo[DatabaseConfig.MDC1].find({'_id.name':vertical_id,'_id.course':course_id,'_id.category':'vertical'},{'definition.children':1}).limit(1)
                                                        #query to get the vertical document with the _id.name as vertical id
							try:
								n=mongo_cur3[0]
                                                                list3=n['definition']['children']			#getting the children array for this vertical, consisiting of list of component ids
                                                                for o in range(len(list3)):					#Iterating over the list of component ids
                                                                        comp_id=n['definition']['children'][o]	#Getting the component id
                                                                        arr2=comp_id.split('/')				#Splitting the component id to get the _id.name field for the problem
                                                                        component_id=arr2[len(arr2)-1]		#Getting component's _id.name
                                                                        mongo_cur4=db_mongo[DatabaseConfig.MDC1].find({'_id.name':component_id,'_id.course':course_id,'_id.category':'problem'},{'metadata.weight':1}).limit(1)
                                                                        #query to get the problem document with the _id.name as problem id and category as problem.
									try:
										p=mongo_cur4[0] 
                                                                                problem_id=comp_id				#Getting the module_id for that problem
                                                                                mysql_cur=db_mysql.cursor()			#Getting MySQL cursor object
                                                                                query="Select grade,max_grade from courseware_studentmodule where student_id=\'"+str(student_id)+"\' and module_id=\'"+problem_id+"\' and max_grade is not null and grade is not null" 
                                                                                #Query to get the grades for the student for that particular problem 
                                                                                try:
                                                                                        mysql_cur.execute(query)		#Executing query
                                                                                except:
                                                                                        f=0
                                                                                row=mysql_cur.fetchone()		#Fetching the row returned, only one row shall be returned
                                                                                try:
                                                                                        grade=row[0]				#Getting the grade of the student for this problem
                                                                                        maxgrade=row[1]				#Getting the max_grade of the student for this problem
                                                                                        try:
                                                                                                weight_of_problem=p['metadata']['weight']			#Getting the weight of the problem	
                                                                                        except:
                                                                                                weight_of_problem=maxgrade				#If no weight is defined, weight=maxgrade
                                                                                        score_obt=grade*weight_of_problem/maxgrade		#Weighted score obtained for this problem
                                                                                        tot_score=weight_of_problem				#Weighted total score for this problem
                                                                                        sum_prob_score_obt+=score_obt
                                                                                        sum_tot_prob_score+=tot_score    
                                                                                except:
                                                                        
                                                                                        try:
                                                                                                weight_of_problem=p['metadata']['weight']
                                                                                        except:
                                                                                                weight_of_problem=0          #if no weight is defined and the problem has not been attempted
                                                                                        sum_tot_prob_score+=weight_of_problem
                                                                        except:
										continue                 
							except:
								continue
                                                if sum_tot_prob_score>0:
                                                        avg_score_sequential=sum_prob_score_obt/sum_tot_prob_score		#Calculating avg score of this sequential
                                                best_score_list.append(avg_score_sequential)		#Adding the sequential score to best_score_list
                                except:
                                        
                                        return -1
                                best_score_list.sort(reverse=True)  #Sorting the scores list for that format in descending order
                                sum_score_format=0			#Initializing sum score of format to 0
                                for q in range(sequential_coun-drop_count):		#Getting the sum of best scores in the format
                                        sum_score_format+=best_score_list[q]
                                if sequential_coun-drop_count > 0 :
                                        avg_score_format=sum_score_format/(sequential_coun-drop_count)		#Getting average score of the format
                                        stud_avg_tot+=avg_score_format*weight		#Getting total student average score   
                                else:
                                        avg_score_format=0
        	except:
                        
			return -1
        except:
                
                return -1
        
        return stud_avg_tot
'''


""" Description: Function to get average grade of a student in all the courses enrolled along with the course maximum and average grade.
    Input Parameters:
            student_id: id of the student.
    Output Type : List
    Author: Sneha
    Date of creation:21 june 2015
"""
'''
def get_student_allcourses_grade(student_id):
        result_list=[]
        try:
                db_sql=MySQLdb.connect(DatabaseConfig.MYSQL_HOST,DatabaseConfig.MYSQL_USER,DatabaseConfig.MYSQL_PASSWORD,DatabaseConfig.MYSQL_DATABASE)  #Getting MySQL Database Connection
        except:
                print "MySQL connection not established"
                return HttpResponse("MySQL connection not established")
        try:
                client=pymongo.MongoClient(DatabaseConfig.MYSQL_HOST,DatabaseConfig.MONGO_PORT)     #establishing mongodb connection
        except:
                print "MongoDB connection not established"
                return HttpResponse("MongoDB connection not established")
        sql_cur=db_sql.cursor()
        query="select course_id from student_courseenrollment where user_id=\'"+student_id+"\'"     #get all courses in which the student is enrolled
        try:
                sql_cur.execute(query)
        except:
                print "Cannot execute the query"
                db_sql.close()
                client.close()
                return HttpResponse("Cannot fetch data from database")
        result=sql_cur.fetchall()
        for row in result:
                course_avg_list=get_student_grade2(row[0],student_id,db_sql,client)
                c_id=row[0].split('/')
                course_name=c_id[1]
                if len(course_avg_list)>0:
                        student_grade=course_avg_list[2]
                        result_list.append([row[0],student_grade,course_avg_list[0],course_avg_list[1]])
                        
        db_sql.close()
        client.close()
        return result_list;
'''

def get_student_allcourses_grade(student_id):
        result_list=[]
        try:
		print "Connecting to mysql from get_student_allcourses_grade"
                db_sql=MySQLdb.connect(DatabaseConfig.MYSQL_HOST,DatabaseConfig.MYSQL_USER,DatabaseConfig.MYSQL_PASSWORD,DatabaseConfig.MYSQL_DATABASE)  #establishing sql connection
        except:
                print "MySQL connection not established"
                return HttpResponse("MySQL connection not established")
        try:
                client=pymongo.MongoClient(DatabaseConfig.MONGO_HOST, DatabaseConfig.MONGO_PORT)     #establishing mongodb connection
        except:
                print "MongoDB connection not established"
                return HttpResponse("MongoDB connection not established")
        
        sql_cur=db_sql.cursor()
        query="select course_id from student_courseenrollment where user_id=\'"+student_id+"\'"     #get all courses in which the student is enrolled
        strquery2="Select grade,max_grade from courseware_studentmodule where max_grade is not null and grade is not null and student_id=%s and module_id=%s"    
        strquery="select user_id,course_id from student_courseenrollment where course_id=%s"
        try:
                sql_cur.execute(query)
        except:
                print "Cannot execute the query"
                db_sql.close()
                client.close()
                return HttpResponse("Cannot fetch data from database")
        result=sql_cur.fetchall()
        for row in result:
                course_avg_list=get_student_grade2(row[0],student_id,db_sql,client,strquery2,strquery)
                if len(course_avg_list)>0:
                        student_grade=course_avg_list[2]
                        result_list.append([row[0],student_grade,course_avg_list[0],course_avg_list[1]])
                        
	print "Disconnecting from mysql in getstudent_allcourses_grade"
        db_sql.close()
        client.close()
        #return render_to_response('newindex4.html',{'data':result_list})
        return result_list;

""" Description: Function to get average grades of all students in a particular course.This function is called by get_student_allcourses_grade().
    Input Parameters:
            course_id: id of course passed as a parameter by function getall_course_grades.
            student_id: id of student 
            db_sql: MySQL Database connection object
            client: MongoDB connection object
    Output Type : List
    Author: Sneha
    Date of creation:21 june 2015
"""

def get_problem_ids(db_sql,client,course_id):
	print "get_problem_ids"
	
	problem_list=[]
	format_dict={}
	db_mongo=client[DatabaseConfig.MONGO_DATABASE1]	#Getting the object for edxapp database of Mongo
	sequential_problem_dict={}
	#print "before first try"
	try:
		print "in 1st try"
                mongo_cur=db_mongo[DatabaseConfig.MDC1].find({'_id.course':course_id,'_id.category':'course'},{'definition.data.grading_policy.GRADER':1,'_id':0}) #Query to get the grading policy of a partticular course
		try:    
			print "in 2nd try"
			i=mongo_cur[0]
                        
			list1=i['definition']['data']['grading_policy']['GRADER'] #Getting the GRADER list which stores the different formats and their weights in a course
                        for j in range(len(list1)):				#iterating over the formats
                                drop_count=list1[j]['drop_count']		#Gives number of droppable sections for that problem
                                type=list1[j]['type']				#Gives the type of the format i.e. Quiz, Final Exam etc.
                                weight=list1[j]['weight']			#Gives the weights of the formats 
                                min_count=list1[j]['min_count']	#Gives the minimum number of sections of that type present in the course
				print "iter1"
				short_label=list1[j]['short_label']				
				format_list=[]
				format_list.append(weight)
				format_list.append(min_count)
				format_list.append(drop_count)
				format_list.append(short_label)
				format_dict[type]=format_list   
				#print "format_dict=",format_dict                           
				try:
                                        mongo_cur2=db_mongo[DatabaseConfig.MDC1].find({'_id.course':course_id,'_id.category':'sequential','metadata.format':type,'metadata.graded':True},{'metadata':1,'definition.children':1})

                                       # Getting the sequentials of a  particular format
                                        for k in mongo_cur2:	#Iterating over the sequentials of format 'type'
						problem_list=[]
						problem_list.append(type)
						sequential_id=k['_id']['name']
                                                list2=k['definition']['children']		#Getting the children list of the sequential, this will consist of vertical ids
                                                #print "new problem list for a new sequential"
                                                for m in range(len(list2)):				#Iterating over the list of vertical ids
                                                        child_id=list2[m]			#Getting the vertical id
                                                        arr=child_id.split('/')							#Splitting the vertical id to get the _id.name field for the vertical
                                                        vertical_id=arr[len(arr)-1]						#Getting vertical's _id.name 
                                                        mongo_cur3=db_mongo[DatabaseConfig.MDC1].find({'_id.name':vertical_id,'_id.course':course_id,'_id.category':'vertical'},{'definition.children':1}).limit(1)
                                                        print "iter2"
                                                        #query to get the vertical document with the _id.name as vertical id
							try:
								n=mongo_cur3[0]
                                                                list3=n['definition']['children']			#getting the children array for this vertical, consisiting of list of component ids
                                                                for o in range(len(list3)):					#Iterating over the list of component ids
                                                                        comp_id=list3[o]	#Getting the component id
                                                                        arr2=comp_id.split('/')				#Splitting the component id to get the _id.name field for the problem
                                                                        component_id=arr2[len(arr2)-1]		#Getting component's _id.name
                                                                        mongo_cur4=db_mongo[DatabaseConfig.MDC1].find({'_id.name':component_id,'_id.course':course_id,'_id.category':'problem'},{'metadata.weight':1}).limit(1)
                                                                        print "iter3"
                                                                        #query to get the problem document with the _id.name as problem id and category as problem.					
									try:
										p=mongo_cur4[0]
										problem_id=comp_id
										problem_list.append(problem_id)
										try:
											wt=p['metadata']['weight']
											problem_list.append(p['metadata']['weight'])
										except:
											print "in wt except"
											problem_list.append(0)
										
										
									except:
										continue
							except:
								continue
						sequential_problem_dict[sequential_id]=problem_list
						#print problem_list
				except:
					continue
		except:
			#print "in 2nd except"
			return -1
	except:
		#print "in 1st except"
		return -1	
	#print sequential_problem_dict
	return (format_dict,sequential_problem_dict)

def get_student_course_grade2(student_id,sequential_problem_dict,format_dict,db_mysql,client,strquery2):
        print "in get_student_course_grade2 with student_id=",student_id
	mysql_cur=db_mysql.cursor()			#Getting MySQL cursor object
	sequential_coun=0
	stud_avg_tot=0	
	for k_format, v_format in format_dict.iteritems():
                best_score_list=[]
                sequential_coun=0
                for k,v in sequential_problem_dict.iteritems():
                        sum_tot_prob_score=0
                        sum_prob_score_obt=0
                        if v[0]==k_format:
                                #print "sequential_coun=",sequential_coun, "sequential_id=",k
                                sequential_coun=sequential_coun+1
                                for i in range(1,len(v),2):
                                        #print "inside a new problem"
                                        problem_id=v[i]
                                        mysql_cur.execute(strquery2,(str(student_id),str(problem_id)))
                                        result=mysql_cur.fetchall()
                                        j=i+1			#Getting the weight of the problem
                                        weight_of_problem=v[j]
                                        sum_tot_prob_score+=weight_of_problem
                                        #if v[0]=="Final Exam":
                                        #       print weight_of_problem
                                        for row in result:
                                                try:
                                                        grade=row[0]				#Getting the grade of the student for this problem
                                                        maxgrade=row[1]				#Getting the max_grade of the student for this problem
                                                        if weight_of_problem==0:
                                                                print "weight not defined"
                                                                weight_of_problem=maxgrade
                                                                sum_tot_prob_score+=weight_of_problem
                                                        score_obt=grade*weight_of_problem/maxgrade		#Weighted score obtained for this problem
                                                        #sum_tot_prob_score+=weight_of_problem
                                                        #tot_score=weight_of_problem				#Weighted total score for this problem
                                                        sum_prob_score_obt+=score_obt
                                                        #sum_tot_prob_score+=tot_score
                                                        #print "score_obt=",score_obt,"tot_score=",tot_score,"sum_prob_score=",sum_prob_score_obt,"sum_tot_prob_score=",sum_tot_prob_score

                                                except:
                                                        print "in xcept"
                                                        f=0
                                                        #sum_tot_prob_score+=weight_of_problem
                                                        #sum_tot_prob_score+=weight_of_problem
                                                #if v[0]=="Final Exam":
                                                 #       print "sum_tot_prob_score=",sum_tot_prob_score,"weight=",weight_of_problem
                                        #if v[0]=="Final Exam":
                                        #print "sum_tot_prob_score=",sum_tot_prob_score,"sum_prob_score_obt=",sum_prob_score_obt
                                if sum_tot_prob_score>0:
                                        avg_score_sequential=sum_prob_score_obt/sum_tot_prob_score		#Calculating avg score of this sequential
                                else:
                                        avg_score_sequential=0
                                #print "score of this sequential=",avg_score_sequential
                                #print "avg_score_sequential=",avg_score_sequential
                                best_score_list.append(avg_score_sequential)		#Adding the sequential score to best_score_list
                #print "best_score_list=",best_score_list
                best_score_list.sort(reverse=True)  #Sorting the scores list for that format in descending order
                
                sum_score_format=0			#Initializing sum score of format to 0
                min_count=v_format[1]
                drop_count=v_format[2]
                short_label=v_format[3]
                weight=v_format[0]
                type=k_format
                #print "type=",type,"min_count=",min_count,"drop_count=",drop_count,"short_label=",short_label,"sequential_count=",sequential_coun
                for q in range(sequential_coun-drop_count):		#Getting the sum of best scores in the format
                        sum_score_format+=best_score_list[q]
                #print "sum_score_format=",sum_score_format
                if sequential_coun-drop_count > 0 :
                        avg_score_format=sum_score_format/(sequential_coun-drop_count)		#Getting average score of the format
                        stud_avg_tot+=avg_score_format*weight		#Getting total student average score   
                else:
                        avg_score_format=0
        #print "student_avg_tot=",stud_avg_tot
	return stud_avg_tot

def get_student_grade2(course_id,student_id,db_sql,client,strquery2,strquery):
        sum_grade=0
        count_student=0
        grade_list=[]
        course_name=course_id.split('/')                #Splitting course id to get course name
        c_name=course_name[1]
        sql_cur=db_sql.cursor()
        student_grade=0
        print "hello before call to get_problem_id"
	x=get_problem_ids(db_sql,client,c_name)
	if x<>-1:
		(format_dict,sequential_problem_dict)=x
	else:
		return []
	print "after call to get_problem_id"
        sql_cur.execute(strquery,(str(course_id),))
        result=sql_cur.fetchall()
        for row in result:
                grade=get_student_course_grade2(str(row[0]),sequential_problem_dict,format_dict,db_sql,client,strquery2)
                if grade==-1:                                   #If grading policy is not defined in a course
                        return []
                if student_id==str(row[0]):
                        student_grade=grade
                grade_list.append(grade)                                #Appending students grade to list
                sum_grade+=grade                        #Adding grades of all students
                count_student+=1                       #Counting no of students
        avg_grade=sum_grade/count_student              #Finding average grade obtained in a course
        max_grade=max(grade_list)                 #Getting maximum grade in a course
        main_list=[]                            #Appending final result list
        main_list.append(avg_grade)
        main_list.append(max_grade)
        main_list.append(student_grade)
        return main_list
'''
def get_student_grade2(course_id,student_id,db_sql,client):
        sum_grade=0
        count_student=0
        grade_list=[]
        course_name=course_id.split('/')                #Splitting course id to get course name
        c_name=course_name[1]
        sql_cur=db_sql.cursor()
        student_grade=0
        query="select user_id,course_id from student_courseenrollment where course_id=\'"+course_id+"\'"   #Query to get ids of students enrolled in a course
        sql_cur.execute(query)
        result=sql_cur.fetchall()
        for row in result:
                grade=get_student_course_grade2(row[0],c_name,db_sql,client)          #Getting grade of each student in each course
                if grade==-1:                                   #If grading policy is not defined in a course
                        return []
                if student_id==str(row[0]):
                        student_grade=grade
                grade_list.append(grade)                                #Appending students grade to list
                sum_grade+=grade                        #Adding grades of all students
                count_student+=1                       #Counting no of students
        avg_grade=sum_grade/count_student              #Finding average grade obtained in a course
        grade_list.sort(reverse=True)                   #Sorting students grade
        max_grade=grade_list[0]                 #Getting maximum grade in a course
        main_list=[]                            #Appending final result list
        main_list.append(avg_grade)
        main_list.append(max_grade)
        main_list.append(student_grade)
        return main_list
'''               
                                  
                                  
                                  
                
                
               
        
	





	
