# Imports
from pymongo import MongoClient
from django.http import HttpResponse
from django.template import Context, Template
import bson
import unicodedata


'''
   Global variables
'''

# Dictionary to store course number as key and course id as value
course_info = dict()
# Server ip address
server_ip = "10.105.24.33"
# Server port
port = 27017

'''
   Following function is for verification
   whether size of data returned is correct or not
'''   
def anjaytest():
    print("testok")
    return 1	
def verify(request):
    
    try:
        # Establish connection with mongo database server
        connection = MongoClient(server_ip, port)
    except:
	    print ("Connection could not be established with server")    
    
    try:
        # Select database edxapp
        database = connection.edxapp
    except:
	    print ("Unable to select database edxapp")    
    
    try:
        # Query on modulestore collection of database
        cursor = database.modulestore.find( { "_id.course":"CS000" , "_id.category" : "about" } )
    except:
	    print ("Unable to query modulestore collection")    
    
    # Intialize variable for calculating size of data
    size = 0
    
    # Following loop iterates through cursor object to calculate size of data
    for record in cursor:
        # Add size of each record in size variable
        size += len(bson.BSON.encode(record))
    
    # HTML element for displaying size of data
    html = "<html> <body> Size is , %d bytes</body> </html>" % size
    
    try:
        # Close server connection
        connection.close()
    except:
	    print ("Connection could not be closed with server at ", server_id, ":", port)
    return HttpResponse(html)


'''
   Following function is for getting 
   amount of all data stored coursewise in bytes
'''   	
def get_size_all_course(request):
    print("------------get_size_all_course() called--------")
    global course_info
    
    try:
        # Establish connection with mongo database server
        connection = MongoClient(server_ip, port)
    except:
	    print ("Connection could not be established with server at ", server_ip, ":", port)
    
    try:
        # Select database edxapp
        database = connection.edxapp
    except:
	    print ("Unable to select database edxapp")
	    
    try:    
        # Query on modulestore collection of database
        cursor = database.modulestore.find( { "_id.category" : "course"} )
    except:
	    print ("Unable to query modulestore collection")
	    	
    '''
       Following loop is for storing "course number" and "course id" in "course_info" dictionary
       with "course number" as key and "course id" as value of each course
    '''
    print ("storing mongo data in dictionary now")
    for record in cursor:
        print("inside loop")
		
		# Type of record["_id"]["course"] is "unicode" which is changed to "ascii"
        course_number = record["_id"]["course"]
        print("course num = ",course_number)
        
        course_id = ""
        course_id = record["definition"]["data"]["wiki_slug"]
        print("course id = ",course_id)
        # Format of "course id" is InstitutionName.CourseNumber.CourseRun which is changed to InstitutionName/CourseNumber/CourseRun using "split()" function
        lst_split = []
        print("attempt split")
        lst_split = course_id.split(".")
        print("course id split list:")
        if course_id != "":
            print("recombine split with dash")
            course_id = lst_split[0]+"/"+lst_split[1]+"/"+lst_split[2]
            print("split done")
        else:
            print("course id was blank")
        print("new course id = ",course_id)
        # Store data in "course_info" dictionary
        course_info[course_number]= course_id
        print("loop again now")
    
    # Close server connection            
    connection.close()
	# Get size of each course from "modulestore" collection of "edxapp" database and store in "modulestore_course_size" dictionary with key as "course number" and value as "size of course in modulestore collection"
    modulestore_course_size = get_modulestore_course_size()
    
    # Get size of each course from "fs.files" collection of "edxapp" database and store in "fs_files_course_size" dictionary with key as "course number" and value as "size of course in fs.files collection"
    fs_files_course_size = get_fs_files_course_size()
    
    # Get size of each course from "fs.chunks" collection of "edxapp" database and store in "fs_chunks_course_size" dictionary with key as "course number" and value as "size of course in fs.chunks collection"
    fs_chunks_course_size = get_fs_chunks_course_size()
    
    # Get size of each course from "contents" collection of "cs_comments_service_development" database and store in "contents_course_size" dictionary with key as "course number" and value as "size of course in contents collection"
    contents_course_size = get_contents_course_size()
    
    # Store total size of course in "total_course_size" dictionary with key as "course number" and "size of course" as key 
    total_course_size = dict()
    
    # Following loop stores total size of course in "total_course_size" dictionary
    for key in modulestore_course_size:
		
		# Summation of size obtained from "modulestore", "fs.files", "fs.chunks" and "contents" collections
        size = modulestore_course_size[key] + fs_files_course_size[key] + fs_chunks_course_size[key] + contents_course_size[key]
        
        # Store size in "total_course_size" dictionary
        total_course_size[key] = size
    for key in total_course_size:
        print (key, total_course_size[key])
    
    # Below code displays course number and course size on html page
    headings = ["CourseNumber", "Size in bytes"]    
    rows = [ [ key , total_course_size[key] ] for key in total_course_size  ]    
    #return HttpResponse(html.render(Context(dict(data = rows, headings = headings))))
    print("returning mongo data now")
    return total_course_size

'''
   Following function gets size of course stored in "modulestore" collection
   of "edxapp" database
'''
def get_modulestore_course_size():
    
    try:
        # Establish connection with mongo database server
        connection = MongoClient(server_ip, port)
    except:
	    print ("Connection could not be established with server at ", server_ip, ":", port)
    
    try:
        # Select database
        database = connection.edxapp
    except:
	    print ("Unable to select database edxapp")	
    
    # Stores size of course in "modulestore_course_size" with key as "course number" and value as "size"
    modulestore_course_size = dict()
    
    # Following loop calculates size of each course and stores in "modulestore_course_size"  dictionary
    for key in course_info:
        
        try:
            # Query "modulestore" collection of "edxapp" database
            cursor = database.modulestore.find({"_id.course":key})
        except:
            print ("Unable to query modulestore collection for course number ", key)
		    	
        # Initialize variable size
        size = 0
        
        # Calculate size of each course in "modulestore" collection
        for record in cursor:
            size = size + len(bson.BSON.encode(record))
            
        # Store in "modulestore_course_size" collection    
        modulestore_course_size[key] = size
    
    try:
        # Close server connection
        connection.close()
    except:
	    print ("Connection could not be closed with server at ", server_ip, ":", port)
	
    return 	modulestore_course_size

'''
   Following function gets size of course stored in "fs.files" collection
   of "edxapp" database
'''	
def get_fs_files_course_size():
	try:
	    # Establish connection with mongo database server
	    connection = MongoClient(server_ip, port)
	except:
	    print ("Connection could not be established with server at ", server_id, ":", port)
	
	try:
	    # Select database
	    database = connection.edxapp
	except:
	    print ("Unable to select database edxapp")
	# Stores size of course in "fs_files_course_size" with key as "course number" and value as "size"
	fs_files_course_size = dict()
	
	# Following loop calculates size of each course and stores in "fs_files_course_size" dictionary
	for key in course_info:
		
		try:
		    # Query "fs.files" collection of "edxapp" database
		    cursor = database.fs.files.find( { "_id.course" : key } )
		except:
		    print ("Unable to query fs.files collection for course number ", key)
		    
		# Initialize variable size
		size = 0
		
		# Calculate size of each course in "fs.files" collection
		for record in cursor:
			size = size + len(bson.BSON.encode(record))
		
		# Store in "fs_files_course_size" collection	
		fs_files_course_size[key] = size
	
	try:
	    # Close server connection
	    connection.close()
	except:
	    print ("Connection could not be closed with server at ", server_id, ":", port)		
	return fs_files_course_size

'''
   Following function gets size of course stored in "fs.chunks" collection
   of "edxapp" database
'''	
def get_fs_chunks_course_size():
	
	try:
	    # Establish connection with mongo database server
	    connection = MongoClient(server_ip, port)
	except:
	    print ("Connection could not be closed with server at ", server_id, ":", port)
	
	try:    	
	    # Select database
	    database = connection.edxapp
	except:
	    print ("Unable to select database edxapp")
	    	
	# Stores size of course in "fs_chunks_course_size" with key as "course number" and value as "size"
	fs_chunks_course_size = dict()
	
	# Following loop calculates size of each course and stores in "fs_chunks_course_size"
	for key in course_info:
		
		try:
		    # Query "fs.chunks" collection of "edxapp" database
		    cursor = database.fs.chunks.find( { "files_id.course" : key } )
		except:
		    print ("Unable to query fs.chunks collection for course number ", key)
		
		# Initialize variable size
		size = 0
		
		# Calculate size of each course in "fs.chunks" collection
		for record in cursor:
			size = size + len(bson.BSON.encode(record))
		
		# Store in "fs_chunks_course_size" collection	
		fs_chunks_course_size[key] = size
	
	try:
	    # Close server connection	
	    connection.close()
	except:
	    print ("Connection could not be closed with server at ", server_id, ":", port)	    
    	
	return fs_chunks_course_size

'''
   Following function gets size of course stored in "contents" collection
   of "cs_comments_service_development" database
'''	
def get_contents_course_size():
	
	try:
	    # Establish connection with mongo database server
	    connection = MongoClient(server_ip, port)
	except:
	    print ("Connection could not be established with server at ", server_id, ":", port)
	
	try:    	
	    # Select database
	    database = connection.cs_comments_service_development
	except:
	    print ("Unable to select database cs_comments_service_development")
	    	
	# Stores size of course in "contents_course_size" with key as "course number" and value as "size"
	contents_course_size = dict()
	
	# Following loop calculates size of each course and stores in "contents_course_size"
	for key in course_info:
		
		try:
		    # Query "contents" collection of "cs_comments_service_development" database
		    cursor = database.contents.find({ "course_id" : course_info[key] })
		except:
		    print ("Unable to query contents collection for course id", course_info[key])
		    	
		# Initialize variable size
		size = 0
		
		# Calculate size of each course in "contents" collection
		for record in cursor:
			size = size + len(bson.BSON.encode(record))
			
		# Store in "contents_course_size" collection	
		contents_course_size[key] = size
	
	try:
	    # Close server connection
	    connection.close()
	except:
	    print ("Connection could not be closed with server at ", server_ip, ":", port)	    
    	
	return contents_course_size

'''
   Following function get's course number of a course
'''
def get_course_num(request):
	
	# HTML element for form
    html = """
        <br /><br />
        <form action="/get_size_course" method="GET">   
            Course Number <br> <br>
            <input type="text" name="course_number"> <br> <br> <br>
            <input type="submit" value="Submit">
        </form>
	"""
    
    return HttpResponse(html)

'''
   Following function calculates's size of specific course
'''
def get_size_course(request):

	# Get course number 
	course_num = request.GET['course_number'].encode("ascii")

	try:
		# Establish connection with mongo database server
		connection = MongoClient(server_ip, port)
	except:
		print ("Connection could not be established with server at ", server_id, ":", port)
	
	try:    	
		# Select database "edxapp"
		database = connection.edxapp
	except:
		print ("Unable to select database edxapp")
	
	try:    	
		# Query on "modulestore" collection of database "edxapp"
		cursor = database.modulestore.find( { "_id.course": course_num , "_id.category" : "course" } )
	except:
		print ("Unable to query modulestore collection for course number", course_num)
	
	# Initialize course id
	course_id = ""

	# Get course id
	for data in cursor:
		course_id = data["definition"]["data"]["wiki_slug"].encode("ascii")

	# Format of "course id" is InstitutionName.CourseNumber.CourseRun which is changed to InstitutionName/CourseNumber/CourseRun using "split()" function
	lst_split = []
	lst_split = course_id.split(".")
	if course_id != "":
		course_id = lst_split[0]+"/"+lst_split[1]+"/"+lst_split[2]   

	# Initialize size
	size = 0

	try:
		# Query on "modulestore" collection of database "edxapp"
		cursor = database.modulestore.find( { "_id.course": course_num } ) 
	except:
		print ("Unable to query modulestore collection with course number ", course_num)

	# Add size of course in "modulestore" collection to size variable
	for record in cursor:
		size = size + len(bson.BSON.encode(record))

	try:
		# Query on "fs.files" collection of database "edxapp"
		cursor = database.fs.files.find( { "_id.course" : course_num } )
	except:
		print ("Unable to query fs.files collection for course number", course_num)

	# Add size of course in "fs.files" collection to size variable
	for record in cursor:
		size = size + len(bson.BSON.encode(record))            

	try:
		# Query on "fs.chunks" collection of database "edxapp"
		cursor = database.fs.chunks.find( { "files_id.course" : course_num } )    
	except:
		print ("Unable to query fs.chunks collection for course number", course_num)

	# Add size of course in "fs.chunks" collection to size variable
	for record in cursor:
		size = size + len(bson.BSON.encode(record))

	try:
		# Select database "cs_comments_service_development"    
		database = connection.cs_comments_service_development
	except:
		print ("Unable to select database cs_comments_service_development")

	try:    	
		# Query on "contents" collection of database "cs_comments_service_development"
		cursor = database.contents.find( { "course_id" : course_id } )
	except:
		print ("Unable to query contents collection for course id", course_id)

	# Add size of course in "contents" collection to size variable
	for record in cursor:
		size = size + len(bson.BSON.encode(record))

	try:
		# Close server connection
		connection.close()
	except:
		print ("Connection could not be closed with server at ", server_id, ":", port)

	# HTML element 
	html = "<html><body>Size of %s " % course_num
	html += " is %d bytes</body></html>" % size       

	return HttpResponse(html)
    
