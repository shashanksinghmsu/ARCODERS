from django.contrib import admin
from django.urls import path, include, re_path
from . import views
from django.conf.urls import url


urlpatterns = [
    path("", views.search, name="search"),
    path("search/program/<str:language>/<str:search>", views.search_program, name="search_program"),
    path("search/querybook/<str:language>/<str:search>", views.search_querybook, name="search_querybook"),
]
