from django.conf.urls import url

from . import views
urlpatterns = [
url(r'^fac/$',views.fac_first,name='fac_first'),
url(r'^fac1/$',views.fac_second,name='fac_second'),
url(r'^index/$',views.index,name='index'),
url(r'^crsofinsti/(?P<orgid>(.+))$',views.organizationwise_courses_enrollment,name='crsofinsti'),

#url(r'^instwise/$',views.institute_wise,name='instwise'),
url(r'^$',views.course_wise,name='coursewise'),
] 
