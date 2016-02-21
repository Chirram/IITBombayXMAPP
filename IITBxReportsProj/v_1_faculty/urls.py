from django.conf.urls import url

from . import views
urlpatterns = [
	url(r'^index/(?P<facultyid>(.+))$',views.index,name='index'),
        url(r'^course_unanswered_questions/(?P<facultyid>(.+))$',views.course_unanswered_questions,name='course_unanswered_questions'),
        url(r'^course_answered_questions/(?P<facultyid>(.+))$',views.course_answered_questions,name='course_answered_questions'),
        url(r'^course_discussions/(?P<facultyid>(.+))$',views.course_discussions,name='course_discussions'),
	url(r'^stuofcrs/(.+)/(.+)/(.+)/(.+)/(.+)/(.+)/(.+)$',views.students_of_course_result_display,name='students_of_course_result_display'),
	url(r'^stuofcrs/(?P<facultyid>(.+))$',views.students_of_course,name='stuofcrs'),
     #  url(r'^course_enrollment_details/(?P<facultyid>(.+))$',views.course_enrollment_details,name='course_enrollment_details'),
        url(r'^stugrades/(?P<courseid>(.+))/(?P<facultyid>(.+))$',views.students_grade_courselevel,name='stugrades'),
        url(r'^quizlevelgrades/(?P<student_id>(.+))/(?P<courseid>(.+))/(?P<facultyid>(.+))$',views.students_grade_quizlevel,name='quizlevelgrades'),
	url(r'^cohort_details$',views.cohort_details,name='cohort_details'),
	url(r'^cohort_detailed_discussions$',views.cohort_detailed_discussions,name='cohort_detailed_discussions'),
        url(r'^cohort_detailed_answered$',views.cohort_detailed_answered,name='cohort_detailed_answered'),
        url(r'^cohort_detailed_unanswered$',views.cohort_detailed_unanswered,name='cohort_detailed_unanswered'),
        url(r'^cohort_students_list$',views.cohort_students_list,name='cohort_students_list'),


] 
