from django.contrib import admin
from django.urls import path, include, re_path
from . import views
from django.conf.urls import url


urlpatterns = [
    path('', views.querybook, name = 'querybook'),
    path('query_form/', views.query_form, name = 'query_form'),
    path('like/', views.like, name = 'querybook_like'),
    path('rating/', views.rating, name='solution_rating'),
    # for particular language
    path('<str:lang>/', views.querybook, name = 'querybook'),
    path('<str:lang>/add/', views.add, name = 'querybook_add'),
    # path('<str:language>/start/', views.start, name = 'start'),
    path('query_data/<str:slug>/', views.get_query_data, name='query_data'),

    path('<str:language>/<str:query_slug>/', views.final_query, name = 'final_query'),
	path('<str:language>/<str:query_slug>/add_solution/', views.solution_form, name = 'solution_form'),
]    
