from django.conf.urls import url
from django.shortcuts import render_to_response
from . import views

urlpatterns = [

	#url(r'^$',views.get_attendance,name='go'),
	url(r'^student_home/', views.student_home, name="student_home"),
	#url(r'^$', views.get_student_all_courses_attendance, name="course"),
	url(r'^course_structure/$', views.get_bootstrap,name="bootstrap"),
	#url(r'^course_skeleton/$', views.get_course_skeleton,name="course_skeleton"),
	#url(r'^test$',views.driver_program,name='test'),
	url(r'^quizes$',views.get_avg_max_marks_list,name='quizes'),
	url(r'^course_structure1', views.get_course_structure, name= "course_data"),
	url(r'^course_structure1', views.get_course_structure, name= "course_data"),
	url(r'^student_unanswered_questions/$',views.course_unanswered_questions,name='student_unanswered_questions'),
        url(r'^student_answered_questions/$',views.course_answered_questions,name='student_answered_questions'),
        url(r'^student_discussions/$',views.course_discussions,name='student_discussions'),


] 
