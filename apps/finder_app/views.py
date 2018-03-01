from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages
from django.core import serializers
# Create your views here.

def index(request):
	return render(request, 'finder_app/index.html')

def success(request):
	if 'user_id' not in request.session:
		return redirect('/')
	activeuser = User.objects.get(id=request.session['user_id'])
	welcome = activeuser.username
	context = {
	'active': welcome
	}
	return render(request, 'finder_app/success.html', context)

def dash(request):
    context = {
		'categories': Category.objects.all(),
        'user': User.objects.get(id=request.session['user_id'])
	}
    return render(request, 'finder_app/map.html', context)

def process(request):
	result = User.objects.regValidation(request.POST, request.FILES)
	if result['status']:
		request.session['user_id'] = result['user'].id
	else: 
		for error in result['errors']:
			messages.error(request, error)
		return redirect('/')
	return redirect('/main')

def login(request):
	result = User.objects.loginValidation(request.POST)
	if result['status'] == False:
		for error in result['errors']:
			messages.warning(request, error)
		return redirect('/')
	request.session['user_id'] = result['user'].id
	return redirect('/main')

def logout(request):
	request.session.clear()
	return redirect('/')

def display_user(request):
	users = User.objects.get(id=1)
	user1 = users.username
	print user1
	return HttpResponse(user1)

def addActivity(request):
	response = Activity.objects.activityValidation(request.POST)
	if response['status']:
		return redirect('/main')
	else:
		for error in response['errors']:
			messages.error(request, error)
		return redirect('/main')

def searchActivity(request):
	search = {
		"category": request.POST['categoryId'],
		"lat": request.POST['Lat'],
		"lng": request.POST['Lng']
	}
	searchCategory = Category.objects.get(id=search['category'])
	searchResults = Activity.objects.filter(category=searchCategory)
	print search
	print searchResults
	return redirect('/activity')