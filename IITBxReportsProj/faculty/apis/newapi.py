from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext,loader
from django.http import HttpResponse
from pymongo import MongoClient
from django.utils.safestring import mark_safe
#from address import ip_address
#from address import mongo_port
#from address import sql_user
#from address import sql_pswd
#from address import database

import collections
import pymongo			
import MySQLdb
#import xlwt
ip_address="10.105.24.33"
mongo_port=27017
sql_user="root"
sql_pswd="edx"
database="edxapp"
"""Description:Function to get grades of a student in each exam(quiz,mid term,final exam etc.).It returns a list of grsdes scored in all exams by a student
   Input Parameters:
       student_id :User_id of student
       course_id : id of course
   Output Type : List
   Author: Samridhi
   Date of creation: 17 june 2015
"""
"""def get_each_student_grade(student_id,course_id):
        print "student_id=",student_id
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
                                print k['_id']['name']
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
                                print "avg_score_sequential=",avg_score_sequential
				sub_results_list.append([sequential_coun,avg_score_sequential])			
				highchart_list.append([str(short_label),str(sequential_coun),str(avg_score_sequential)])
				best_score_list.append(avg_score_sequential)		#Adding the sequential score to best_score_list
			best_score_list.sort(reverse=True)  #Sorting the scores list for that format in descending order
			print "best_score_list=",best_score_list
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
	print highchart_list
	return highchart_list"""


def get_each_student_grade(student_id,course_id):
        #print "student_id=",student_id
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
	mongo_cur=db_mongo.modulestore.find({'_id.course':course_id,'_id.category':'course'})		#Query to get the grading policy of a partticular course
	
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
                        chapters_list=i['definition']['children']
			#mongo_cur2=db_mongo.modulestore.find({'_id.course':course_id,'_id.category':'sequential','metadata.format':type,'metadata.graded':True},{'metadata':1,'definition.children':1})            
			#Query to find the different sequentials having the format 'type' 
			sequential_coun=0		#intializing sequential count to zero
                        for g in chapters_list:
                                        chapter_full_id=g
                                        arr=g.split("/")
                                        chapter_id=arr[5]
                                        mongo_cur7=db_mongo.modulestore.find({'_id.course':course_id,'_id.category':'chapter','_id.name':chapter_id}) #Getting a course
                                        h=mongo_cur7[0]
                                        list_sequentials=h['definition']['children']
                                        for j in list_sequentials:
                                                sequential_full_id=j
                                                arr2=j.split("/")
                                                sequential_id=arr2[5]
                                                try:
                                                        mongo_cur2=db_mongo.modulestore.find({'_id.course':course_id,'_id.category':'sequential','_id.name':sequential_id,'metadata.format':type,'metadata.graded':True},{'metadata':1,'definition.children':1})
                                                        k=mongo_cur2[0]
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
                                                        #print "avg_score_sequential=",avg_score_sequential
                                                        sub_results_list.append([sequential_coun,avg_score_sequential])			
                                                        highchart_list.append([str(short_label),str(sequential_coun),str(avg_score_sequential)])
                                                        best_score_list.append(avg_score_sequential)		#Adding the sequential score to best_score_list
                                                except:
                                                        continue
			best_score_list.sort(reverse=True)  #Sorting the scores list for that format in descending order
			#print "best_score_list=",best_score_list
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
