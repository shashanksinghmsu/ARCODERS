from django.contrib import admin
from django.urls import path, include, re_path
from . import views
from django.conf.urls import url


urlpatterns = [
	path('update_username/', views.update_username, name='username_update'),
	path('username_check/', views.username_check, name='username_check'),
	path('update_email/', views.email, name='email_update'),
	path('update_name/', views.name, name='name_update'),
	path('update_dob/', views.dob, name='dob_update'),
	path('update_gender/', views.gender, name='gender_update'),
	path('update_phone/', views.phone, name='phone_update'),
	path('update_about/', views.about, name='about_update')
]
