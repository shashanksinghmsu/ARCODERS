from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate
from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers

from meta.views import Meta  # For Meta Data

# importing Model
from django.contrib.auth.models import User
from .models import *
from arcoder.models import Language
from program.models import program_title, Program
from querybook.models import Query

from arcoder.views import home
from arcoder.my_function import program_title_remove_quotations


#####################
# Required Functions#
#####################
# this function take the next url and replace the 'c  ' in c++
def cpp_checker(url):
    url = url.replace('C  ', 'C++')
    return url

def check_language(lang):
    try:
        if lang == 'C  ':
            lang = 'C++'

        language = Language.objects.get(name=lang)
    except:
        language = 'all'
    return language


def get_languages():
    languages = Language.objects.all()
    lang_list = []
    for lang in languages:
        lang_list.append(lang.name)
    return lang_list


#####################
# Required Variables#
#####################
# it store the number of blog will display on a particular page
no_of_blogs = 5
cat = 'Blog'
meta_data = ['ARCODERS', 'Blog', 'Programming']
all_languages = get_languages()


##########################
# Create your views here.#
##########################


def search(request):
    try:
        search_category = request.GET['category']
        temp_language = request.GET['language']
        search = request.GET['search']
        language = check_language(temp_language)

    except Exception as e:
        messages.error(
            request, "Something Gone Wrong! Search Your Query Again. ")
        return redirect('home')
        
    if search_category == 'Program':
        return redirect("search_program", search=search, language=language)

    elif search_category == 'Querybook':
        return redirect("search_querybook", search=search, language=language)
        



# Handle search program request
def search_program(request, search, language=None):
    if language == 'all' or language == 'All':
        programs = program_title.objects.filter(Q(title__icontains = search))
    else:
        programs = program_title.objects.filter(Q(title__icontains = search), language=language)
    
    paginator = Paginator(programs, no_of_blogs)
    page_number = request.GET.get('page')
    try:
        program_data = paginator.page(page_number)
    except PageNotAnInteger:
        program_data = paginator.page(1)
    except EmptyPage:
        program_data = paginator.page(paginator.num_pages)

    program_data = program_title_remove_quotations(program_data);
    program_data_json = serializers.serialize('json', program_data)
    meta = Meta(
        title="ARCODERS PROGRAMS",
        description='ARCODERS PROGRAMS:- Here you get the stuff related to programming and the latest technology',
        keywords=meta_data + all_languages,
        extra_props={
            'viewport': 'width=device-width, initial-scale=1.0, minimum-scale=1.0'},
        extra_custom_props=[('http-equiv', 'Content-Type', 'text/html; charset=UTF-8'),
                            ]
    )

    params = {'cat': cat, 'data':program_data, 'json_data': program_data_json, 'meta': meta}
    return render(request, 'search/program/program.html', params)


# Handle search Querybook request
def search_querybook(request, search, language=None):
    if language == 'all' or language == 'All':
        queries = Query.objects.filter(Q(query__icontains=search) | Q(
            description__icontains=search))
    else:
        queries = Query.objects.filter(Q(query__icontains=search) | Q(
            description__icontains=search))

    paginator = Paginator(queries, no_of_blogs)
    page_number = request.GET.get('page')
    try:
        datas = paginator.page(page_number)
    except PageNotAnInteger:
        datas = paginator.page(1)
    except EmptyPage:
        datas = paginator.page(paginator.num_pages)

    meta = Meta(
        title="ARCODERS QUERYBOOK",
        description='ARCODERS QUERYBOOK:- Here you get the stuff related to programming and the latest technology',
        keywords=meta_data + all_languages,
        extra_props={
            'viewport': 'width=device-width, initial-scale=1.0, minimum-scale=1.0'},
        extra_custom_props=[('http-equiv', 'Content-Type', 'text/html; charset=UTF-8'),
                            ]
    )

    params = {'cat': cat, 'data': datas, 'meta': meta}
    return render(request, 'search/querybook/querybook.html', params)
