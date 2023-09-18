from django.db.models.expressions import F
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, UserManager
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.apps import apps
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from random import randint
from time import time
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
import json

from django.core.cache import cache, caches
from custom_cache_page.cache import cache_page
from custom_cache_page.utils import generate_query_params_cache_key
from cache_key_generator import get_cache_key

# Email stuff
from django.template.loader import render_to_string
from django.utils.html import json_script, linebreaks, strip_tags
from django.core.mail import EmailMultiAlternatives
from ARCODERS import settings

from program.views import add_program
from querybook.forms import add_query, add_solution

from .language_name import prism_name

# Forms
from program.forms import add_program_code
from .forms import privacy_form
# Models
from .models import *
from program.models import program_title, Program, program_rating
from querybook.models import Solutions, Query, solution_rating

# For Meta Data
from meta.views import Meta

# To delete the image
from shutil import rmtree

from django.core.cache import cache, caches
from custom_cache_page.cache import cache_page
from custom_cache_page.utils import generate_query_params_cache_key
from cache_key_generator import get_cache_key
from arcoder.my_function import program_title_remove_quotations, check_language


#####################
# Required Functions#
#####################
# this function take the next url and replace the 'c  ' in c++
no_of_blogs = 5


def cpp_checker(url):
    url = url.replace('C  ', 'C++')
    return url


def check_language(lang):
    try:
        if lang == 'C  ':
            lang = 'C++'
        language = Language.objects.get(name=lang)
    except:
        language = None
    return language


def get_languages():
    languages = Language.objects.all()
    lang_list = []
    for lang in languages:
        lang_list.append(lang.name)
    return lang_list


# removing the prism code edit
def reverse_solution(solution):
    # for 1 line space
    solution = solution.replace('<br>\r\n\n', '</code></p>\r\n\r\n<p>&nbsp;</p>\r\n\r\n<p><code>')
    # for no space
    solution = solution.replace('<br>\r\n', '</code></p>\r\n\r\n<p><code>')
    solution = solution.replace(f'<body class="line-numbers"><pre class="code" >', '<code>')
    solution = solution.replace(f'</code></pre></body>', '</code>')
    return solution

# edit the code for prism
def edit_solution(temp_solution):
    # for 1 line space
    temp_solution = temp_solution.replace(
        '</code></p>\r\n\r\n<p>&nbsp;</p>\r\n\r\n<p><code>', '<br>\r\n\n')
    # for no space
    temp_solution = temp_solution.replace('</code></p>\r\n\r\n<p><code>', '<br>\r\n')
    temp_solution = temp_solution.replace(
        '<code', f'<body class="line-numbers"><pre class="code" > <code')
    temp_solution = temp_solution.replace(
        '</code>', f'</code></pre></body>')
    return temp_solution


#####################
# Required Variables#
#####################
# it store the number of blog will display on a particular page
# no_of_blogs = 3
meta_data = ['ARCODERS', 'Programming', 'Programs',
             'codes', 'Querybook', 'Home']
all_languages = get_languages()


# Create your views here.

# Home Page
def home(request):
    meta = Meta(
        title="ARCODERS:- Programs, Querybook",
        description='ARCODERS:- Here you get the stuff related to programming. We provide programs and query solutions related to diffrent programming languages.',
        keywords=meta_data + all_languages,
        extra_props={
            'viewport': 'width=device-width, initial-scale=1.0, minimum-scale=1.0'},
        extra_custom_props=[('http-equiv', 'Content-Type', 'text/html; charset=UTF-8'),
                            ]
    )

    params = {'meta': meta}
    return render(request, 'arcoder/home.html', params)



# def manifest(request):
#     return render(request, 'arcoder/manifest.json')


def ads(request):
    return render(request, 'ads.txt')



def navbar(request):
    if request.user.is_authenticated:
        params = {'username':request.user.username, 'auth': True}
        return JsonResponse(params)    
    else:
        params = {'auth': False}
        return JsonResponse(params)    


# Particular Language Page
@cache_page(
    timeout=60 * 10,
    key_func=lambda r: r.path,
    versioned=0,
    group_func=lambda r: 'cached_views',
    prefix='language'
)
def language(request, lang):
    language = check_language(lang)
    if language != None:
        program_text = f'Find the best {language.name} Programs.'
        querybook_text = f'Find the best solutions of {language.name} Query.'
        text = {'program' : program_text, 'querybook' : querybook_text}
        meta = Meta(
            title="ARCODERS:- Blogs, Programs, Tutorials, Projects, Querybook",
            description='ARCODERS:- Here you get the stuff related to programming. We provide programs and query solutions related to diffrent programming languages.',
            keywords=meta_data + [language.name],
            extra_props={
                'viewport': 'width=device-width, initial-scale=1.0, minimum-scale=1.0'},
            extra_custom_props=[('http-equiv', 'Content-Type', 'text/html; charset=UTF-8'),
                                ]
        )

        params = {'language': language, 'text' : text, 'meta': meta}
        return render(request, 'arcoder/language.html', params)


# Contact Page
def contact(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            name = request.POST['name']
            email = request.POST['email']
            desc = request.POST['desc']
            user_data = request.user

            mail_subject = 'ARCODER-Contact Us.'
            html_content = render_to_string('arcoder/contact_us.html', {
                'user': user_data, 'desc': desc, 'name' : name, 'email': email})

            text_content = strip_tags(html_content)
            to_email = 'Anuragrai15march@gmail.com'
            email_send = EmailMultiAlternatives(
                mail_subject, text_content, settings.EMAIL_HOST_USER, to=[to_email])
            email_send.attach_alternative(html_content, 'text/html')
            email_send.send()
            messages.error(request, 'We will contact you soon regarding your problem!!!')
            return render(request, 'arcoder/home.html')

        else:
            meta = Meta(
                title="ARCODERS Contact",
                description='ARCODERS:- Here you get the stuff related to programming. We provide programs and query solutions related to diffrent programming languages.',
                keywords=['ARCODERS', 'Contact'],
                extra_props={
                    'viewport': 'width=device-width, initial-scale=1.0, minimum-scale=1.0'},
                extra_custom_props=[('http-equiv', 'Content-Type', 'text/html; charset=UTF-8'),
                                    ]
            )
            params = {'meta': meta}
            return render(request, 'arcoder/contact.html', params)
    else:
        messages.error(request, 'You need to Login first!!!')
        return render(request, 'arcoder/home.html')


# Validating the OTP
def otp_verification(request, url_otp):
    user_detail_obj = user_detail.objects.filter(url_otp=url_otp).first()
    if user_detail_obj == None:
        messages.success(request, 'Please Create Account first !!!')
        return redirect('sign_up')

    # run = time_otp(user_detail_obj.profile_created_at)
    run = True
    if run:
        if user_detail_obj != None:
            user_detail_obj.url_otp = '1503023333'
            user = User.objects.filter(
                username=user_detail_obj.user.username).first()
            user.is_active = True
            user_detail_obj.save()
            user.save()
            messages.success(
                request, 'Account Created successfully! Please Login')
            return redirect('home')
        else:
            messages.success(request, 'Please Create Account First!')
            return redirect('sign_up')


# Handle Sign up and sign up post request
def sign_up(request):
    if request.method == 'POST':
        username = request.POST['username'].lower()
        fname = request.POST['fname']
        lname = request.POST['lname']
        gender = request.POST['gender']
        # date format yyyy-dd-mm
        dob_temp = request.POST['DOB'].split('-')[::-1]
        month = dob_temp[1]
        day = dob_temp[0]
        dob_temp[0] = day
        dob_temp[1] = month
        DOB = '-'.join(dob_temp)


        email = request.POST['email']
        email = email.lower()
        # phone = request.POST['phone']
        pass1 = request.POST['password1']
        pass2 = request.POST['password2']

        # Check for errorneous inputs

        # passwords should match
        if pass1 != pass2:
            messages.error(request, "Passwords do not match")
            return redirect('sign_up')

        # checking unique Phone Number
        # phoneRegister = userDetail.objects.filter(phone=phone)
        # if len(phoneRegister) > 0:
        #     messages.error(request, "Phone Number is already Registered!")
        #     return redirect('signup')

        # checking unique Email
        email_register = User.objects.filter(email=email)
        if len(email_register) > 0:
            messages.error(request, "Email is already Registered!")
            return redirect('sign_up')

        # Create the user
        try:
            user = User.objects.create_user(username, email, pass1)
        except Exception as e:
            messages.error(request, "username is already Registered!")
            return redirect('sign_up')

        user.first_name = fname
        user.last_name = lname
        user.is_active = False
        user.save()
        otp = ""
        url_otp = ""
        i = 0

        while i < 6:
            otp += str(randint(0, 9))
            url_otp += str(randint(0, 9))
            i += 1
        while i < 10:
            url_otp += str(randint(0, 9))
            i += 1

        # today_date = datetime.date.today()
        # # dob = today_date.strftime("%d/%m/%y")
        user_detail_obj = user_detail(
            user=user, gender=gender, otp=otp, url_otp=url_otp, dob = DOB)
        user_detail_obj.save()

        # domain will not work for local host
        # domain = '127.0.0.1:8000/otp_verification/'
        domain = 'www.arcoders.com/otp_verification/'
        # testing
        # domain = 'www.stackoverflw.com/'
        url = domain + url_otp
        mail_subject = 'Activate your ARCODERS account.'
        html_content = render_to_string('arcoder/acc_active_email.html', {
                                   'user': user, 'url': url})

        text_content = strip_tags(html_content)
        to_email = email
        email_send = EmailMultiAlternatives(
            mail_subject, text_content, settings.EMAIL_HOST_USER, to=[to_email])
        email_send.attach_alternative(html_content, 'text/html')
        # email_send = EmailMessage(mail_subject, text_content, to=[to_email])
        # email_send.content_subtype = 'html'
        email_send.send()

        messages.success(request, "Please conform your accout at " + email+".")
        # params= {"user":user}
        return redirect("home")

    if request.user.is_authenticated:
        messages.success(request, "Please Log out to create New Account")
        return render(request, 'arcoder/home.html')
        # return redirect("Home")
    else:
        return render(request, 'arcoder/sign_up.html')


# Handle Login
def log_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            url = cpp_checker(request.GET.get('next'))
            if 'page' in url:
                return redirect(url+'&next=/')
            else:
                return redirect(url+'?next=/')

        else:
            messages.error(request, 'Invalid Credentials, Plase try Again!')
            url = cpp_checker(request.GET.get('next'))
            return redirect(url+'?auth=lg')


# Handle log out
@login_required()
def log_out(request):
    logout(request)
    messages.success(request, 'Successfully Logged Out!!!')
    try:
        url = cpp_checker(request.GET.get('next'))
        if 'page' in url:
            return redirect(url+'&next=/')
        else:
            return redirect(url+'?next=/')
    except:
        return redirect('home')


# Handle User Profile
@login_required()
def user(request):
    user_key = 'user/' + str(request.user.username) + '/'
    user_cache_value = caches['user'].get(user_key)

    no_of_programs = len(Program.objects.filter(author=request.user))
    no_of_solutions = len(Solutions.objects.filter(author=request.user))
    no_of_querys = len(Query.objects.filter(author=request.user))
    
    if user_cache_value is not None:
        # getting the data from the cache 
        user = user_cache_value['user']
        user_data = user_cache_value['user_data']

        user_data['programs'] = no_of_programs
        user_data['querys'] = no_of_querys 
        user_data['solutions'] = no_of_solutions
        
        user_data['program_rating'] = round(user_data['program_rating'], 2) 
        user_data['solution_rating'] = round(user_data['solution_rating'], 2) 
        form = privacy_form(request.POST or None, request.FILES or None, initial={'privacy': user_data['privacy']})

    else:
        user = User.objects.get(username=request.user.username)
        user_data = user_detail.objects.get(user=request.user)

        user_data.programs = no_of_programs
        user_data.solutions = no_of_solutions
        user_data.querys = no_of_querys
        


        form = privacy_form(request.POST or None, request.FILES or None, initial={
                'privacy': user_data.privacy})

    params = {'user_data': user_data, 'user': user, 'privacy_form': form 
              }
    return render(request, 'arcoder/user_profile.html', params)


# handle privacy
@login_required()
def user_privacy(request):
    if request.method == 'POST':
        form_data = privacy_form(request.POST)
        if form_data.is_valid():
            privacy = form_data.cleaned_data['privacy']        
            user_data = user_detail(user = request.user)
            user_data.privacy = privacy
            user_data.save()

            # updating the cache data
            user_key = 'user/' + str(request.user.username) + '/'
            user_cache_value = caches['user'].get(user_key)
            if user_cache_value is not None:
                cache_value = user_cache_value
                caches['user'].delete(user_key)
                cache_value['user_data']['privacy'] = privacy
                caches['user'].set(user_key, cache_value, 10*60)

            messages.error(request, 'Your Email privacy has been updated!!!')
            return redirect('user')


# change user image
@login_required()
def upload_image(request):
    if request.method == 'POST':
        user_data = user_detail(user = request.user)

        # for adding the profile image
        try:
            rmtree(f'media/files/image/user/{request.user.username}')
        except:
            pass

        user_data.image = request.FILES['image']
        user_data.save()
    

        # updating the cache data
        user_key = 'user/' + str(request.user.username) + '/'
        user_cache_value = caches['user'].get(user_key)
        if user_cache_value is not None:
            cache_value = user_cache_value
            caches['user'].delete(user_key)
            cache_value['user_data']['image'] = user_data.image
            caches['user'].set(user_key, cache_value, 10*60)



        
        return HttpResponse(True)
    else:
        return redirect('user')


# remove image
@login_required()
def remove_image(request):
    user_data = user_detail(user = request.user)
    user_data.image = 'user.png'
    user_data.save()
    try:
        rmtree(f'media/files/image/user/{request.user.username}')
    except:
        pass


    # updating the cache data
    user_key = 'user/' + str(request.user.username) + '/'
    user_cache_value = caches['user'].get(user_key)
    if user_cache_value is not None:
        cache_value = user_cache_value
        caches['user'].delete(user_key)
        cache_value['user_data']['image'] = user_data.image
        caches['user'].set(user_key, cache_value, 10*60)

    return redirect('user')



# Handle Editing user Program page
@login_required()
def edit_program(request, language, program_id):
    program = Program.objects.get(id = program_id)
    if program.author != request.user:
        messages.error(request, 'Something Gone Wrong!!!')
        return redirect('user_program')
        


    if request.method == 'POST':
        form = add_program_code(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            code = code.replace('<', '&lt;')
            code = code.replace('>', '&gt;')
            code = '<code>' + code + '</code>'

            program.code = code

            # Handeling the language
            program.url = request.POST['url']
            program.save()

            # handle the program caching 
            program_key = 'program/' + str(program.title.slug) + '/'
            program_cache_value = caches['program'].get(program_key)

            program_id = int(program.id)

            if program_cache_value is not None:
                # updating program cache value
                if program_id in program_cache_value['programs']['id']:
                    index = program_cache_value['programs']['id'].index(program_id)
                
                    temp_cache_value = program_cache_value
                    caches['program'].delete(program_key)
                    temp_cache_value['programs']['code'][index] = program.code
                    caches['program'].set(program_key, temp_cache_value, 10*60)



            messages.error(request, 'Program is Successfully Updated!!!')
            # return redirect('edit_program', language=program.title.language, program_id=program.title.id)
            return redirect('user_program')

        messages.error(
            request, 'Something Gone Wrong. Program did not Updated.')

        return redirect('edit_program', language=language, program_id=program_id)

    # Handeling GET request
    language = check_language(language)
    if language != None:
        category = language.category.split(',')
        if 'Program' in category or 'program' in category:
            if program.code[0:6] == '<code>':
                program.code = program.code[6:-7]

            form = add_program_code(request.POST or None, request.FILES or None, initial={
                'code': program.code, 'title': program.title.title})
            program.cat = 'Program'
            params = {'program': program, 'form': form}
            return render(request, 'arcoder/user_profile/program/add.html', params)

import random

# Handle Editing user Query page
@login_required()
def edit_query(request, language, query_id):
    # for security check
    query = Query.objects.get(id=query_id)
    if request.user != query.author:
        messages.error(request, 'Something Gone Wrong!!!')
        return redirect('user_query')

    if int(query.answer) > 0:
        messages.error(request, 'Sorry, the query had a solution, Now it cannot be changed!!!') 
        return redirect('user_query')

    if request.method == 'POST':
        form = add_query(request.POST)
        if form.is_valid():
            # query = Query.objects.get(id=query_id)
            query.query = form.cleaned_data['query']
            query.description = form.cleaned_data['description']
            query.language = request.POST['language']
            temp_slug = form.cleaned_data['query'].replace(' ', '-')
            query.slug = temp_slug + str(query_id) + str(random.randint(100, 999))
            query.save()

            messages.error(
                request, 'Query is Successfully Updated in Querybook!!!')
            # return redirect('edit_querybook', language=language, solution_id=solution.id)
            return redirect('user_query')

        messages.error(request, 'Something Gone Wrong. Query did not get Updated.')
        return redirect('edit_query', language=language, query_id=query_id)

    # Handeling GET request
    language = check_language(language)
    if language != None:
        category = language.category.split(',')
        if 'Querybook' in category or 'querybook' in category:
            # query = Query.objects.get(id=query_id)
            form = add_query(request.POST or None, request.FILES or None, initial={
                'query': query.query, 'description': query.description})

            params = {'cat':'Query', 'query': query, 'form': form}
            return render(request, 'arcoder/user_profile/query/query_add.html', params)


# Handle Editing user solution page
@login_required()
def edit_solution(request, language, solution_id):
    # for security check
    solution = Solutions.objects.get(id = solution_id)
    # solution.solution = reverse_solution(solution.solution)
    query = solution.query
    prism = query.prism_name
    if solution.author != request.user:
        messages.error(request, 'Something Gone Wrong!!!')
        return redirect('user_solution')

    if request.method == 'POST':
        form = add_solution(request.POST)
        if form.is_valid():
            temp_solution = form.cleaned_data['solution']
            temp_solution = temp_solution.replace(
        '<code>', f'<body class="line-numbers"><pre class="code" > <code class="language-{prism}">')
            temp_solution = temp_solution.replace(
        '</code>', f'</code></pre></body>')

            solution.solution = temp_solution
            solution.save()

            # handle caching
            query_key = 'query/' + str(query.slug) + '/'
            query_cache_value = caches['query'].get(query_key)

            solution_id = int(solution.id)

            if query_cache_value is not None:
                # updating program cache value
                if solution_id in query_cache_value['solutions']['id']:
                    index = query_cache_value['solutions']['id'].index(solution_id)

                temp_cache_value = query_cache_value
                caches['query'].delete(query_key)
                temp_cache_value['solutions']['solution'][index] = solution.solution
                caches['query'].set(query_key, temp_cache_value, 10*60)


            messages.error(request, 'Solution is Successfully Updated in Querybook!!!')
            # return redirect('edit_querybook', language=language, solution_id=solution.id)
            return redirect('user_solution')


        messages.error(request, 'Something Gone Wrong. Solution did not Updated.')
        return redirect('edit_querybook', language=language, solution_id=solution_id)

    # Handeling GET request
    language = check_language(language)
    if language != None:
        category = language.category.split(',')
        if 'Querybook' in category or 'querybook' in category:
            form = add_solution(request.POST or None, request.FILES or None, initial={
                'solution': solution.solution})
            solution.cat = 'Querybook'

            params = {'cat':'Query', 'solution': solution, 'form': form}
            # params = {'solution_data': soution, 'form': form}
            return render(request, 'arcoder/user_profile/solution/solution_form.html', params)


# Listing the user Programs
@login_required
def user_program(request, lang=None):
    temp_language = lang
    language = check_language(temp_language)

    if language != None:
        program = Program.objects.filter( author=request.user, title__language=language)
        
    else:
        program = Program.objects.filter(author=request.user)


    paginator = Paginator(program, no_of_blogs)
    page_number = request.GET.get('page')
    try:
        program_data = paginator.page(page_number)
    except PageNotAnInteger:
        program_data = paginator.page(1)
    except EmptyPage:
        program_data = paginator.page(paginator.num_pages)

    json_data = list()
    for obj in program_data:
        json_data.append({ 'fields' : obj.title_detail()})

    program_data_json = json.dumps(json_data)

    if language == None:
        lang_params = ''
    else:
        lang_params = language.name
    meta = Meta(
        title="ARCODERS PROGRAM:- " + request.user.username,
        description='ARCODERS PROGRAM:- Here you get the stuff related to programming and the latest technology',
        keywords=[request.user.username, 'ARCODERS', 'Profile', 'Programs'],
        extra_props={
            'viewport': 'width=device-width, initial-scale=1.0, minimum-scale=1.0'},
        extra_custom_props=[('http-equiv', 'Content-Type', 'text/html; charset=UTF-8'),
                            ])

    # return HttpResponse(test_data)
    params = {'cat': 'Program', 'data':program_data, 'json_data': program_data_json, 'meta': meta, 'language':lang_params, 'is_user_data':True,'title_prefix':'My'}
    return render(request, 'arcoder/user_profile/program/program.html', params)


# Listing the user query
@login_required
def user_query(request):
    if request.method == 'POST':
        temp_language = request.POST['language']
        if temp_language == 'all':
            query = Query.objects.filter(author=request.user)
            language = temp_language
        else:
            language = check_language(temp_language)
            if language is not None:
                query = Query.objects.filter(
                    author=request.user, language=language.name)
                language = temp_language
            else:
                query = Query.objects.filter(author=request.user)
                language = ''
    else:
        query = Query.objects.filter(author=request.user)
        language = ''

    paginator = Paginator(query, no_of_blogs)
    page_number = request.GET.get('page')
    try:
        query_data = paginator.page(page_number)
    except PageNotAnInteger:
        query_data = paginator.page(1)
    except EmptyPage:
        query_data = paginator.page(paginator.num_pages)


    meta = Meta(
        title="ARCODERS QUERYBOOK:- " + request.user.username,
        description='ARCODERS QUERYBOOK:- Here you get the stuff related to programming and the latest technology',
        keywords=[request.user.username, 'ARCODERS',
                  'Profile', 'Querybook', 'Query'],
        extra_props={
            'viewport': 'width=device-width, initial-scale=1.0, minimum-scale=1.0'},
        extra_custom_props=[('http-equiv', 'Content-Type', 'text/html; charset=UTF-8'),
                            ])

    params = {'cat': 'Query', 'data': query_data, 'meta': meta, 'language': language}
    # params = {'query_data': query_data,'language': language, 'all_languages': all_languages}
    return render(request, 'arcoder/user_profile/query/query.html', params)

# Listing the user solution
@login_required
def user_solution(request):
    if request.method == 'POST':
        temp_language = request.POST['language']
        if temp_language == 'all':
            solution = Solutions.objects.filter(author=request.user)
            language = temp_language
        else:
            language = check_language(temp_language)
            if language is not None:
                solution = Solutions.objects.filter(
                    author=request.user, query__language=language.name)
                language = temp_language
            else:
                solution = Solutions.objects.filter(author=request.user)
                language = ''
    else:
        solution = Solutions.objects.filter(author=request.user)
        language = ''

    paginator = Paginator(solution, no_of_blogs)
    page_number = request.GET.get('page')
    try:
        solution_data = paginator.page(page_number)
    except PageNotAnInteger:
        solution_data = paginator.page(1)
    except EmptyPage:
        solution_data = paginator.page(paginator.num_pages)

    # Handling like of solution
    for solution in solution_data:
        if solution.like.filter(id=request.user.id).exists():
            solution.liked = True
        else:
            solution.liked = False

    meta = Meta(
        title="ARCODERS QUERYBOOK:- " + request.user.username,
        description='ARCODERS QUERYBOOK:- Here you get the stuff related to programming and the latest technology',
        keywords=[request.user.username, 'ARCODERS',
                  'Profile', 'Querybook', 'Solution'],
        extra_props={
            'viewport': 'width=device-width, initial-scale=1.0, minimum-scale=1.0'},
        extra_custom_props=[('http-equiv', 'Content-Type', 'text/html; charset=UTF-8'),
                            ])
    params = {'cat': 'Query Solution', 'data': solution_data, 'meta': meta, 'language': language}
    # params = {'solution_data': solution_data, 'language': language, 'all_languages': all_languages}
    return render(request, 'arcoder/user_profile/solution/solution.html', params)


# To check avaibility of username while signing up
@csrf_exempt
def username(request):
    username = request.POST.get('username').lower()
    avaibile_obj = User.objects.filter(username=username).exists()
    if avaibile_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


# To handle other user profile
def other_profile(request, username):
    if request.user.username == username:
        return redirect('user')

    user_detail_obj = user_detail.objects.get(user__username=username)
    user_obj = User.objects.get(username=username)
    # adding the length of other data in user_obj
    user_obj.programs = len(Program.objects.filter(author=user_obj))
    user_obj.querys = len(Query.objects.filter(author=user_obj))
    user_obj.solutions = len(Solutions.objects.filter(author=user_obj))

    program_ratings = program_rating.objects.filter(user=user_obj)
    program_rating_data = dict()
    sum_program_rating = 0
    program_rating_count = 0
    for rating in program_ratings:
        program_rating_data[rating.program.id] = rating.rating
        sum_program_rating += rating.rating
        program_rating_count += 1
    if program_rating_count == 0:
        program_rating_count = 1

    solution_ratings = solution_rating.objects.filter(
        user=user_obj)
    solution_rating_data = dict()
    sum_query_rating = 0
    query_rating_count = 0
    for rating in solution_ratings:
        solution_rating_data[rating.solution.id] = rating.rating
        sum_query_rating += rating.rating
        query_rating_count += 1
    if query_rating_count == 0:
        query_rating_count = 1

    user_detail_obj.program_rating = round((sum_query_rating * 20)/query_rating_count, 2)
    user_detail_obj.solution_rating = round(
        (sum_program_rating * 20)/program_rating_count, 2)


    # handling the user privacy
    if user_detail_obj.privacy:
        user_obj.email = 'Privatized'

    meta = Meta(
        title="ARCODERS USERPROFILE:- @" + request.user.username,
        description='ARCODERS USERPROFILE:- Here you get the stuff related to programming and the latest technology',
        keywords=[request.user.username, 'ARCODERS', 'Profile'],
        extra_props={
            'viewport': 'width=device-width, initial-scale=1.0, minimum-scale=1.0'},
        extra_custom_props=[('http-equiv', 'Content-Type', 'text/html; charset=UTF-8'),
                            ])
    params = {'user_obj': user_obj, 'user_data': user_detail_obj}
    return render(request, 'arcoder/other_profile.html', params)




# Handle other user program data
def other_program(request, username, lang = None):
    user_obj = User.objects.get(username=username)
    temp_language = lang
    language = check_language(temp_language)

    if language != None:
        programs = Program.objects.filter(
                    author=user_obj, title__language=language)
    else:
        programs = Program.objects.filter(author=user_obj)

    paginator = Paginator(programs, no_of_blogs)
    page_number = request.GET.get('page')
    try:
        program_data = paginator.page(page_number)
    except PageNotAnInteger:
        program_data = paginator.page(1)
    except EmptyPage:
        program_data = paginator.page(paginator.num_pages)

    json_data = list()
    for obj in program_data:
        json_data.append({ 'fields' : obj.title_detail()})

    program_data_json = json.dumps(json_data)

    if language == None:
        lang_params = ''
    else:
        lang_params = language.name
    params = {'cat':'Program', 'data':program_data, 'json_data':program_data_json, 'language':lang_params, 'user_obj': user_obj, 'title_prefix':user_obj.username}
    return render(request, 'arcoder/other_profile/program/program.html', params)


# Handle other user query data
def other_query(request, username):
    user_obj = User.objects.get(username=username)
    if request.method == 'POST':
        temp_language = request.POST['language']
        if temp_language == 'all':
            querys = Query.objects.filter(author=user_obj)
            language = temp_language
        else:
            language = check_language(temp_language)
            if language is not None:
                querys = Query.objects.filter(
                    author=user_obj, language=language.name)
                language = temp_language
            else:
                querys = Query.objects.filter(author=user_obj)
                language = ''
    else:
        querys = Query.objects.filter(author=user_obj)
        language = ''

    paginator = Paginator(querys, no_of_blogs)
    page_number = request.GET.get('page')
    try:
        query_data = paginator.page(page_number)
    except PageNotAnInteger:
        query_data = paginator.page(1)
    except EmptyPage:
        query_data = paginator.page(paginator.num_pages)

    params = {'cat': 'Query', 'data': query_data, 'language': language, 'user_obj':user_obj}
    # params = {'solution_data': solution_data, 'languages': all_languages, 'language_data': language}
    return render(request, 'arcoder/other_profile/query/query.html', params)


# Handle other user solution data
def other_solution(request, username):
    user_obj = User.objects.get(username=username)
    if request.method == 'POST':
        temp_language = request.POST['language']
        if temp_language == 'all':
            solutions = Solutions.objects.filter(author=user_obj)
            language = temp_language
        else:
            language = check_language(temp_language)
            if language is not None:
                solutions = Solutions.objects.filter(
                    author=user_obj, query__language=language.name)
                language = temp_language
            else:
                solutions = Solutions.objects.filter(author=user_obj)
                language = ''
    else:
        solutions = Solutions.objects.filter(author=user_obj)
        language = ''

    paginator = Paginator(solutions, no_of_blogs)
    page_number = request.GET.get('page_number')
    try:
        solution_data = paginator.page(page_number)
    except PageNotAnInteger:
        solution_data = paginator.page(1)
    except EmptyPage:
        solution_data = paginator.page(paginator.num_pages)

    for solution in solution_data:
        if solution.like.filter(id=request.user.id).exists():
            solution.liked = True
        else:
            solution.liked = False

    params = {'cat': 'Query Solution', 'data': solution_data, 'language': language, 'user_obj': user_obj}
    # params = {'solution_data': solution_data, 'languages': all_languages, 'language_data': language}
    return render(request, 'arcoder/other_profile/solution/solution.html', params)







########################
### REMOVE FUNCTIONS ###
########################    


# remove program
@login_required()
def remove_program(request, program_id):

    # for security check
    program = Program.objects.get(id = program_id)
    if request.user != program.author or program is None:
        messages.error(request, 'Something went wrong!!!')
        return redirect('user_program')

    title = program_title.objects.get(id = program.title.id)    
    
    # handle the program caching 
    program_key = 'program/' + str(title.slug) + '/'
    program_cache_value = caches['program'].get(program_key)

    program_id = int(program.id)

    if program_cache_value is not None:
        # updating program cache value
        if program_id in program_cache_value['programs']['id']:
            index = program_cache_value['programs']['id'].index(program_id)
        
            temp_cache_value = program_cache_value
            caches['program'].delete(program_key)
            temp_cache_value['answer_count'] -= 1
            temp_cache_value['programs']['id'].pop(index)
            temp_cache_value['programs']['code'].pop(index)
            temp_cache_value['programs']['author'].pop(index)
            temp_cache_value['programs']['time_stamp'].pop(index)
            temp_cache_value['programs']['total_rating'].pop(index)
            temp_cache_value['programs']['like_count'].pop(index)
            caches['program'].set(program_key, temp_cache_value, 10*60)



    program.delete()
    title.answers -= 1
    title.save()


    messages.error(request, 'Program Get Removed Sucessfully!!!')
    return redirect('user_program')



# removing the query
@login_required()
def remove_query(request, query_id):

    # for security check
    query = Query.objects.get(id = query_id)
    if request.user != query.author or query is None:
        messages.error(request, 'Something went wrong!!!')
        return redirect('user_query')
    
    if Solutions.objects.filter(query=query).exists():
        messages.error(request, 'Sorry, The solution of this query is given by someone. So,it cannot get removed now!')
        return redirect('user_query')

    # handling the caching
    query_key = 'query/' + str(query.slug) + '/'
    query_cache_value = caches['query'].get(query_key)

    caches['query'].delete(query_key)

    query.delete()
    messages.error(request, 'Query Get Successfully Removed!!!')
    return redirect('user_query')



# removing the solution
@login_required()
def remove_solution(request, solution_id):

    # security check
    solution = Solutions.objects.get(id = solution_id)
    if request.user != solution.author or solution is None:
        messages.error(request, 'Something went wrong!!!')
        return redirect('user_solution')

    query = Query.objects.get(id = solution.query.id)

    # handle caching
    query_key = 'query/' + str(query.slug) + '/'
    query_cache_value = caches['query'].get(query_key)

    solution_id = int(solution.id)

    if query_cache_value is not None:
        # updating program cache value
        if solution_id in query_cache_value['solutions']['id']:
            index = query_cache_value['solutions']['id'].index(solution_id)
    
        temp_cache_value = query_cache_value
        caches['query'].delete(query_key)
        temp_cache_value['answer_count'] -= 1
        temp_cache_value['solutions']['id'].pop(index)
        temp_cache_value['solutions']['solution'].pop(index)
        temp_cache_value['solutions']['author'].pop(index)
        temp_cache_value['solutions']['time_stamp'].pop(index)
        temp_cache_value['solutions']['total_rating'].pop(index)
        temp_cache_value['solutions']['like_count'].pop(index)
        caches['query'].set(query_key, temp_cache_value, 10*60)



    query.answer -= 1
    query.save()
    solution.delete()
    messages.error(request, 'Solution Get Removed Successfully!!!')
    return redirect('user_solution')


