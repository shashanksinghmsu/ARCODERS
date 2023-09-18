from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate
from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from arcoder.models import Language, user_detail
from arcoder.views import user
from django.views.decorators.csrf import csrf_exempt

 
# for cache 
from django.core.cache import cache, caches
from cache_key_generator import get_cache_key



# this function take the next url and replace the 'c  ' in c++


def cpp_checker(url):
    url = url.replace('C  ', 'C++')
    return url


################
# my functions #
################
def check_user_account(request):
	if not request.user.is_authenticated:
		messages.error(request, 'Something Gone Wrong!')
		return redirect(user)


##########################
# Create your views here.#
##########################

@login_required()
def update_username(request):
	if request.method == 'POST':
		new_username = request.POST['username'].lower()
		if User.objects.filter(username=new_username).exists():
			messages.error(request, 'Oups! Username is Not Available.')
		else:
			old_username = request.user.username
			obj = User.objects.get(username=old_username)
			obj.username = new_username
			obj.save()

			# updating the cache data
			user_key = 'user/' + str(old_username) + '/'
			user_cache_value = caches['user'].get(user_key)
			if user_cache_value is not None:
				cache_value = user_cache_value
				caches['user'].delete(user_key)
				cache_value['user']['username'] = new_username
				updated_user_key = 'user/' + str(new_username) + '/'
				caches['user'].set(updated_user_key, cache_value, 10*60)
				
			messages.error(request, 'Username Changed Successfully.')
	return redirect(user)



@csrf_exempt
def username_check(request):
	check_user_account(request)
	username = request.POST.get('username').lower()
	obj = User.objects.filter(username=username).exists()
	if obj:
		return HttpResponse(True)
	else:
		return HttpResponse(False)



@login_required()
def email(request):
	if request.method == 'POST':
		new_email = request.POST['email']
		if User.objects.filter(email=new_email).exists():
			messages.error(request, 'Email Already Exists!')
		else:
			old_mail = request.user.email
			obj = User.objects.get(username=request.user.username)
			obj.email = new_email
			obj.save()

            # updating the cache data
			user_key = 'user/' + str(request.user.username) + '/'
			user_cache_value = caches['user'].get(user_key)
			if user_cache_value is not None:
				cache_value = user_cache_value
				caches['user'].delete(user_key)
				cache_value['user']['email'] = new_email
				caches['user'].set(user_key, cache_value, 10*60)

			messages.error(request, 'Email Updated Successfully!')
	return redirect(user)



@login_required()
def name(request):
	if request.method == 'POST':
		new_name = request.POST['name']
		name_lst = new_name.split(' ')
		if len(name_lst) > 1:
			last_name = name_lst[-1]
			name_lst.pop()
			first_name = ' '.join(name_lst)
			change = True
		elif len(name_lst) > 0:
			first_name = new_name
			last_name = ' '
			change = True
		else:
			messages.error(request, 'Invalid Credential')
			change = False

		if change:
			obj = User.objects.get(username=request.user.username)
			obj.first_name = first_name
			obj.last_name = last_name
			obj.save()

            # updating the cache data
			user_key = 'user/' + str(request.user.username) + '/'
			user_cache_value = caches['user'].get(user_key)
			if user_cache_value is not None:
				cache_value = user_cache_value
				caches['user'].delete(user_key)
				cache_value['user']['first_name'] = first_name
				cache_value['user']['last_name'] = last_name
				caches['user'].set(user_key, cache_value, 10*60)

			messages.error(request, 'Name Updated Successfully!')
		return redirect(user)


def dob(request):
	check_user_account(request)
	if request.method == 'POST':
		dob = request.POST['dob']
		obj = user_detail(user = request.user)
		obj.dob = dob
		obj.save()

		# updating the cache data
		user_key = 'user/' + str(request.user.username) + '/'
		user_cache_value = caches['user'].get(user_key)
		if user_cache_value is not None:
			cache_value = user_cache_value
			caches['user'].delete(user_key)
			cache_value['user_data']['dob'] = dob
			caches['user'].set(user_key, cache_value, 10*60)

		messages.error(request, 'DOB Updated Successfully!')
	return redirect(user)


def gender(request):
	check_user_account(request)
	if request.method == 'POST':
		gender = request.POST['gender']
		obj = user_detail(user = request.user)
		obj.gender = gender
		obj.save()

		# updating the cache data
		user_key = 'user/' + str(request.user.username) + '/'
		user_cache_value = caches['user'].get(user_key)
		if user_cache_value is not None:
			cache_value = user_cache_value
			caches['user'].delete(user_key)
			cache_value['user_data']['gender'] = gender
			caches['user'].set(user_key, cache_value, 10*60)

		messages.error(request, 'Gender Updated Successfully!')
	return redirect(user)


def phone(request):
	check_user_account(request)
	if request.method == 'POST':
		new_phone = request.POST['phone']
		if user_detail.objects.filter(phone=phone).exists():
			messages.error(request, 'Phone Number Already Exists!')
		else:
			user_obj = User.objects.get(username=request.user.username)
			obj = user_detail(user=user_obj)
			obj.phone = new_phone
			obj.save()
			messages.error(request, 'Phone Number Updated Successfully!')
	return redirect(user)


def about(request):
	check_user_account(request)
	if request.method == 'POST':
		about = request.POST['about']
		obj = user_detail(user = request.user)
		obj.about = about
		obj.save()

		# updating the cache data
		user_key = 'user/' + str(request.user.username) + '/'
		user_cache_value = caches['user'].get(user_key)
		if user_cache_value is not None:
			cache_value = user_cache_value
			caches['user'].delete(user_key)
			cache_value['user_data']['about'] = about
			caches['user'].set(user_key, cache_value, 10*60)

		messages.error(request, 'About Section Updated Successfully!')
	return redirect(user)
