from django.core import serializers
from django.db.models import query
from django.db.models.query_utils import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate
from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from meta.views import Meta  # For Meta Data


# importing Models
from django.contrib.auth.models import User
from arcoder.models import Language
from .forms import add_query, add_solution
from .models import *
from arcoder.language_name import prism_name


# for user caching
from django.core.cache import cache, caches
from cache_key_generator import get_cache_key
from django.http import JsonResponse
from querybook.models import Solutions, Query, solution_rating

from arcoder.my_function import check_language, query_title_remove_quotations

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


# edit the code for prism
def edit_solution(solution,prism):
    # for 1 line space
    solution = solution.replace(
        '</code></p>\r\n\r\n<p>&nbsp;</p>\r\n\r\n<p><code>', '<br>\r\n\n')
    # for no space
    solution = solution.replace('</code></p>\r\n\r\n<p><code>', '<br>\r\n')
    solution = solution.replace(
        '<code>', f'<body class="line-numbers"><pre class="code" > <code class="language-{prism}">')
    solution = solution.replace(
        '</code>', f'</code></pre></body>')
    return solution

# removing the prism code edit
def reverse_solution(solution, prism):
    # for 1 line space
    solution = solution.replace('<br>\r\n\n', '</code></p>\r\n\r\n<p>&nbsp;</p>\r\n\r\n<p><code>')
    # for no space
    solution = solution.replace('<br>\r\n', '</code></p>\r\n\r\n<p><code>')
    solution = solution.replace(f'<body class="line-numbers"><pre class="code" > <code class="language-{prism}">', '<code>')
    solution = solution.replace(f'</code></pre></body>', '</code>')
    return solution



# updating the (user and solution) cache while liking the program
def update_like_cache(slug, username, id):   
    id = int(id)
    # for caching data
    user_key = 'user/' + str(username) + '/'
    user_cache_value = caches['user'].get(user_key)

    query_key = 'query/' + str(slug) + '/'
    query_cache_value = caches['query'].get(query_key)



    if user_cache_value is not None:
        if int(id) in user_cache_value['querybook']['like']:
            # updating user cache value
            cache_value = user_cache_value
            caches['user'].delete(user_key)
            cache_value['querybook']['like'].remove(id)
            caches['user'].set(user_key, cache_value, 10*60)

            if query_cache_value is not None:
                index = query_cache_value['solutions']['id'].index(int(id))
                # updating program cache value
                temp_cache_value = query_cache_value
                caches['query'].delete(query_key)
                temp_cache_value['solutions']['like_count'][index] -= 1
                caches['query'].set(query_key, temp_cache_value, 10*60)

            return False

        else:
            # updating user cache value
            cache_value = user_cache_value
            caches['user'].delete(user_key)
            cache_value['querybook']['like'].append(id)
            caches['user'].set(user_key, cache_value, 10*60)
            
            if query_cache_value is not None:
                index = query_cache_value['solutions']['id'].index(int(id))
                # updating program cache value
                temp_cache_value = query_cache_value
                caches['query'].delete(query_key)
                temp_cache_value['solutions']['like_count'][index] += 1
                caches['query'].set(query_key, temp_cache_value, 10*60)


            return True
    else:
        return None



# updating the (user and query) cache while rating the program
def upade_rating_cache(id, slug, username, rate):
    id = int(id)
    # for caching data
    user_key = 'user/' + str(username) + '/'
    user_cache_value = caches['user'].get(user_key)

    query_key = 'query/' + str(slug) + '/'
    query_cache_value = caches['query'].get(query_key)

    if int(id) in user_cache_value['querybook']['rating']:
        previous_rate = user_cache_value['querybook']['rating'][id]
    else:
        previous_rate = 0

    if query_cache_value is not None:
        index = query_cache_value['solutions']['id'].index(int(id))
        # updating program cache value
        temp_cache_value = query_cache_value
        caches['query'].delete(query_key)
        if previous_rate == 0:
            temp_cache_value['solutions']['total_rating'][index][1] += 1

        count = temp_cache_value['solutions']['total_rating'][index][1]

        temp_cache_value['solutions']['total_rating'][index][2] = temp_cache_value[
            'solutions']['total_rating'][index][2] - previous_rate + rate

        total = temp_cache_value['solutions']['total_rating'][index][2]
        total_rating = int(total*20/count)
        temp_cache_value['solutions']['total_rating'][index][0] = total_rating
        caches['query'].set(query_key, temp_cache_value, 10*60)


    # handling the user cache
    if user_cache_value is not None:
        if int(id) in user_cache_value['querybook']['rating']:
            # updating user cache value
            cache_value = user_cache_value
            caches['user'].delete(user_key)
            cache_value['querybook']['rating'][id] = rate
            count = len(cache_value['querybook']['rating'])
            sum = (cache_value['user_data']['solution_rating']
                   * (count-1)) + (rate * 20)
            cache_value['user_data']['solution_rating'] = sum/count

            caches['user'].set(user_key, cache_value, 10*60)

        else:
            # updating user cache value
            cache_value = user_cache_value
            caches['user'].delete(user_key)
            cache_value['querybook']['rating'][id] = rate
            count = len(cache_value['querybook']['rating'])
            sum = (cache_value['user_data']['solution_rating']
                   * (count-1)) + (rate * 20)
            cache_value['user_data']['solution_rating'] = sum/count

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
# it store the number of queries will display on a particular page
no_of_queries = 5
cat = 'Querybook'
meta_data = ['ARCODERS', 'Query', 'Querybook', 'Solution', 'Programming']
all_languages = get_languages()


##########################
# Create your views here.#
##########################
def querybook(request, lang = None):
    language = check_language(lang)

    if language != None:
        category = language.category.split(',')
        if 'Querybook' in category or 'querybook' in category:
            query_key = language.name + '/'
            query_cache_value = caches['query'].get(query_key)

            if query_cache_value is not None:
                queries = query_cache_value['queries']
            else:
                queries = Query.objects.filter(language=language)
                params = {'queries': queries}
                caches['query'].set(query_key, params, 1*60)
        else:
            redirect('querybook')
    else:
        # handling for all the languages
        query_key = 'query/'
        query_cache_value = caches['query'].get(query_key)

        if query_cache_value is not None:
            queries = query_cache_value['queries']
        else:
            queries = Query.objects.all()
            params = {'queries': queries}
            caches['query'].set(query_key, params, 1*60)

    paginator = Paginator(queries, no_of_queries)
    page_number = request.GET.get('page')
    try:
        query_data = paginator.page(page_number)
    except PageNotAnInteger:
        query_data = paginator.page(1)
    except EmptyPage:
        query_data = paginator.page(paginator.num_pages)

    query_data = query_title_remove_quotations(query_data)
    query_data_json = serializers.serialize('json', query_data)

    # for meta data and params
    if language == None:
        meta_language = all_languages
        language_name = ''
    else:
        meta_language = [language.name]
        language_name = language.name

    meta = Meta(
        title="ARCODERS QUERYBOOK",
        description='ARCODERS QUERYBOOK:- Here you get the stuff related to programming.',
        keywords=meta_data + meta_language,
        extra_props={
            'viewport': 'width=device-width, initial-scale=1.0, minimum-scale=1.0'},
        extra_custom_props=[('http-equiv', 'Content-Type', 'text/html; charset=UTF-8'),
                            ]
    )

    params = {'cat': cat, 
    'data': query_data, 
    'json_data':query_data_json, 
    'meta': meta, 
    'paginator_data':query_data, 
    'language':language_name, 
    'title_prefix':''}
    return render(request, 'querybook/querybook.html', params)


# form will add the Query(Questions)
# handle post request and save it into the database
def query_form(request):
    if request.user.is_authenticated:
        if request.method == 'POST':

            form_data = add_query(request.POST)
            form_data.is_valid()
            query = form_data.cleaned_data['query']
            description = form_data.cleaned_data['description']
            if description == '':
                description = 'No description'
            language = request.POST['language']

            username = request.user.username
            user = User.objects.get(username=username)
            if not Query.objects.filter(query=query, language=language, description=description).exists():
                prism = prism_name[language]
                save_data = Query(query=query, description=description, author=user, language=language, prism_name = prism)
                save_data.save()
                messages.error(request, " Your Query is SucessFully Added in our Querybook")
                return redirect("querybook_add", lang=language)

            else:
                messages.error(
                    request, " Your Query is already Exists in our Querybook")
                return redirect('querybook_add', lang=language)

    messages.error(request, "Something Gone Wrong, Try Again!")
    return redirect('querybook_add', lang='Python')

    # messages.error(request, "Login to Add Queries in Querybook !!!")
    # return redirect("querybook_add", lang=language)


# it handle html pages also
# form will add the Solution
# handle post request and save it into the database
def solution_form(request, language, query_slug):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form_data = add_solution(request.POST)
            if form_data.is_valid():
                query = Query.objects.get(slug=query_slug)
                solution = form_data.cleaned_data['solution']

                username = request.user.username
                user = User.objects.get(username=username)
                prism = query.prism_name
                solution = edit_solution(solution, prism)

                # saving the solution
                save_data = Solutions(
                    query=query, solution=solution, author=user)
                save_data.save()

                query_key = 'query/' + str(query.slug) + '/'
                query_cache_value = caches['query'].get(query_key)

                if query_cache_value is not None:
                    # updating program cache value
                    temp_cache_value = query_cache_value
                    caches['query'].delete(query_key)
                    temp_cache_value['answer_count'] += 1
                    temp_cache_value['solutions']['id'].append(save_data.id)
                    temp_cache_value['solutions']['solution'].append(save_data.solution)
                    temp_cache_value['solutions']['author'].append(request.user.username)
                    temp_cache_value['solutions']['time_stamp'].append(save_data.time_stamp)
                    temp_cache_value['solutions']['total_rating'].append([0,0,0])
                    temp_cache_value['solutions']['like_count'].append(0)
                    caches['program'].set(query_key, temp_cache_value, 10*60)


                # Increasing the number of solution in Query Model
                answer = query.answer
                query.answer = answer + 1
                query.save()
                messages.error(
                    request, " Your Solution is SucessFully Added in our Querybook")

                return redirect('final_query', language=language, query_slug=query_slug)
    messages.error(request, "Login to Add Queries in Querybook !!!")
    return redirect('final_query', language=language, query_slug=query_slug)


# function will handle request related to Querybook of particular language
def language(request, lang=None):
    language = check_language(lang)
    if language != None:
        category = language.category.split(',')
        if 'Querybook' in category or 'querybook' in category:
            query_key = lang + '/'
            query_cache_value = caches['query'].get(query_key)

            if query_cache_value is not None:
                queries = query_cache_value['queries']

            else:
                queries = Query.objects.filter(language=language)
                params = {
                    'queries': queries,
                }
                caches['query'].set(query_key, params, 1*60)


            paginator = Paginator(queries, no_of_queries)
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
                keywords=meta_data + [lang],
                extra_props={
                    'viewport': 'width=device-width, initial-scale=1.0, minimum-scale=1.0'},
                extra_custom_props=[
                    ('http-equiv', 'Content-Type', 'text/html; charset=UTF-8'), ]
            )

            params = {'language': language.name,
                      'cat': cat, 'data': datas, 'meta': meta}
            return render(request, 'querybook/querybook.html', params)


# Handle final Qurey page to show all solutions
def final_query(request, language, query_slug):
    language = check_language(language)
    if language != None:
        category = language.category.split(',')
        if 'Querybook' in category or 'querybook' in category:
            query = Query.objects.get(language=language.name, slug=query_slug)

            # solution form
            form = add_solution(request.POST or None, request.FILES or None)

    meta = Meta(
        title="ARCODERS QUERYBOOK:- " + query.query,
        description=query.query,
        keywords=meta_data + [query.query, query.language],
        extra_props={
            'viewport': 'width=device-width, initial-scale=1.0, minimum-scale=1.0'},
        extra_custom_props=[('http-equiv', 'Content-Type', 'text/html; charset=UTF-8'),
                            ]
    )

    # params = {'cat': cat, 'query': query,
    #           'solutions': solutions, 'meta': meta, 'form': form, 'rating' : True, 'slug' : query_slug}
    params = {'cat': cat, 'query': query, 'meta': meta, 'form': form, 'rating' : True, 'slug' : query_slug}
    return render(request, 'querybook/final.html', params)




# Handeling the like
@csrf_exempt
def like(request):
    if request.method == 'POST':
        id = request.POST['id']

        solution_obj = Solutions.objects.get(id=id)
        return_value = update_like_cache(solution_obj.query.slug, request.user.username, id)


        # handling program cache
        query_key = 'query/' + str(solution_obj.query.slug) + '/'
        query_cache_value = caches['query'].get(query_key)


        if return_value is None:
            if solution_obj.like.filter(id=request.user.id).exists():
                solution_obj.like.remove(request.user)

                if query_cache_value is not None:
                    index = query_cache_value['solutions']['id'].index(int(id))
                    # updating program cache value
                    temp_cache_value = query_cache_value
                    caches['query'].delete(query_key)
                    temp_cache_value['solutions']['like_count'][index] -= 1
                    caches['query'].set(query_key, temp_cache_value, 10*60)


                return HttpResponse(False)

            else:
                solution_obj.like.add(request.user)

                if query_cache_value is not None:
                    index = query_cache_value['solutions']['id'].index(int(id))
                    # updating query cache value
                    temp_cache_value = query_cache_value
                    caches['query'].delete(query_key)
                    temp_cache_value['solutions']['like_count'][index] += 1
                    caches['query'].set(query_key, temp_cache_value, 10*60)


                return HttpResponse(True)


        else:
            if return_value:
                solution_obj.like.add(request.user)
                return HttpResponse(True)

            else:
                solution_obj.like.remove(request.user)
                return HttpResponse(False)






# Handle form page
def add(request, lang):
    if request.method == 'POST':
        language = request.POST['language_name']
        return redirect('querybook_add', lang=language)

    language = check_language(lang)
    if language != None:
        category = language.category.split(',')
        if 'Querybook' in category or 'querybook' in category:
            if not request.user.is_authenticated:
                messages.success(request, 'Please Login First')
                url = cpp_checker(request.GET.get('next'))
                return redirect(url)


            form = add_query(request.POST or None, request.FILES or None)

            meta = Meta(
                title="ARCODERS QUERYBOOK",
                description='Add Query to ARCODERS QUERYBOOK',
                keywords=meta_data + [language.name],
                extra_props={
                    'viewport': 'width=device-width, initial-scale=1.0, minimum-scale=1.0'},
                extra_custom_props=[('http-equiv', 'Content-Type', 'text/html; charset=UTF-8'),
                                    ]
            )

            params = {'language': language, 'cat': cat, 'form': form}
            return render(request, 'querybook/query_add.html', params)





# get query data
def get_query_data(request, slug):
    query_key = 'query/' + str(slug) + '/'
    query_cache_value = caches['query'].get(query_key)

    if query_cache_value is not None:
        params = query_cache_value

    else:
        exists = False
        query = Query.objects.get(slug=slug)
        if query is not None:
            exists = True

        solutions = Solutions.objects.filter(query = query)
        solution_id = list()
        total_ratings = list()
        data = list()
        author = list() 
        time_stamp = list()
        like_count = list()
        prism = query.prism_name
        for solution in solutions:
            total_ratings.append(solution.total_rating())
            data.append(solution.solution)
            solution_id.append(solution.id)
            author.append(solution.author.username)
            time_stamp.append(solution.time_stamp)
            like_count.append(solution.likeCount())
        solution_data = {
            'id' : solution_id,
            'solution' : data,
            'author' : author,
            'time_stamp' : time_stamp,
            'total_rating' : total_ratings,
            'like_count' : like_count
        }
        params = {
            'exists' : exists,
            'title_id' : query.id,
            'title' : query.query,
            'language' : query.language,
            # 'prism_name' : query.prism_name,
            'answer_count' : query.answer,
            'solutions' : solution_data,
            'description': query.description,
            'time_stamp' : query.time_stamp,
            'author' : query.author.username
        }
        caches['query'].set(query_key, params, 10*60)
    
    user_auth = False
    if request.user.is_authenticated:
        user_auth = True 
        user_key = 'user/' + str(request.user.username) + '/'
        user_cache_value = caches['user'].get(user_key)
        like_data = list()
        rating = list()
        for id in params['solutions']['id']:
            # handle the liking
            if int(id) in user_cache_value['querybook']['like']:
                like_data.append(True)
            else:
                like_data.append(False)

            # handle the rating
            try:
                rating.append(user_cache_value['querybook']['rating'][id])
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
        solution_id = request.POST['id']
        rate = float(request.POST['rate'])
        if rate > 5:
            rate = 5
        if rate <= 0:
            rate = 1
        
        solution_obj = Solutions.objects.get(id=solution_id)
        slug = solution_obj.query.slug

        return_data = upade_rating_cache(solution_id, slug, request.user.username, rate)


        if return_data:
            sr = solution_rating.objects.get(solution=solution_obj, user = request.user)
            sr.rating = rate
            sr.save()
            return HttpResponse(True)

        else:
            if solution_rating.objects.filter(solution=solution_obj, user = request.user).exists():
                sr = solution_rating.objects.get(solution=solution_obj, user = request.user)
                sr.rating = rate
                sr.save()
                return HttpResponse(True)

            else:
                sr = solution_rating.objects.create(
                    user=request.user, solution=solution_obj, rating=rate)
                sr.save()
                return HttpResponse(True)

    return HttpResponse(False)

