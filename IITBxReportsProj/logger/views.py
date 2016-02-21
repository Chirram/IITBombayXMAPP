#importing libraries and dependencies
from django.shortcuts import render_to_response,redirect
from django.contrib.auth import authenticate,login,logout
from django.core.context_processors import csrf
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User
import MySQLdb
from django.contrib.auth.decorators import login_required
from faculty import views as facultyviews
from faculty.apis.inputs import DatabaseConfig
from adminpanel import views as adminpanelviews
from student import views as studentviews

#NOTE 
"""
	Problems with this login_user and logout_user
	even though the user logged out the web pages stored in history can be seen. If anybody further developes please take care of this.
	currently the login and user identification is done using IITBombayX tables(edxapp-mysql) tables only.
	So At any particular time user is able to login into either ITTBombaX or IITBombayXMAPP . try to take care of this.
	As per our knowledge it is due to session conflicts. If single sign-on implemented then it will become more easier.	
"""

"""
The following is a user defined decorator. checks if any user is logged in or not.can be called before a fuction
which user request as argument to check wether any user is logged in or not.
"""
def user_login_required(f):
        def wrap(request, *args, **kwargs):
                if 'user_id' not in request.session.keys():
                        return HttpResponseRedirect(request.build_absolute_uri('/'))
                return f(request, *args, **kwargs)
        wrap.__doc__=f.__doc__
        wrap.__name__=f.__name__
        return wrap
        
#function : login_user(request)
"""
Description : This is the first fuction called. i.e. start point of the application which
		checks the user credentials and redirects them to their dashboards accordingly
		to thier user role. Don't confuse with state it returns the account status
		that can be used in giving alerts, currently not using anywhere.
input : request - Http Request from client i.e. webbrowser

output: If the session is already existed based on user type it will redirects to the respective panel
	else it will check for the credentials and redirects to the respective panel
Author : 
	  Dileep Kumar Dora
	  email: dileepdora.iiit@gmail.com 
Date of Creation : 17/06/2015
"""


def login_user(request):
	if "usertype" in request.session:
		s1=request.session["usertype"]
		if (s1 == "instructor"):
			response=facultyviews.index(request)
		elif (s1=="student"):
			response=studentviews.student_home(request)
		elif (s1=="admin"):
			response=redirect('adminpanel/')
		return response
	else:
		c={}
		c.update(csrf(request))
		state = "Please log in below..."
		username =''
		password = ''
		if request.POST:
			username = request.POST.get('username')
			password = request.POST.get('password')
			request_user = authenticate(username=username, password=password)
			if request_user is not None:
				if request_user.is_active:
					login(request, request_user)
					state = "You're successfully logged in!"
					db = MySQLdb.connect(DatabaseConfig.MYSQL_HOST,DatabaseConfig.MYSQL_USER,DatabaseConfig.MYSQL_PWD,DatabaseConfig.MYSQL_DB )
					cursor = db.cursor()
					query="select is_superuser,id from auth_user where username='"+username+"';"
					cursor.execute(query)
					data=cursor.fetchall()
					db.close()
					usertype={}
					if(int(data[0][0])==1):
						usertype={"user_type":"admin","user_id":data[0][1]}
						request.session["user_id"]=usertype["user_id"]
						request.session["username"]=username
						request.session["usertype"]=usertype["user_type"]
						print "admin id:",request.session["user_id"]
						response=redirect('adminpanel/')
						return response
					else:
						db = MySQLdb.connect(DatabaseConfig.MYSQL_HOST,DatabaseConfig.MYSQL_USER,DatabaseConfig.MYSQL_PWD,DatabaseConfig.MYSQL_DB )
						cursor = db.cursor()
						query="select count(*),a.id from auth_user a inner join student_courseaccessrole b on a.id=b.user_id where a.username='"+username+"';"
						cursor.execute(query)
						datas=cursor.fetchall()
						db.close()
						print datas
						if (int(datas[0][0])>0):
							usertype={"user_type":"instructor","user_id":datas[0][1]}
							request.session["user_id"]=usertype["user_id"]
							request.session["username"]=username
							request.session["usertype"]=usertype["user_type"]
							response=facultyviews.index(request)
							return response
						else:
							usertype={"user_type":"student","user_id":datas[0][1]}
							request.session["user_id"]=usertype["user_id"]
							request.session["username"]=username
							request.session["usertype"]=usertype["user_type"]
							response=studentviews.student_home(request)
							return response
				else:
					state = "Your account is not active, please contact the site admin."
			else:
				state = "Your username and/or password were incorrect."
	
		return render_to_response('auth.html',{'state':state, 'username': username})

"""
Description : This fuction is to clear the session variables and expiry the session and logging out the user
input : request - Http Request from client i.e. webbrowser
	

output: Clears session and deletes session variables and redirects to home page.
Author : 
	  Dileep Kumar Dora
	  email: dileepdora.iiit@gmail.com 
Date of Creation : 17/06/2015
"""


@user_login_required #It indicates user should be logged in before logout
def logout_user(request):
	del request.session["user_id"]
	del request.session["usertype"]
	del request.session["username"]
	request.session.set_expiry(0)	
	request.session.modified=True
	return HttpResponseRedirect(request.build_absolute_uri('/'))
