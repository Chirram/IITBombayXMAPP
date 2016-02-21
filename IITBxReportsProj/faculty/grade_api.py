from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext,loader
from django.http import HttpResponse
from pymongo import MongoClient
import collections
import pymongo			
import MySQLdb
def get_student_course_grades(request,student_id,course_id):#function to get the total marks of a student in a particular course
	results={}		#A dictionary to store the final results
	sub_results={}		#A dictionary which shall be embedded within the results dictionary
	results_list=[]		#A list to store the final results
	sub_results_list=[]		#A list which shall be embedded within the results_list list
	client=pymongo.MongoClient("10.105.24.33",27017) 	#Establishing MongoDB connection
	db_mysql=MySQLdb.connect("10.105.24.33","edx","","edxapp")
	db_mongo=client.edxapp		#Getting the object for edxapp database of Mongo
	mongo_cur=db_mongo.modulestore.find({'_id.course':course_id,'_id.category':'course'},{'definition.data.grading_policy.GRADER.':1,'_id':0})		#Query to get the grading policy of a partticular course
	for i in mongo_cur:			#iterating over the documents returned by above query, this query will actually return only one document
		stud_avg_tot=0			#initializing the student total marks for the course as zero
		list=i['definition']['data']['grading_policy']['GRADER']		#Getting the GRADER list which stores the different formats and their weights in a course
		for j in range(len(list)):				#iterating over the formats
			best_score_list=[]					#This list will store the final scores for the particular format
			drop_count=i['definition']['data']['grading_policy']['GRADER'][j]['drop_count']			#Gives number of droppable sections for that problem
			type=i['definition']['data']['grading_policy']['GRADER'][j]['type']				#Gives the type of the format i.e. Quiz, Final Exam etc.
			weight=i['definition']['data']['grading_policy']['GRADER'][j]['weight']			#Gives the weights of the formats 
			min_count=i['definition']['data']['grading_policy']['GRADER'][j]['min_count']	#Gives the minimum number of sections of that type present in the course
			sub_results={}			#initializing the sub_results to an empty dictionary
			sub_results_list=[]		#initializing the sub_results to an empty list
			mongo_cur2=db_mongo.modulestore.find({'_id.course':course_id,'_id.category':'sequential','metadata.format':type,'metadata.graded':True},{'metadata':1,'definition.children':1})
                        
			#Query to find the different sequentials having the format 'type' 
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
					vertical_id=arr[len(arr)-1]						#Storing the vertical id 
					mongo_cur3=db_mongo.modulestore.find({'_id.name':vertical_id,'_id.course':course_id,'_id.category':'vertical'},{'definition.children':1}).limit(1)
					#query to get the vertical document with the _id.name as vertical id
					for n in mongo_cur3:			#This for loop will run only once, for the no of documents returned by the above query is 1 
                                                
						list3=n['definition']['children']			#getting the children array for this vertical, consisiting of list of component ids
						for o in range(len(list3)):					#Iterating over the list of component ids
							comp_id=n['definition']['children'][o]	#Getting the component id
							arr2=comp_id.split('/')				#Splitting the component id to get the _id.name field for the problem
							component_id=arr2[len(arr2)-1]		#Storing the component id
							mongo_cur4=db_mongo.modulestore.find({'_id.name':component_id,'_id.course':course_id,'_id.category':'problem'},{'metadata.weight':1}).limit(1)
							#query to get the problem document with the _id.name as problem id and category as problem.
							for p in mongo_cur4:				#This for loop will run only once, for the no of documents returned by the above query is 1
								problem_id=comp_id				#Getting the module_id for that problem
								
								mysql_cur=db_mysql.cursor()			#Getting MySQL cursor object
								query="Select grade,max_grade from courseware_studentmodule where student_id=\'"+student_id+"\' and module_id=\'"+problem_id+"\' and max_grade is not null and grade is not null" 
								#Query to get the grades for the student for that particular problem
								mysql_cur.execute(query)		#Executing query
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
                                                                                weight_of_problem=0
                                                                        sum_tot_prob_score+=weight_of_problem
                                                                
                                					
                                if sum_tot_prob_score>0:
					avg_score_sequential=sum_prob_score_obt/sum_tot_prob_score		#Calculating avg score of this sequential
                                else:
                                        avg_score_sequential=0
                                
                                sub_results[sequential_coun]=avg_score_sequential			#Appending the results to dictionary
				l=[]
				l.append(sequential_coun)
				l.append(avg_score_sequential)
				sub_results_list.append(l)			#Appending the results to list
				best_score_list.append(avg_score_sequential)		#Adding the sequential score to best_score_list
			results[type]=sub_results			
			l=[]
			l.append(type)
			l.append(sub_results_list)
			best_score_list.sort(reverse=True)  #Sorting the scores list for that format in descending order
			sum_score_format=0			#Initializing sum score of format to 0
			for q in range(sequential_coun-drop_count):		#Getting the sum of best scores in the format
				sum_score_format+=best_score_list[q]
			if sequential_coun-drop_count>0:
                                avg_score_format=sum_score_format/(sequential_coun-drop_count)		#Getting average score of the format
                                sub_results['Avg']=avg_score_format			#Appending values to dictionary
                                results[type]=sub_results
                                l=[]
                                l.append('Avg')
                                l.append(avg_score_format)
                                sub_results_list.append(l)				#Appending values to list
                                l=[]
                                l.append(type)
                                l.append(sub_results_list)
                                results_list.append(l)
                                stud_avg_tot+=avg_score_format*weight
                        else:
                                avg_score_format=0
					#Getting total student average score
                if len(results_list)>0:
                        sub_results={}
                        sub_results[1]=stud_avg_tot			#Appending final results in dictionary
                        results["total"]=sub_results
                        l=[]
                        l.append(1)
                        l.append(stud_avg_tot)
                        sub_results_list=[]
                        sub_results_list.append(l)			#Appending final results in list
                        l=[]
                        l.append("Total")
                        l.append(sub_results_list)
                        results_list.append(l)
		client.close()
		db_mysql.close()
	return render_to_response('index.html',{'data':results_list})
def getall_course_grades(user_id):
        result_list=[]
        db_sql=MySQLdb.connect(host='10.105.24.33',user='root',passwd='edx',db='edxapp')        #Connecting SQL
        sql_cur=db_sql.cursor()
        query="select course_id,count(user_id) as no_of_students from student_courseenrollment where course_id IN (select course_id from student_courseaccessrole where user_id=\'"+user_id+"\') group by course_id"
        #Query to get course id and no of students enrolled in each course
        sql_cur.execute(query)
        result=sql_cur.fetchall()
        for row in result:              #Iterating over each course
                course_list=[]
                course_list=get_student_grade(row[0])           #Getting total grades of all students in a particular course
                if len(course_list)>0:
                        result_sub_list=[]
                        result_sub_list.append(str(row[0]))             #Appending the result sub list
                        result_sub_list.append(str(row[1]))
                        result_sub_list.append(str(course_list[0]))
                        result_sub_list.append(str(course_list[1]))     
                        result_list.append(result_sub_list)             #Appending final result list
        db_sql.close()
        #return HttpResponse(result_list)
        return result_list                
                


def get_student_grade(course_id):
        sum_grade=0
        count_student=0
        grade_list=[]
        course_name=course_id.split('/')                #Splitting course id to get course name
        c_name=course_name[1]
        db_sql=MySQLdb.connect(host='10.105.24.33',user='root',passwd='edx',db='edxapp')
        sql_cur=db_sql.cursor()
        query="select user_id,course_id from student_courseenrollment where course_id=\'"+course_id+"\'"
        #Query to get ids of students enrolled in a course
        sql_cur.execute(query)
        result=sql_cur.fetchall()
        for row in result:
                grade=get_student_course_grade2(row[0],c_name)          #Getting grade of each student in each course
                if grade==-1:                                   #If grading policy is not defined in a course
                        return []
                grade_list.append(grade)                                #Appending students grade to list
                sum_grade+=grade                        #Adding grades of all students
                count_student+=1                       #Counting no of students
        avg_grade=sum_grade/count_student              #Finding average grade obtained in a course
        grade_list.sort(reverse=True)                   #Sorting students grade
        max_grade=grade_list[0]                 #Getting maximum grade in a course
        main_list=[]                            #Appending final result list
        main_list.append(avg_grade)
        main_list.append(max_grade)
        return main_list
        
                
        

	
def get_student_course_grade2(student_id,course_id):#function to get the total marks of a student in a particular course
	results={}		#A dictionary to store the final results
	sub_results={}		#A dictionary which shall be embedded within the results dictionary
	results_list=[]		#A list to store the final results
	sub_results_list=[]		#A list which shall be embedded within the results_list list
	client=pymongo.MongoClient("10.105.24.33",27017) 	#Establishing MongoDB connection
	db_mongo=client.edxapp		#Getting the object for edxapp database of Mongo
        db_mysql=MySQLdb.connect("10.105.24.33","root","edx","edxapp")
	try:
                
                mongo_cur=db_mongo.modulestore.find({'_id.course':course_id,'_id.category':'course'},{'definition.data.grading_policy.GRADER.':1,'_id':0})		#Query to get the grading policy of a partticular course
                for i in mongo_cur:			#iterating over the documents returned by above query, this query will actually return only one document
                        stud_avg_tot=0			#initializing the student total marks for the course as zero
                        list=i['definition']['data']['grading_policy']['GRADER']		#Getting the GRADER list which stores the different formats and their weights in a course
                        for j in range(len(list)):				#iterating over the formats
                                best_score_list=[]					#This list will store the final scores for the particular format
                                drop_count=i['definition']['data']['grading_policy']['GRADER'][j]['drop_count']			#Gives number of droppable sections for that problem
                                type=i['definition']['data']['grading_policy']['GRADER'][j]['type']				#Gives the type of the format i.e. Quiz, Final Exam etc.
                                weight=i['definition']['data']['grading_policy']['GRADER'][j]['weight']			#Gives the weights of the formats 
                                min_count=i['definition']['data']['grading_policy']['GRADER'][j]['min_count']	#Gives the minimum number of sections of that type present in the course
                                sub_results={}			#initializing the sub_results to an empty dictionary
                                sub_results_list=[]		#initializing the sub_results to an empty list
                                try:
                                        mongo_cur2=db_mongo.modulestore.find({'_id.course':course_id,'_id.category':'sequential','metadata.format':type,'metadata.graded':True},{'metadata':1,'definition.children':1})
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
                                                        vertical_id=arr[len(arr)-1]						#Storing the vertical id 
                                                        mongo_cur3=db_mongo.modulestore.find({'_id.name':vertical_id,'_id.course':course_id,'_id.category':'vertical'},{'definition.children':1}).limit(1)
                                                        #query to get the vertical document with the _id.name as vertical id
                                                        for n in mongo_cur3:			#This for loop will run only once, for the no of documents returned by the above query is 1 
                                                                list3=n['definition']['children']			#getting the children array for this vertical, consisiting of list of component ids
                                                                for o in range(len(list3)):					#Iterating over the list of component ids
        
                                                                        comp_id=n['definition']['children'][o]	#Getting the component id
                                                                        arr2=comp_id.split('/')				#Splitting the component id to get the _id.name field for the problem
                                                                        component_id=arr2[len(arr2)-1]		#Storing the component id
                                                                        mongo_cur4=db_mongo.modulestore.find({'_id.name':component_id,'_id.course':course_id,'_id.category':'problem'},{'metadata.weight':1}).limit(1)
                                                                        #query to get the problem document with the _id.name as problem id and category as problem.
                                                                        for p in mongo_cur4:				#This for loop will run only once, for the no of documents returned by the above query is 1
                                                                                
                                                                                problem_id=comp_id				#Getting the module_id for that problem
                                                                                
                                                                                mysql_cur=db_mysql.cursor()			#Getting MySQL cursor object
                                                                                query="Select grade,max_grade from courseware_studentmodule where student_id=\'"+str(student_id)+"\' and module_id=\'"+problem_id+"\' and max_grade is not null and grade is not null" 
                                                                                #Query to get the grades for the student for that particular problem
                                                                                
                                                                                try:
                                                                                        mysql_cur.execute(query)		#Executing query
                                                                                except:
                                                                                        print"QUERY MYSQL EXCEPT"
                                                                                
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
                                                                                                weight_of_problem=0
                                                                                      
                                                                                        sum_tot_prob_score+=weight_of_problem
                                                                                      
                                                                                
                                                                                
                                                
                                                if sum_tot_prob_score>0:
                                                        avg_score_sequential=sum_prob_score_obt/sum_tot_prob_score		#Calculating avg score of this sequential
                                                
                                                sub_results[sequential_coun]=avg_score_sequential			#Appending the results to dictionary
                                                l=[]
                                                l.append(sequential_coun)
                                                l.append(avg_score_sequential)
                                                sub_results_list.append(l)			#Appending the results to list
                                                best_score_list.append(avg_score_sequential)		#Adding the sequential score to best_score_list
                                except:
                                        
                                        return -1
                                
                                results[type]=sub_results
                                l=[]
                                l.append(type)
                                l.append(sub_results_list)
                                best_score_list.sort(reverse=True)  #Sorting the scores list for that format in descending order
                                sum_score_format=0			#Initializing sum score of format to 0
                                for q in range(sequential_coun-drop_count):		#Getting the sum of best scores in the format
                                        sum_score_format+=best_score_list[q]
                                
                                if sequential_coun-drop_count > 0 :
                                        
                                        avg_score_format=sum_score_format/(sequential_coun-drop_count)		#Getting average score of the format
                                        sub_results['Avg']=avg_score_format			#Appending values to dictionary
                                        results[type]=sub_results
                                        l=[]
                                        l.append('Avg')
                                        l.append(avg_score_format)
                                        sub_results_list.append(l)				#Appending values to list
                                        l=[]
                                        l.append(type)
                                        l.append(sub_results_list)
                                        results_list.append(l)
                                        stud_avg_tot+=avg_score_format*weight		#Getting total student average score
                                        
                                else:
                                        
                                        avg_score_format=0
                        
                        if len(results_list)>0:
                                sub_results={}
                                sub_results[1]=stud_avg_tot			#Appending final results in dictionary
                                results["total"]=sub_results
                                l=[]
                                l.append(1)
                                l.append(stud_avg_tot)
                                sub_results_list=[]
                                sub_results_list.append(l)			#Appending final results in list
                                l=[]
                                l.append("Total")
                                l.append(sub_results_list)
                                results_list.append(l)
                        client.close()
                        db_mysql.close()
        except:
                
                return -1
        
	
        
        return stud_avg_tot


	
	
def get_course_grades(request,course_name):
	db_mysql=MySQLdb.connect("10.105.24.33","edx","","edxapp")		#Establishing MySQL connection
	mysql_cur=db_mysql.cursor()			#Getting MySQL cursor object
	results=[]
	query="select id, user_id, course_id from student_courseenrollment" #Getting all student ids enrolled in a course
	mysql_cur.execute(query)
	x=mysql_cur.fetchall()
	results=[]
	list_student_id=[]
	for row in x:                                           #For appending student ids in a list 
		str2=row[2]
		arr=str2.split('/')                             #Splitting course id
		course_id=arr[1]                                
		if(course_id==course_name):
			list_student_id.append(row[1])                  #Appending list of students in a course
	sum_stud_grade=0
	coun_stud=0
	results=[]
	for i in list_student_id:                               #Iterating over each student
		stud_grade=get_student_course_grade2(str(i),course_name)                #Getting score of each student
		query2="select name from auth_userprofile where user_id=\'"+str(i)+"\'"         #Getting names of students
		mysql_cur2=db_mysql.cursor()
		mysql_cur2.execute(query2)
		y=mysql_cur2.fetchall()
		for row in y:                                   
			stud_name=row[0]                        #Appending list
			l=[]
			l.append(stud_name)
			l.append(stud_grade)
			l.append(i)
			results.append(l)
	db_mysql.close()
	return render_to_response('index2.html',{'data':results})

	

