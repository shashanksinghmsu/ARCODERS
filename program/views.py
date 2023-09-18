from django.db.models.aggregates import Count
from .models import *
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate
from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from arcoder.language_name import prism_name
from arcoder.models import Language
from .forms import add_program_code
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from meta.views import Meta  # For Meta Data

from django.core.cache import cache, caches
from custom_cache_page.cache import cache_page
from custom_cache_page.utils import generate_query_params_cache_key
from cache_key_generator import get_cache_key
import json
from django.core import serializers
from arcoder.my_function import program_title_remove_quotations, check_language

#####################
# Required Functions#
#####################
# this function take the next url and replace the 'c  ' in c++
def cpp_checker(url):
    try:
        url = url.replace('C  ', 'C++')
        return url
    except:
        pass



def get_languages():
    languages = Language.objects.all()
    lang_list = []
    for lang in languages:
        lang_list.append(lang.name)
    return lang_list


# creating the program title if not exists
def create_title(title, language, prism):
    obj = program_title(title=title, language=language, answers=1, prism_name=prism)
    obj.save()
    return obj


# saving a code to the database
def add_program(title, code, author, language, prism, url=None):
    if program_title.objects.filter(title=title, language=language).exists():
        title_obj = program_title.objects.get(title=title, language=language)
        ans = title_obj.answers
        title_obj.answers = ans+1
        title_obj.save()
        obj = Program(title=title_obj, code=code, author=author, url=url)
        obj.save()
        return obj
    else:
        title_obj = create_title(title, language, prism)
        title_obj.answers = 1
        title_obj.save()
        obj = Program(title=title_obj, code=code, author=author, url=url)
        obj.save()
        return obj




# updating the (user and program) cache while liking the program
def update_like_cache(slug, username, id):   
    id = int(id)
    # for caching data
    user_key = 'user/' + str(username) + '/'
    user_cache_value = caches['user'].get(user_key)

    program_key = 'program/' + str(slug) + '/'
    program_cache_value = caches['program'].get(program_key)



    if user_cache_value is not None:
        if int(id) in user_cache_value['program']['like']:
            # updating user cache value
            cache_value = user_cache_value
            caches['user'].delete(user_key)
            cache_value['program']['like'].remove(id)
            caches['user'].set(user_key, cache_value, 10*60)

            if program_cache_value is not None:
                index = program_cache_value['programs']['id'].index(int(id))
                # updating program cache value
                temp_cache_value = program_cache_value
                caches['program'].delete(program_key)
                temp_cache_value['programs']['like_count'][index] -= 1
                caches['program'].set(program_key, temp_cache_value, 10*60)

            return False

        else:
            # updating user cache value
            cache_value = user_cache_value
            caches['user'].delete(user_key)
            cache_value['program']['like'].append(id)
            caches['user'].set(user_key, cache_value, 10*60)
            
            if program_cache_value is not None:
                index = program_cache_value['programs']['id'].index(int(id))
                # updating program cache value
                temp_cache_value = program_cache_value
                caches['program'].delete(program_key)
                temp_cache_value['programs']['like_count'][index] += 1
                caches['program'].set(program_key, temp_cache_value, 10*60)


            return True
    else:
        return None



# updating the (user and program) cache while rating the program
def upade_rating_cache(id, slug, username, rate):
    id = int(id)
    # for caching data
    user_key = 'user/' + str(username) + '/'
    user_cache_value = caches['user'].get(user_key)

    program_key = 'program/' + str(slug) + '/'
    program_cache_value = caches['program'].get(program_key)

    if int(id) in user_cache_value['program']['rating']:
        previous_rate = user_cache_value['program']['rating'][id]
    else:
        previous_rate = 0

    if program_cache_value is not None:
        index = program_cache_value['programs']['id'].index(int(id))
        # updating program cache value
        temp_cache_value = program_cache_value
        caches['program'].delete(program_key)
        if previous_rate == 0:
            temp_cache_value['programs']['total_rating'][index][1] += 1

        count = temp_cache_value['programs']['total_rating'][index][1]

        temp_cache_value['programs']['total_rating'][index][2] = temp_cache_value[
            'programs']['total_rating'][index][2] - previous_rate + rate

        total = temp_cache_value['programs']['total_rating'][index][2]
        total_rating = int(total*20/count)
        temp_cache_value['programs']['total_rating'][index][0] = total_rating
        caches['program'].set(program_key, temp_cache_value, 10*60)


    # handling the user cache
    if user_cache_value is not None:
        if int(id) in user_cache_value['program']['rating']:
            # updating user cache value
            cache_value = user_cache_value
            caches['user'].delete(user_key)
            cache_value['program']['rating'][id] = rate
            count = len(cache_value['program']['rating'])
            sum = (cache_value['user_data']['program_rating'] * (count-1)) + (rate *20)
            cache_value['user_data']['program_rating'] = sum/count 
            caches['user'].set(user_key, cache_value, 10*60)

        else:
            # updating user cache value
            cache_value = user_cache_value
            caches['user'].delete(user_key)
            cache_value['program']['rating'][id] = rate
            count = len(cache_value['program']['rating'])
            sum = (cache_value['user_data']['program_rating']
                   * (count-1)) + (rate * 20)
            cache_value['user_data']['program_rating'] = sum/count
            caches['user'].set(user_key, cache_value, 10*60)

        if previous_rate != 0:
            return True
        else:
            return False
    else:
        return False



#####################
# Required Variables#
#####################
# it store the number of programs will display on a particular page
meta = None
no_of_programs = 5
cat = 'Program'
meta_data = ['ARCODERS', 'Program', 'Programming']
all_languages = get_languages()


##########################
# Create your views here.#
##########################

# handle the program page specially for all language

def program(request, lang = None):
    temp_language = lang
    language = check_language(temp_language)

    if language != None:
        category = language.category.split(',')
        if 'Program' in category or 'program' in category:
            program_key = language.name +'/'
            program_cache_value = caches['program'].get(program_key)

            if program_cache_value is not None:
                programs = program_cache_value['programs']
            else:
                programs = program_title.objects.filter(language=language)
                params = {'programs': programs}
                caches['program'].set(program_key, params, 1*60)
        else:
            return redirect('program')

    else:
        # Handeling for all languages    
        program_key = 'program/'
        program_cache_value = caches['program'].get(program_key)

        if program_cache_value is not None:
            programs = program_cache_value['programs']

        else:
            programs = program_title.objects.all()
            params = {'programs' : programs,}
            caches['program'].set(program_key, params, 1*60)


    paginator = Paginator(programs, no_of_programs)
    page_number = request.GET.get('page')
    try:
        program_data = paginator.page(page_number)
    except PageNotAnInteger:
        program_data = paginator.page(1)
    except EmptyPage:
        program_data = paginator.page(paginator.num_pages)

    program_data = program_title_remove_quotations(program_data)
    program_data_json = serializers.serialize('json', program_data)
    
    # for meta data and params
    if language == None:
        meta_language = all_languages
        language_name = ''
    else:
        meta_language = [language.name]
        language_name = language.name
    meta = Meta(
        title="ARCODERS PROGRAMS",
        description='ARCODERS PROGRAMS:- Here you get the stuff related to programming.',
        keywords=meta_data + meta_language,
        extra_props={
            'viewport': 'width=device-width, initial-scale=1.0, minimum-scale=1.0'},
        extra_custom_props=[('http-equiv', 'Content-Type', 'text/html; charset=UTF-8'),
                            ]
    )
    
    params = {'cat': cat, 'data': program_data, 'json_data': program_data_json, 'meta': meta, 'paginator_data':program_data, 'language':language_name, 'title_prefix':''}
    return render(request, 'program/program.html', params)


# form will add the user program data
# handle post request and save it into the database
def form(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form_data = add_program_code(request.POST)
            if form_data.is_valid():
                title = form_data.cleaned_data['title']
                code = form_data.cleaned_data['code']
                code = code.replace('<', '&lt;')
                code = code.replace('>', '&gt;')
                code = '<code>' + code + '</code>'
                language = request.POST['language']
                prism = prism_name[language]
                username = request.user.username
                
                # handeling the new title if exists
                obj = add_program(title, code, request.user, language, prism)

                program_key = 'program/' + str(obj.title.slug) + '/'
                program_cache_value = caches['program'].get(program_key)

                if program_cache_value is not None:
                    # updating program cache value
                    temp_cache_value = program_cache_value
                    caches['program'].delete(program_key)
                    temp_cache_value['answer_count'] += 1
                    temp_cache_value['programs']['id'].append(obj.id)
                    temp_cache_value['programs']['code'].append(obj.code)
                    temp_cache_value['programs']['author'].append(request.user.username)
                    temp_cache_value['programs']['time_stamp'].append(obj.timeStamp)
                    temp_cache_value['programs']['total_rating'].append([0,0,0])
                    temp_cache_value['programs']['like_count'].append(0)
                    caches['program'].set(program_key, temp_cache_value, 10*60)





                messages.error(request, "Program SucessFully Added")
                try:
                    url = cpp_checker(request.GET.get('next'))
                    return redirect(url)
                except:
                    return redirect('program_add', lang='Python')
        messages.error(request, "Invalid Credential")
        try:
            url = cpp_checker(request.GET.get('next'))
            return redirect(url)
        except:
            return redirect('program_add', lang='Python')

    messages.error(request, "Login to Add Program !!!")
    # try:
    #     url = cpp_checker(request.GET.get('next'))
    #     return redirect(url)
    # except:
    #     return redirect('program_add', lang='Python')



# Handle final program
# @cache_page(
#     timeout=60 * 10,
#     key_func=lambda r: r.path,
#     versioned=0,
#     group_func=lambda r: 'cached_views',
#     prefix='program_final'
# )
# dont cache page due to csrf token
def final_program(request, lang, slug):
    language = check_language(lang)
    if language != None:
        category = language.category.split(',')
        if 'Program' in category or 'program' in category:

            title_obj = program_title.objects.get(language=lang, slug=slug)


            form = add_program_code(
                request.POST or None, request.FILES or None, initial={
                    'title': title_obj.title})

            meta = Meta(
                title="ARCODERS PROGRAMS:- " + title_obj.title,
                description=title_obj.title,
                keywords=meta_data + [title_obj.title, title_obj.language],
                extra_props={
                    'viewport': 'width=device-width, initial-scale=1.0, minimum-scale=1.0'},
                extra_custom_props=[('http-equiv', 'Content-Type', 'text/html; charset=UTF-8'),
                                    ]
            )

            params = { 'slug': slug, 'language': language.name, 'meta': meta, 'form': form, 'rating': True}

            return render(request, 'program/final.html', params)




# Handeling the like
@csrf_exempt
def like(request):
    if request.method == 'POST':
        id = request.POST['id']

        program_obj = Program.objects.get(id=id)
        return_value = update_like_cache(program_obj.title.slug, request.user.username, id)

        # handling program cache
        program_key = 'program/' + str(program_obj.title.slug) + '/'
        program_cache_value = caches['program'].get(program_key)



        if return_value is None:
            if program_obj.like.filter(id=request.user.id).exists():
                program_obj.like.remove(request.user)

               
                if program_cache_value is not None:
                    index = program_cache_value['programs']['id'].index(int(id))
                    # updating program cache value
                    temp_cache_value = program_cache_value
                    caches['program'].delete(program_key)
                    temp_cache_value['programs']['like_count'][index] -= 1
                    caches['program'].set(program_key, temp_cache_value, 10*60)


                return HttpResponse(False)

            else:
                program_obj.like.add(request.user)

                if program_cache_value is not None:
                    index = program_cache_value['programs']['id'].index(int(id))
                    # updating program cache value
                    temp_cache_value = program_cache_value
                    caches['program'].delete(program_key)
                    temp_cache_value['programs']['like_count'][index] += 1
                    caches['program'].set(program_key, temp_cache_value, 10*60)


                return HttpResponse(True)


        else:
            if return_value:
                program_obj.like.add(request.user)
                return HttpResponse(True)

            else:
                program_obj.like.remove(request.user)
                return HttpResponse(False)



        

# getting the program data
def get_program_data(request, slug):
    program = None
    program_key = 'program/' + str(slug) + '/'
    program_cache_value = caches['program'].get(program_key)



    if program_cache_value is not None:
        params = program_cache_value

    else:
        exists = False
        title = program_title.objects.get(slug=slug)
        if title is not None:
            exists = True

        programs = Program.objects.filter(title__id = title.id)
        program_id = list()
        total_ratings = list()
        code = list()
        author = list() 
        time_stamp = list()
        like_count = list()

        for program in programs:
            total_ratings.append(program.total_rating())
            code.append(program.code)
            program_id.append(program.id)
            author.append(program.author.username)
            time_stamp.append(program.timeStamp)
            like_count.append(program.like_count())
        program_data = {
            'id' : program_id,
            'code' : code,
            'author' : author,
            'time_stamp' : time_stamp,
            'total_rating' : total_ratings,
            'like_count' : like_count
        }
        params = {
            'exists' : exists,
            'title_id' : title.id,
            'title' : title.title,
            'language' : title.language,
            'prism_name' : title.prism_name,
            'answer_count' : title.answers,
            'programs' : program_data,
        }
        caches['program'].set(program_key, params, 10*60)
    
    user_auth = False
    if request.user.is_authenticated:
        user_auth = True 
        user_key = 'user/' + str(request.user.username) + '/'
        user_cache_value = caches['user'].get(user_key)
        like_data = list()
        rating = list()
        for id in params['programs']['id']:
            # handle the liking
            if int(id) in user_cache_value['program']['like']:
                like_data.append(True)
            else:
                like_data.append(False)

            # handle the rating
            try:
                rating.append(user_cache_value['program']['rating'][id])
            except:
                rating.append(0)


        params['like_data'] = like_data
        params['rating'] = rating
    else:
        params['like_data'] = list()
        params['rating'] = list()

    params['user_auth'] = user_auth
    return JsonResponse(params)







# Handle rating
@csrf_exempt
def rating(request):
    if request.method == 'POST':
        code_id = request.POST['id']
        rate = float(request.POST['rate'])
        if rate > 5:
            rate = 5
        if rate <= 0:
            rate = 1
        
        program_obj = Program.objects.get(id=code_id)
        slug = program_obj.title.slug

        return_data = upade_rating_cache(code_id, slug, request.user.username, rate)


        if return_data:
            pr = program_rating.objects.get(program=program_obj, user = request.user)
            pr.rating = rate
            pr.save()
            return HttpResponse(True)

        else:
            if program_rating.objects.filter(program=program_obj, user = request.user).exists():
                pr = program_rating.objects.get(program=program_obj, user = request.user)
                pr.rating = rate
                pr.save()
                return HttpResponse(True)

            else:
                pr = program_rating.objects.create(
                    user=request.user, program=program_obj, rating=rate)
                pr.save()
                return HttpResponse(True)

    return HttpResponse(False)







def add(request, lang):
    if request.method == 'POST':
        language = request.POST["language_name"]
        return redirect("program_add", lang=language)

    language = check_language(lang)
    if language != None:
        category = language.category.split(",")
        if "Program" in category or 'program' in category:
            if not request.user.is_authenticated:
                messages.success(request, 'Please Login First')
                url = cpp_checker(request.GET.get('next'))
                return redirect(url)
            form = add_program_code(
                request.POST or None, request.FILES or None)
            meta = Meta(
                title="ARCODERS PROGRAM",
                description='Add Program to ARCODERS PROGRAMS',
                keywords=meta_data + [language.name],
                extra_props={
                    'viewport': 'width=device-width, initial-scale=1.0, minimum-scale=1.0'},
                extra_custom_props=[('http-equiv', 'Content-Type', 'text/html; charset=UTF-8'),
                                    ]
            )

            params = {"language": language, "cat": cat, "form": form}
            return render(request, "program/add.html", params)
