from pymongo import MongoClient
from django.http import HttpResponse
from django.template import Context, Template
import bson
import traceback

def get_all_courses_size(host, port, user, password):
    ''' Calculates size of each course on disk. 
        
        Args:
            host : server ip address.
            port : server port number.
            user : user name for connecting with mongo database on server.
            password : password for connecting with mongo database on server.
        
        Returns:
            size of each course on disk
        
    '''
    print "Hello Disk api"    
    # Dictionary used for storing course id as key and total course size
    # in bytes as value
    total_course_size = dict()
    
    # Dictionary used for storing course id as key and size of course in
    # modulestore collection in bytes as value
    module_size = dict()
    
    # Dictionary used for storing course id as key and size of course in
    # fs.files collection in bytes as value
    files_size = dict()
    
    # Dictionary used for storing course id as key and size of course in
    # fs.chunks collection in bytes as value
    chunks_size = dict()
    
    # Dictionary used for storing course id as key and size of course in
    # contents collection in bytes as value
    contents_size = dict()
    
    # Dictionary used for storing course number as key and course id as 
    # value
    course_info = dict()
    
    try:
        try:		
            # Establish connection with server
            connection = MongoClient(host, port)
        except:
            mongoserver_uri = "mongodb://" + user + ":" + password + "@" + host + ":" + str(port)
            # Establish connection with server
            connection = MongoClient(host= mongoserver_uri)
    except:
        print "diskapi:",traceback
    try:
        # Select database edxapp
        database = connection.edxapp
        
        # Query on modulestore collection
        cursor = database.modulestore.find({"_id.category": "course"})    
        # Following loop is used for getting course number and course id and
        # storing it in course_info
        for data in cursor:
            course_number = data["_id"]["course"]
            course_id = data["definition"]["data"]["wiki_slug"]
            
            # Format of "course id" is InstitutionName.CourseNumber.CourseRun
            # which is changed to InstitutionName/CourseNumber/CourseRun using
            # "split()" function
            lst_split = course_id.split(".")
            if course_id != "":
                course_id = lst_split[0] + "/" + lst_split[1] + "/" + lst_split[2]
            
            course_info[course_number] = course_id
    except:
        print "diskapi:",traceback
    
    try:
        # Query on modulestore collection
        cursor = database.modulestore.find({"_id.course": {"$exists": True}})
        
        # Following loop is for getting size of course in modulestore collection
        # and store it in module_size
        for data in cursor:
            course_num = data["_id"]["course"]
            
            if course_info[course_num] in module_size :
                module_size[course_info[course_num]] += len(bson.BSON.encode(data))
            else:
                module_size[course_info[course_num]] = len(bson.BSON.encode(data))    
    except:
        print "diskapi:",traceback
    
    try:
        # Query on fs.files collection
        cursor = database.fs.files.find({"_id.course": {"$exists": True}})
        
        # Following loop is for getting size of course in fs.files collection 
        # and store it in files_size	
        for data in cursor:
            course_num = data["_id"]["course"]
            
            if course_info[course_num] in files_size:
                files_size[course_info[course_num]] += len(bson.BSON.encode(data))
            else:
                files_size[course_info[course_num]] = len(bson.BSON.encode(data))	
    except:
        print "diskapi:",traceback
    
    try:
        # Query on fs.chunks collection
        cursor = database.fs.chunks.find({"files_id.course": {"$exists": True }})
        
        # Following loop is for getting size of course in fs.chunks collection
        # and store it in chunks_size
        for data in cursor:
            course_num = data["files_id"]["course"]
            
            if course_num != "" :
                if course_info[course_num] in chunks_size:
                    chunks_size[course_info[course_num]] += len(bson.BSON.encode(data))
                else:
                    chunks_size[course_info[course_num]] = len(bson.BSON.encode(data))
    except:
        print "diskapi:",traceback
    
    try:
        # Select database cs_comments_service_development			
        database = connection.cs_comments_service_development			
        
        # Query on contents collection
        cursor = database.contents.find({"course_id": {"$exists": True}})
        
        # Following loop is for getting size of course in contents collection
        # and store it in contents_size
        for data in cursor:
            course_id = data["course_id"]
            
            if course_id != "" :
                if course_id in contents_size:
                    contents_size[course_id] += len(bson.BSON.encode(data))
                else:
                    contents_size[course_id] = len(bson.BSON.encode(data))
    except:
        print "diskapi:",traceback
    
    # Following loop is for getting total course size and storing it in 
    # total_course_size
    for key in course_info:
		
        # Initialize dummy variable
        size = 0
        
        value = course_info[key]
        
        if value in module_size:
            size = size + module_size[value]
        if value in files_size:
            size = size + files_size[value]
        if value in chunks_size:
            size = size + chunks_size[value]
        if value in contents_size:
            size = size + contents_size[value]
        
        total_course_size[value] = size
        print value, total_course_size[value]
    
    try:
        # Close connection with server
        connection.close()
    except:
        print "diskapi:",traceback
    return total_course_size
