from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template.loader import render_to_string
from collections import OrderedDict
from operator import itemgetter 
from .custom_api.diskapi import get_all_courses_size
from .custom_api.student_reg_datewise import  get_all_stu_registrations
from .custom_api.emails_count_by_course_id import get_emails_count_by_course_id
from .custom_api.coursewise_students_strength import get_student_count_coursewise
from .custom_api.course_enrollment_details import get_course_enrollment_body
from .custom_api.registrations_between_dates import details_of_registration_between_dates
from .custom_api.course_enrollment_detail_on_a_date import get_course_enrollment_detail_on_a_date
from .custom_api.course_enrollment_detail_on_a_date import get_course_enrollment_detail_coursewise_on_a_date
from .custom_api.email_details import emais_count_coursewise
from .custom_api.mysql_info import   MYSQL_SERVER_IP
from .custom_api.mysql_info import   USER
from .custom_api.mysql_info import   PASSWORD
from .custom_api.mysql_info import   DATABASE
from .custom_api.mongo_info import   MONGO_SERVER_IP
from .custom_api.mongo_info import   MONGO_PORT
import json
import collections
import os
from django.contrib.auth.decorators import login_required
#-------------------------------------------------------------------------------VIEWS FOR THIRD THEME------------------------
''' 
        

Author : Anjay Abhishek(anjayabhishek@gmail.com),Aditya Kalkonde(adityakalkonde007@gmail.com)
Last Modified : 30-June-2015


        
'''
def admin_login_required(f):
        def wrap(request, *args, **kwargs):
                #this check the session if userid key exist, if not it will redirect to login page
                if 'user_id' not in request.session.keys():
                        return HttpResponseRedirect(request.build_absolute_uri('/'))
                elif request.session["usertype"]!="admin":
                	return HttpResponse(request.build_absolute_uri('/'))
                return f(request, *args, **kwargs)
        wrap.__doc__=f.__doc__
        wrap.__name__=f.__name__
        return wrap
@admin_login_required
def index3theme3(request):	
    if request.method=='GET' and 'type' in request.GET:
         request_code = int(request.GET.get('type')) #request code identifies what data has to be returned
    else:
        request_code = 0 # if request code not provided , assume 0
    sd = request.GET.get('sd') # receive start date if provided (optional , needed when api needs them)
    ed = request.GET.get('ed') # receive end date if provided (optional , needed when api needs them)
    #following are some dictionaries that store the result to be sent
    total_course_size={}
    total_stu_reg_datewise0={}
    mail_btwn_dates={}
    coursewise_strength={}
    email_coursewise={}
	#call code specific api and store result
    if request_code == 100 :
        coursewise_strength=get_student_count_coursewise(ip=MYSQL_SERVER_IP,user=USER,pwd=PASSWORD,db=DATABASE)
    elif request_code == 101 :
        total_stu_reg_datewise0=get_all_stu_registrations(ip=MYSQL_SERVER_IP,user=USER,pwd=PASSWORD,db=DATABASE)
    elif request_code == 102 :
        total_course_size=get_all_courses_size(host=MONGO_SERVER_IP, port=MONGO_PORT, user="", password="")
    elif request_code == 103 :
        email_coursewise=get_emails_count_by_course_id(ip=MYSQL_SERVER_IP,user=USER,pwd=PASSWORD,db=DATABASE)
    else :
        print("invalid type")
    #using ordered dictionary to preserve the order of data , suffix number indicates which request code it is serving
    od100 = collections.OrderedDict(sorted(coursewise_strength.items()))
    od101 = collections.OrderedDict(sorted(total_stu_reg_datewise0.items()))
    od102 = collections.OrderedDict(sorted(total_course_size.items()))
    od103 = collections.OrderedDict(sorted(email_coursewise.items()))
	# return data to front end now based on request code request_code
    if request_code == 0:
        return render(request,"adminpanel/index.html")
    elif request_code == 100: 
        return HttpResponse(json.dumps(od100), content_type="application/json") 
    elif request_code == 101:
        return HttpResponse(json.dumps(od101), content_type="application/json") 
    elif request_code == 102 :
        return HttpResponse(json.dumps(od102), content_type="application/json")
    elif request_code >= 103:
        return HttpResponse(json.dumps(od103), content_type="application/json")   
    else :
        return HttpResponse("REQUEST TYPE ERROR")
#following views render various html contents as required by ajax calls 

@admin_login_required
def registration_details(request):
    page_no=int(request.GET.get("page_no"))
    records_per_page=int(request.GET.get("records_per_page"))
    sd=request.GET.get("sd")
    ed=request.GET.get("ed")
    datalist=[]
    datalist=details_of_registration_between_dates(ip=MYSQL_SERVER_IP,user=USER,pwd=PASSWORD,db=DATABASE,page_no=page_no,records_per_page=records_per_page,date1=sd,date2=ed)
    return render(request,"adminpanel/registration_details.html",{'data':datalist[0],'page_no':datalist[2],'records_per_page':datalist[3],'max_page':datalist[1],'total_rows':datalist[4],'startdate':sd,'enddate':ed})

@admin_login_required
def dashboardcharts(request):
    return render(request,"adminpanel/dashboardcharts.html")

@admin_login_required
def course_enrollment_student_detail_on_a_date(request):
    print "Views Course Body"
    page_no=int(request.GET.get("page_no"))
    records_per_page=int(request.GET.get("records_per_page"))
    date1=request.GET.get("fromdate")
    print("in views -> ",date1)
    datalist=[]
    datalist=get_course_enrollment_detail_on_a_date(ip=MYSQL_SERVER_IP,user=USER,paswd=PASSWORD,db=DATABASE,page_no=page_no,records_per_page=records_per_page,date=date1)
    print datalist[0]
    return render(request,"adminpanel/course_enrollment_student_detail_on_a_date.html",{'data':datalist[0],'page_no':datalist[2],'records_per_page':datalist[3],'max_page':datalist[1],'date':date1})

@admin_login_required
def course_enrollment_coursewise_detail_on_a_date(request):
    print "Views Course Body"
    page_no=int(request.GET.get("page_no"))
    records_per_page=int(request.GET.get("records_per_page"))
    date1=request.GET.get("fromdate")
    print("in views -> ",date1)
    datalist=[]
    datalist=get_course_enrollment_detail_coursewise_on_a_date(ip=MYSQL_SERVER_IP,user=USER,paswd=PASSWORD,db=DATABASE,page_no=page_no,records_per_page=records_per_page,date=date1)
    print datalist[0]
    return render(request,"adminpanel/course_enrollment_coursewise_detail_on_a_date.html",{'data':datalist[0],'page_no':datalist[2],'records_per_page':datalist[3],'max_page':datalist[1],'date':date1})

@admin_login_required
def course_enrollment_detail_on_a_date(request):
    return render(request,"adminpanel/course_enrollment_detail_on_a_date.html")

@admin_login_required
def course_enrollment_body(request):
    page_no=int(request.GET.get("page_no"))
    records_per_page=int(request.GET.get("records_per_page"))
    sd=request.GET.get("sd")
    ed=request.GET.get("ed")
    datalist=[]
    datalist=get_course_enrollment_body(ip=MYSQL_SERVER_IP,user=USER,pwd=PASSWORD,db=DATABASE,page_no=page_no,records_per_page=records_per_page,startdate=sd,enddate=ed)
    return render(request,"adminpanel/course_enrollment_body.html",{'data':datalist[0],'page_no':datalist[3],'records_per_page':datalist[2],'max_page':datalist[1],'startdate':sd,'enddate':ed})

@admin_login_required
def email_details(request):
    pageno=int(request.GET.get("page_no"))
    records_per_page=int(request.GET.get("records_per_page"))
    sd=request.GET.get("sd")
    ed=request.GET.get("ed")
    datalist=emais_count_coursewise(ip=MYSQL_SERVER_IP,user=USER,pwd=PASSWORD,db=DATABASE,page_no=pageno,no_of_entries=records_per_page,date1=sd,date2=ed)
    return render_to_response('adminpanel/email_details.html',{'data':datalist[0],'page_no':datalist[1],'records_per_page':datalist[2],'max_page':datalist[3],'total_email':datalist[4],'startdate':sd,'enddate':ed})
