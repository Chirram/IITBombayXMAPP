from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext,loader
from django.http import HttpResponse
from pymongo import MongoClient
from django.utils.safestring import mark_safe
from address import ip_address
from address import mongo_port
from address import sql_user
from address import sql_pswd
from address import database

import collections
import pymongo			
import MySQLdb
#import xlwt

"""Description:Function to get grades of a student in each exam(quiz,mid term,final exam etc.).It returns a list of grsdes scored in all exams by a student
   Input Parameters:
       student_id :User_id of student
       course_id : id of course
   Output Type : List
   Author: Samridhi
   Date of creation: 17 june 2015
"""
def get_student_course_grades(student_id,course_id):
	results_list=[]		#A list to store the final results
	sub_results_list=[]		#A list which shall be embedded within the results_list list
	highchart_list=[]       #List to be returned for highcharts
        try:
                client=pymongo.MongoClient(ip_address,mongo_port) 	#Establishing MongoDB connection
        except:
                print "MongoDB connection not established"
                return HttpResponse("MongoDB connection not established")
        try:
                db_mysql=MySQLdb.connect(ip_address,sql_user,sql_pswd,database)
        except:
                print "MySQL connection not established"                #Establishing MySQL connection
                return HttpResponse("MySQL connection not established")
	db_mongo=client.edxapp		#Getting the object for edxapp database of MongoDB
	mongo_cur=db_mongo.modulestore.find({'_id.course':course_id,'_id.category':'course'},{'definition.data.grading_policy.GRADER':1,'_id':0})		#Query to get the grading policy of a partticular course
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
			short_label=list1[j]['short_label']
			sub_results_list=[]		#initializing the sub_results to an empty list
			mongo_cur2=db_mongo.modulestore.find({'_id.course':course_id,'_id.category':'sequential','metadata.format':type,'metadata.graded':True},{'metadata':1,'definition.children':1})            
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
					mongo_cur3=db_mongo.modulestore.find({'_id.name':vertical_id,'_id.course':course_id,'_id.category':'vertical'},{'definition.children':1}).limit(1)
					#query to get the vertical document with the _id.name as vertical id
					n=mongo_cur3[0]			
					list3=n['definition']['children']                       #getting the children array for this vertical, consisiting of list of component ids
					for o in range(len(list3)):                                     #Iterating over the list of component ids
						comp_id=list3[o]  #Getting the component id
						arr2=comp_id.split('/')                         #Splitting the component id to get the _id.name field for the problem
						component_id=arr2[len(arr2)-1]          #Getting the component's _id.name
						mongo_cur4=db_mongo.modulestore.find({'_id.name':component_id,'_id.course':course_id,'_id.category':'problem'},{'metadata.weight':1}).limit(1)
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
				highchart_list.append([str(short_label),str(sequential_coun),str(avg_score_sequential)])
				best_score_list.append(avg_score_sequential)		#Adding the sequential score to best_score_list
			best_score_list.sort(reverse=True)  #Sorting the scores list for that format in descending order
			sum_score_format=0			#Initializing sum score of format to 0
			for q in range(sequential_coun-drop_count):		#Getting the sum of best scores in the format
				sum_score_format+=best_score_list[q]
			if sequential_coun-drop_count>0:
                                avg_score_format=sum_score_format/(sequential_coun-drop_count)		#Getting average score of the format      
                                sub_results_list.append(['Avg',avg_score_format])				#Appending values to list
                                results_list.append([short_label,sub_results_list])
                                stud_avg_tot+=avg_score_format*weight
                        else:
                                avg_score_format=0
					#Getting total student average score
                
                if len(results_list)>0:
                        sub_results_list=[]
                        sub_results_list.append([1,stud_avg_tot])			#Appending final results in list
                        results_list.append(['Total',sub_results_list])
                        highchart_list.append(['Total',str(""),str(stud_avg_tot)])
	except:
		result_list=[]
	client.close()
	db_mysql.close()
	return highchart_list
"""
   Description: Function to get average grade and maximum grade in all courses associated to a particular faculty.
   Input Parameters:
           user-id: id of the faculty.
   Output Type: List
   Author : Sneha
   Date of creation: 18 june 2015
"""

def getall_course_grades(user_id):
        try:
                client=pymongo.MongoClient(ip_address,mongo_port) 	#Establishing MongoDB connection
        except:
                print "MongoDB connection not established"
                return HttpResponse("MongoDB connection not established")
        
        try:
		print "Connecting to mySQL now from getall_course_grades"
                db_sql=MySQLdb.connect(ip_address,sql_user,sql_pswd,database)        #Connecting SQL
        except:
                print "MySQL connection not established"
                return HttpResponse("MySQL connection not established")
        result_list=[]
        sql_cur=db_sql.cursor()
        strquery2="Select grade,max_grade from courseware_studentmodule where max_grade is not null and grade is not null and student_id=%s and module_id=%s"    
        strquery="select user_id,course_id from student_courseenrollment where course_id=%s"
        query="select course_id,count(user_id) as no_of_students from student_courseenrollment where course_id IN (select course_id from student_courseaccessrole where user_id=\'"+user_id+"\') group by course_id"
        #Query to get course id and no of students enrolled in each course
        sql_cur.execute(query)
        result=sql_cur.fetchall()
        for row in result:              #Iterating over each course
                course_list=[]
                course_list=get_student_grade(row[0],db_sql,client,strquery,strquery2)           #Getting total grades of all students in a particular course
                if len(course_list)>0:    
                        result_list.append([str(row[0]),str(row[1]),str(course_list[0]),str(course_list[1])])             #Appending final result list
	print "DisConnecting from mySQL now"
        db_sql.close()
        client.close()
        return result_list
                
                
""" Description: Function to get average grades of all students in a particular course.This function is called by getall_course_grade().
    Input Parameters:
            course_id: id of course passed as a parameter by function getall_course_grades.
            db_sql: MySQL Database connection object
            client: MongoDB connection object
    Output Type : List
    Author: Sneha
    Date of creation:18 june 2015
"""

def get_student_grade(course_id,db_sql,client,strquery,strquery2):
        sum_grade=0
        count_student=0
        grade_list=[]
        course_name=course_id.split('/')                #Splitting course id to get course name
        c_name=course_name[1]
        sql_cur=db_sql.cursor()
        #query="select user_id,course_id from student_courseenrollment where course_id=\'"+course_id+"\'"
        #Query to get ids of students enrolled in a course
        sql_cur.execute(strquery,(str(course_id),))
        result=sql_cur.fetchall()
        for row in result:
                grade=get_student_course_grade2(row[0],c_name,db_sql,client,strquery2)          #Getting grade of each student in each course
                if grade==-1:                                   #If grading policy is not defined in a course
                        return []
                grade_list.append(grade)                                #Appending students grade to list
                sum_grade+=grade                        #Adding grades of all students
                count_student+=1                       #Counting no of students
        if count_student>0:
                avg_grade=sum_grade/count_student              #Finding average grade obtained in a course
        grade_list.sort(reverse=True)                   #Sorting students grade
        max_grade=grade_list[0]                 #Getting maximum grade in a course
        main_list=[]                            #Appending final result list
        main_list.append(avg_grade)
        main_list.append(max_grade)
        return main_list
        
""" Description: Function to get average grade of each student in a paricular course.This function is called by functions get_student_grade() and get_course_grade().
    Input Parameters:
            student_id: user_id of a student
            course_id: id of course for which grades are to be calculated
            db_mysql: MySQL Database connection object
            client: MongoDB connection object
    Output: Student total average
    Author: Samridhi
    Date of creation: 17 june 2015    
"""              
    

	
def get_student_course_grade2(student_id,course_id,db_mysql,client,strquery2):
	
	db_mongo=client.edxapp		#Getting the object for edxapp database of Mongo
	try:
                mongo_cur=db_mongo.modulestore.find({'_id.course':course_id,'_id.category':'course'},{'definition.data.grading_policy.GRADER':1,'_id':0}) #Query to get the grading policy of a partticular course
		
		try:
                        #strquery="Select grade,max_grade from courseware_studentmodule where max_grade is not null and grade is not null and student_id=\'"+str(student_id)+"\' and module_id=%s"    
			i=mongo_cur[0]
                        stud_avg_tot=0			#initializing the student total marks for the course as zero
                        list1=i['definition']['data']['grading_policy']['GRADER']		#Getting the GRADER list which stores the different formats and their weights in a course
                        for j in range(len(list1)):				#iterating over the formats
                                best_score_list=[]					#This list will store the final scores for the particular format
                                drop_count=list1[j]['drop_count']			#Gives number of droppable sections for that problem
                                type=list1[j]['type']				#Gives the type of the format i.e. Quiz, Final Exam etc.
                                weight=list1[j]['weight']			#Gives the weights of the formats 
                                min_count=list1[j]['min_count']	#Gives the minimum number of sections of that type present in the course
                                try:
                                        mongo_cur2=db_mongo.modulestore.find({'_id.course':course_id,'_id.category':'sequential','metadata.format':type,'metadata.graded':True},{'metadata':1,'definition.children':1})
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
                                                        child_id=list2[m]			#Getting the vertical id
                                                        arr=child_id.split('/')							#Splitting the vertical id to get the _id.name field for the vertical
                                                        vertical_id=arr[len(arr)-1]						#Getting vertical's _id.name 
                                                        mongo_cur3=db_mongo.modulestore.find({'_id.name':vertical_id,'_id.course':course_id,'_id.category':'vertical'},{'definition.children':1}).limit(1)
                                                        #query to get the vertical document with the _id.name as vertical id
							try:
								n=mongo_cur3[0]
                                                                list3=n['definition']['children']			#getting the children array for this vertical, consisiting of list of component ids
                                                                for o in range(len(list3)):					#Iterating over the list of component ids
                                                                        comp_id=list3[o]	#Getting the component id
                                                                        arr2=comp_id.split('/')				#Splitting the component id to get the _id.name field for the problem
                                                                        component_id=arr2[len(arr2)-1]		#Getting component's _id.name
                                                                        mongo_cur4=db_mongo.modulestore.find({'_id.name':component_id,'_id.course':course_id,'_id.category':'problem'},{'metadata.weight':1}).limit(1)
                                                                        #query to get the problem document with the _id.name as problem id and category as problem.
									try:
										p=mongo_cur4[0]
										
                                                                                problem_id=comp_id				#Getting the module_id for that problem
                                                                                mysql_cur=db_mysql.cursor()			#Getting MySQL cursor object
                                                                                #query="Select grade,max_grade from courseware_studentmodule where student_id=\'"+str(student_id)+"\' and module_id=\'"+problem_id+"\' and max_grade is not null and grade is not null" 
                                                                                #query=strquery+problem_id+"\'"
                                                                                #Query to get the grades for the student for that particular problem 
                                                                                try:
                                                                                        mysql_cur.execute(strquery2,(str(student_id),str(problem_id),))		#Executing query
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

""" Description: Function to get average grade of all students enrolled in a course.
    Input Parameters:
            course_name: name of the course for which grades are to be calculated.
    Output Type : List
    Author: Samridhi
    Date of creation:18 june 2015
"""
	
	
def get_course_grades(course_name):
        try:
                client=pymongo.MongoClient(ip_address,mongo_port) 	#Establishing MongoDB connection
        except:
                print "MongoDB connection not established"
                return HttpResponse("MongoDB connection not established")
        try:
		print "Connecting to mysql from get_course_grades"
                db_mysql=MySQLdb.connect(ip_address,sql_user,sql_pswd,database)		#Establishing MySQL connection
        except:
                print "MySQL connection not established"
                return HttpResponse("MySQL connection not established")
        results=[]
	query2="select a.id, a.username, b.course_id from auth_user as a, student_courseenrollment as b where a.id=b.user_id"        #Getting all students and their courses
        strquery2="Select grade,max_grade from courseware_studentmodule where max_grade is not null and grade is not null and student_id=%s and module_id=%s"    
	mysql_cur2=db_mysql.cursor()
	mysql_cur2.execute(query2)
	y=mysql_cur2.fetchall()
	for row in y:                                   
                str2=row[2]
                arr=str2.split('/')
                course_id=arr[1]
                if course_id==course_name:
                        stud_name=row[1]                        #Appending list
                        stud_grade=get_student_course_grade2(str(row[0]),course_name,db_mysql,client,strquery2)   #Getting score of each student
                        stud_id=row[0]
                        #if stud_grade==-1:
                                #stud_grade=0
                        
                        results.append([stud_name,stud_grade,stud_id])
	print "Disconneting from get_course_grades"
	db_mysql.close()
	client.close()
	return results

""" Description: Function to get average grade of a student in all the courses enrolled along with the course maximum and average grade.
    Input Parameters:
            student_id: id of the student.
    Output Type : List
    Author: Sneha
    Date of creation:21 june 2015
"""

def get_student_allcourses_grade(request,student_id):
        result_list=[]
        try:
		print "Connecting to mysql from get_student_allcourses_grade"
                db_sql=MySQLdb.connect(ip_address,sql_user,sql_pswd,database)  #establishing sql connection
        except:
                print "MySQL connection not established"
                return HttpResponse("MySQL connection not established")
        try:
                client=pymongo.MongoClient(ip_address,mongo_port)     #establishing mongodb connection
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
                c_id=row[0].split('/')
                course_name=c_id[1]
                if len(course_avg_list)>0:
                        student_grade=course_avg_list[2]
                        result_list.append([row[0],student_grade,course_avg_list[0],course_avg_list[1]])
                        
	print "Disconnecting from mysql in getstudent_allcourses_grade"
        db_sql.close()
        client.close()
        return render_to_response('newindex4.html',{'data':result_list})

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

def get_student_grade2(course_id,student_id,db_sql,client,strquery2,strquery):
        sum_grade=0
        count_student=0
        grade_list=[]
        course_name=course_id.split('/')                #Splitting course id to get course name
        c_name=course_name[1]
        sql_cur=db_sql.cursor()
        student_grade=0
        #query="select user_id,course_id from student_courseenrollment where course_id=\'"+course_id+"\'"   #Query to get ids of students enrolled in a course
        sql_cur.execute(strquery,(str(course_id),))
        result=sql_cur.fetchall()
        for row in result:
                grade=get_student_course_grade2(row[0],c_name,db_sql,client,strquery2)          #Getting grade of each student in each course
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





""" Description: Function to get quiz level grades of all students in a particular course.
    Input Parameters:
            course_name: id of course.
    Output Type : List
    Author: Sneha
    Date of creation:24 june 2015
"""



def getall_student_grades(request,course_name):
        count=1
        try:
                client=pymongo.MongoClient(ip_address,mongo_port) 	#Establishing MongoDB connection
        except:
                print "MongoDB connection not established"
                return HttpResponse("MongoDB connection not established")
        try:
		print "Connecting to mysql from getall_student_grades"
                db_mysql=MySQLdb.connect(ip_address,sql_user,sql_pswd,database)
        except:
                print "MySQL connection not established"                #Establishing MySQL connection
                return HttpResponse("MySQL connection not established")
        stud_grade=[]
        all_list=[]
        strquery="Select grade,max_grade from courseware_studentmodule where max_grade is not null and grade is not null and student_id=%s and module_id=%s"
        query="select a.id, a.username, a.email, b.course_id from auth_user as a, student_courseenrollment as b where a.id=b.user_id"
        #Query to retrieve the details of all students who have enrolled in any course
        mysql_cur2=db_mysql.cursor()
	mysql_cur2.execute(query)
	y=mysql_cur2.fetchall()
	for row in y:
                c_id=row[3].split('/')
                c_name=c_id[1]
                if course_name==c_name:         #Comparing course_id to get students enrolled in a particular course
                        stud_name=row[1]
                        stud_grade=get_student_course_grades3(str(row[2]),str(row[1]),str(row[0]),course_name,count,db_mysql,client,strquery)#Calling function to get quiz grades of each student
                        count+=1
                        all_list.append(stud_grade) #Appending student's grade list
        newlist1=[]
        newlist2=[]
        newlist1.append("id")
        newlist1.append("username")
        newlist1.append("email")
        for i in range(len(all_list[0][0])):
                newlist1.append(all_list[0][0][i])
                
        newlist2.append(all_list[0][1])
        for i in range(1,len(all_list)):
                newlist2.append(all_list[i])
        client.close()          #Closing MongoDB connection
	print "Disconnecting from mysql in getall_student_grades"
        db_mysql.close()        #Closing MySQL connection
        return render_to_response('report1.html',{'data':newlist1,'data1':newlist2})

        

               
                                  
                                  
                                  
                
                
               
        
	




""" Description: Function to get quiz level grades of each student in a paricular course.This function is called by functions getall_student_grades().
    Input Parameters:
            email: Email id of student passed to this function by getall_student_grades()
            stud_name:Username of student passed to this function by getall_student_grades() 
            student_id: user_id of a student
            course_id: id of course for which grades are to be calculated
            db_mysql: MySQL Database connection object
            client: MongoDB connection object
            strquery:Query passed to this function by getall_student_grades()
    Output Type: List
    Author: Samridhi
    Date of creation: 24 june 2015    
"""              
    

def get_student_course_grades3(email,stud_name,student_id,course_id,count,db_mysql,client,strquery):
        h_list=[]
	highchart_list=[]       #List to be returned for highcharts
	highchart_list2=[]       #List to be returned for highcharts
	highchart_list3=[]
	highchart_list.append('grade')
	highchart_list3.append(str(student_id))
	highchart_list3.append(stud_name)
	highchart_list3.append(email)
	db_mongo=client.edxapp		#Getting the object for edxapp database of MongoDB
	mongo_cur=db_mongo.modulestore.find({'_id.course':course_id,'_id.category':'course'},{'definition.data.grading_policy.GRADER':1,'_id':0})		#Query to get the grading policy of a partticular course
	try:
		i=mongo_cur[0]
		stud_avg_tot=0			
		list1=i['definition']['data']['grading_policy']['GRADER']		#Getting the GRADER list which stores the different formats and their weights in a course
		for j in range(len(list1)):      				#iterating over the formats
			best_score_list=[]					#This list will store the final scores for the particular format
			drop_count=list1[j]['drop_count']			#Gives number of droppable sections for that problem
			type=list1[j]['type']				#Gives the type of the format i.e. Quiz, Final Exam etc.
			short_label=list1[j]['short_label']
			weight=list1[j]['weight']			#Gives the weights of the formats 
			min_count=list1[j]['min_count']	#Gives the minimum number of sections of that type present in the course
			mongo_cur2=db_mongo.modulestore.find({'_id.course':course_id,'_id.category':'sequential','metadata.format':type,'metadata.graded':True},{'metadata':1,'definition.children':1})            
                        count_doc=db_mongo.modulestore.find({'_id.course':course_id,'_id.category':'sequential','metadata.format':type,'metadata.graded':True},{'metadata':1,'definition.children':1}).count()            
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
					mongo_cur3=db_mongo.modulestore.find({'_id.name':vertical_id,'_id.course':course_id,'_id.category':'vertical'},{'definition.children':1}).limit(1)
					#query to get the vertical document with the _id.name as vertical id
					n=mongo_cur3[0]			
					list3=n['definition']['children']                       #getting the children array for this vertical, consisiting of list of component ids
					for o in range(len(list3)):                                     #Iterating over the list of component ids
						comp_id=list3[o]  #Getting the component id
						arr2=comp_id.split('/')                         #Splitting the component id to get the _id.name field for the problem
						component_id=arr2[len(arr2)-1]          #Getting the component's _id.name
						mongo_cur4=db_mongo.modulestore.find({'_id.name':component_id,'_id.course':course_id,'_id.category':'problem'},{'metadata.weight':1}).limit(1)
						#query to get the problem document with the _id.name as problem id and category as problem.
						try:
							p=mongo_cur4[0]
							problem_id=comp_id                              #Getting the module_id for that problem
							mysql_cur=db_mysql.cursor()                     #Getting MySQL cursor object
							#query="Select grade,max_grade from courseware_studentmodule where student_id=\'"+student_id+"\' and module_id=\'"+problem_id+"\' and max_grade is not null and grade is not null" 
							#Query to get the grades for the student for that particular problem
							mysql_cur.execute(strquery,(str(student_id),str(problem_id),))                #Executing query
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
                                if count==1:
                                        if count_doc>1:
                                                highchart_list.append(str(short_label)+str(sequential_coun))
                                        else:
                                                highchart_list.append(str(short_label))
                                        highchart_list2.append(str(avg_score_sequential))
                                else:
                                        highchart_list2.append(str(avg_score_sequential))
				best_score_list.append(avg_score_sequential)		#Adding the sequential score to best_score_list
			best_score_list.sort(reverse=True)  #Sorting the scores list for that format in descending order
			sum_score_format=0			#Initializing sum score of format to 0
			for q in range(sequential_coun-drop_count):		#Getting the sum of best scores in the format
				sum_score_format+=best_score_list[q]
			if sequential_coun-drop_count>0:
                                avg_score_format=sum_score_format/(sequential_coun-drop_count)		#Getting average score of the format      
                                if sequential_coun-drop_count>1:
                                        if count==1:
                                                highchart_list.append(str(short_label)+'Avg')
                                                highchart_list2.append(str(avg_score_format))
                                        else:
                                                highchart_list2.append(str(avg_score_format))
                                stud_avg_tot+=avg_score_format*weight
                        else:
                                avg_score_format=0
					#Getting total student average score
                
                if len(highchart_list2)>0:
                        if count==1:
                                #highchart_list.append('Total')
                                highchart_list2.append(str(stud_avg_tot))
                        else:
                                highchart_list2.append(str(stud_avg_tot))
	except:
		highchart_list2=[]
	highchart_list3.append(highchart_list2[(len(highchart_list2)-1)])
	
	for k in range((len(highchart_list2)-1)):
                highchart_list3.append(highchart_list2[k])
                
	if count==1:
                h_list.append(highchart_list)
                h_list.append(highchart_list3)
                return h_list
        else:
                return highchart_list3

""" Description: Function to get grading policy of a course
    Input Parameters:
            course_name: name of course for which grading policy is required (ex. ME209) 
    Output Type: List
    Author: Samridhi
    Date of creation: 24 june 2015    
"""              
def get_grading_policy(request, course_name):
        resultlist={}
        try:
                client=pymongo.MongoClient(ip_address,mongo_port) 	#Establishing MongoDB connection
        except:
                print "MongoDB connection not established"
                return HttpResponse("MongoDB connection not established")
        db_mongo=client.edxapp
        mongo_cur=db_mongo.modulestore.find({"_id.course":course_name,"_id.category":"course"},{"metadata.start":1,"metadata.end":1,"metadata.enrollment_start":1,"metadata.enrollment_end":1,"metadata.display_name":1,"definition.data.grading_policy":1})
        i=mongo_cur[0]
        course_start=i['metadata']['start']
        c_start=course_start.split('T')
        course_end=i['metadata']['end']
        c_end=course_end.split('T')
        course_reg_start=i['metadata']['enrollment_start']
        c_reg_start=course_reg_start.split('T')
        course_reg_end=i['metadata']['enrollment_end']
        c_reg_end=course_reg_end.split('T')
        id_org=i['_id']['org']
        id_course=i['_id']['course']
        id_name=i['_id']['name']
        course_disp_name=i['metadata']['display_name']
        course_id=id_org+"/"+id_course+"/"+id_name
        resultlist["course_start"]=c_start[0];
        resultlist["course_end"]=c_end[0];
        resultlist["course_reg_start"]=c_reg_start[0];
        resultlist["course_reg_end"]=c_reg_end[0];
        resultlist["course_id"]=course_id;
        resultlist["course_display_name"]=course_disp_name;
        grade_list=i['definition']['data']['grading_policy']['GRADER']
        grader_result_list=[]
        
        for j in range(len(grade_list)):
                grader_result_dict={}
                min_count=grade_list[j]['min_count']
                drop_count=grade_list[j]['drop_count']
                short_label=grade_list[j]['short_label']
                display_name=grade_list[j]['type']
                grader_result_dict["min_count"]=min_count
                grader_result_dict["drop_count"]=drop_count
                grader_result_dict["short_label"]=short_label
                grader_result_dict["type"]=display_name
                grader_result_list.append(grader_result_dict)
        resultlist["grader"]=grader_result_list
        mongo_cur=db_mongo.modulestore.find({"_id.course":course_name,"_id.category":"course"},{"definition.data.grading_policy":1})
        grade_cutoffs=i['definition']['data']['grading_policy']['GRADE_CUTOFFS']
        max_grade=1
        grade_cutoffs_dict={}
        for k,v in grade_cutoffs.iteritems():
                label=k
                grade_cutoffs[k]=v
        resultlist["grade_cutoffs"]=grade_cutoffs
        print resultlist
        return resultlist
        #return render_to_response('report2.html',{'data':resultlist})
def get_quiz_grades(request,course_name,quiz_name):
        course_name="ME209"
        quiz_name="077a0ef1bbe546abb4646c90d3475725"
        #arr=quiz_id.split("/")
        try:
                client=pymongo.MongoClient(ip_address,mongo_port) 	#Establishing MongoDB connection
        except:
                print "MongoDB connection not established"
                return HttpResponse("MongoDB connection not established")
        try:
		print "Connecting to mysql in get_quiz_grades"
                db_mysql=MySQLdb.connect(ip_address,sql_user,sql_pswd,database)
        except:
                print "MySQL connection not established"                #Establishing MySQL connection
                return HttpResponse("MySQL connection not established")
        db_mongo=client.edxapp
        mongo_cur2=db_mongo.modulestore.find({'_id.course':'ME209','_id.category':'sequential','_id.name':quiz_name,'metadata.graded':True},{'metadata':1,'definition.children':1})            
        try:
                k=mongo_cur2[0]				
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
			mongo_cur3=db_mongo.modulestore.find({'_id.name':vertical_id,'_id.course':course_name,'_id.category':'vertical'},{'definition.children':1}).limit(1)
			#query to get the vertical document with the _id.name as vertical id
			n=mongo_cur3[0]			
			list3=n['definition']['children']                       #getting the children array for this vertical, consisiting of list of component ids
			for o in range(len(list3)):                                     #Iterating over the list of component ids
				comp_id=list3[o]  #Getting the component id
				arr2=comp_id.split('/')                         #Splitting the component id to get the _id.name field for the problem
				component_id=arr2[len(arr2)-1]          #Getting the component's _id.name
				mongo_cur4=db_mongo.modulestore.find({'_id.name':component_id,'_id.course':course_name,'_id.category':'problem'},{'metadata.weight':1}).limit(1)
				#query to get the problem document with the _id.name as problem id and category as problem.
				try:
                        		p=mongo_cur4[0]
					problem_id=comp_id                              #Getting the module_id for that problem
					mysql_cur=db_mysql.cursor()                     #Getting MySQL cursor object
					query="Select grade,max_grade from courseware_studentmodule where student_id=70 and module_id=\'"+problem_id+"\' and max_grade is not null and grade is not null" 
					#Query to get the grades for the student for that particular problem
					mysql_cur.execute(query)                #Executing query
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
        except:
                print"in excpt"
	print "DisConnecting to mysql in get_quiz_grades"
        db_mysql.close()        #Closing MySQL connection
        print"hello",avg_score_sequential
        return HttpResponse(avg_score_sequential)
