from django.contrib import admin
from django.urls import path, include, re_path
from . import views
from django.conf.urls import url

urlpatterns = [
    path('', views.home, name='home'),
    path('ads.txt/', views.ads, name='ads'),
    
    # For Avaibality of usernames
    path('username/', views.username, name='username'),
    # handle the nav bar according to user authentication
    path('navbar/', views.navbar, name='navbar'),


    # For Ck-Editor
    path('ckeditor', include('ckeditor_uploader.urls')),

    path('contact/', views.contact, name='contact'),
    path('signup/', views.sign_up, name='sign_up'),
    path('login/', views.log_in, name='log_in'),
    path('logout/', views.log_out, name='log_out'),

    # User  Profile
    path('user/', views.user, name='user'),
    # privacy
    path('privacy/', views.user_privacy, name='user_privacy'),
    # change user image
    path('upload_image/', views.upload_image, name='upload_image'),
    # remove profile picture
    path('remove_image/', views.remove_image, name='remove_image'),

    # For Particular Language category
    path('<str:lang>/', views.language, name='language'),
     # for all language program
    path('user/program/', views.user_program, name='user_program'),
    path('user/query/', views.user_query, name='user_query'),
    path('user/solution/', views.user_solution, name='user_solution'),

    # Other user profile
    path('user/<str:username>/', views.other_profile, name='other_profile'),


    # For OTP Verification
    path('otp_verification/<str:url_otp>/',
         views.otp_verification, name='otp_verification'),

     # for user program of particular language
    path('user/program/<str:lang>/', views.user_program, name='user_program'),

    # remove User Data
    path('user/remove_program/<int:program_id>',
         views.remove_program, name='remove_program'),
    path('user/remove_query/<int:query_id>',
         views.remove_query, name='remove_query'),
    path('user/remove_solution/<int:solution_id>',
         views.remove_solution, name='remove_solution'),


    # Other User Profile Data
    path('user/<str:username>/program/',
         views.other_program, name='other_program'),
    path('user/<str:username>/query/', views.other_query, name='other_query'),
    path('user/<str:username>/solution/',
         views.other_solution, name='other_solution'),



    # Edit User Data
    # here language has no use
    path('user/edit_program/<str:language>/<int:program_id>',
         views.edit_program, name='edit_program'),
    path('user/edit_query/<str:language>/<int:query_id>',
         views.edit_query, name='edit_query'),
    path('user/edit_solution/<str:language>/<int:solution_id>',
         views.edit_solution, name='edit_solution'),

     # for other user program of particular language 
    path('user/<str:username>/program/<str:lang>/',
         views.other_program, name='other_program'),


]
