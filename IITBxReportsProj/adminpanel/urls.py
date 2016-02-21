from django.conf.urls import patterns, url
from adminpanel import views
from django.views.generic import TemplateView

urlpatterns = patterns('',

		url(r'^$', views.index3theme3, name='index3atheme3'),
		url(r'^index', views.index3theme3, name='index3btheme3'),
		url(r'^registration_details', views.registration_details, name='registration_details'),
		url(r'^dashboardcharts', views.dashboardcharts, name='dashboardcharts'),
		url(r'^email_details', views.email_details, name='email_details'),
		url(r'^course_enrollment_body', views.course_enrollment_body, name='course_enrollment_body'),
		url(r'^course_enrollment_detail_on_a_date', views.course_enrollment_detail_on_a_date, name='course_enrollment_detail_on_a_date'),
                url(r'^course_enrollment_coursewise_detail_on_a_date', views.course_enrollment_coursewise_detail_on_a_date, name='course_enrollment_coursewise_detail_on_a_date'),
		url(r'^course_enrollment_student_detail_on_a_date', views.course_enrollment_student_detail_on_a_date, name='course_enrollment_student_detail_on_a_date'),
		)
