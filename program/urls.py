from django.contrib import admin
from django.urls import path, include,re_path
from . import views
from django.conf.urls import url




urlpatterns = [
    # for all language
    path('', views.program, name = 'program'),
    path('form/', views.form, name = 'program_form'),
    path('like/', views.like, name = 'program_like'),
    path('rating/', views.rating, name = 'program_rating'),
    # for particular language program
    path('<str:lang>/', views.program, name = 'program'),
    
    path('program_data/<str:slug>/', views.get_program_data, name='program_data'),
    
    path('<str:lang>/add/', views.add, name = 'program_add'),
    # path('<str:language>/start/', views.start, name = 'start'),
    path('<str:lang>/<str:slug>/', views.final_program, name = 'final_program')
    ]
