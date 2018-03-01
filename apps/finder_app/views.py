from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from .models import *
import math
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
	lat = []
	lng = []
	pictures = []
	ratings = []
	rating_links = []
	names = []
	usernames = []
	categories = []
	descriptions = []
	wheres = []
	starts = []
	ends = []
	joineds = []
	max_users = []
	join_links = []
	leave_links = []
	message_links = [] 

	activities = Activity.objects.all()

	for each in activities:
		lat.append(each.lat)
		lng.append(each.lng)
		pictures.append(each.created_by.photo.url)
		reviews = Review.objects.filter(written_for=each.created_by.id)
		rating = 0
		if (len(reviews)):
			for each in reviews:
				rating += each.rating
			rating = rating/len(reviews)
		ratings.append(round(rating, 1))
		rating_links.append('leave_review/{}'.format(each.created_by.id))
		names.append('{} {}'.format(each.created_by.first_name, each.created_by.last_name))
		usernames.append(each.created_by.username)
		categories.append(each.category.name)
		descriptions.append(each.desc)
		wheres.append(each.where)
		starts.append(each.created_at.strftime('%I:%M%p %m/%d'))
		ends.append(each.endtime.strftime('%I:%M%p %m/%d'))
		joineds.append(len(each.joined_users.all()))
		max_users.append(each.max_users)
		join_links.append('join_activity/{}'.format(each.id))
		leave_links.append('leave_activity/{}'.format(each.id))
		message_links.append('write_message/{}'.format(each.created_by.id))
		
	context = {
		'lat': ",".join(str(x) for x in lat),
		'lng': ",".join(str(x) for x in lng),
	    'pictures': ",".join(str(x) for x in pictures),
		'rating': ratings,
		'rating_links': ",".join(str(x) for x in rating_links),
		'names': ",".join(str(x) for x in names),
		'usernames': ",".join(str(x) for x in usernames),
		'category_names': ",".join(str(x) for x in categories),
		'descriptions': ",".join(str(x) for x in descriptions),
		'wheres': ",".join(str(x) for x in wheres),
		'starts': ",".join(str(x) for x in starts),
		'ends': ",".join(str(x) for x in ends),
		'joineds': ",".join(str(x) for x in joineds),
		'max_users': ",".join(str(x) for x in max_users),
		'join_links': ",".join(str(x) for x in join_links),
		'leave_links': ",".join(str(x) for x in leave_links),
		'message_links': ",".join(str(x) for x in message_links),
		'categories': Category.objects.all(),
		'user': User.objects.get(id=request.session['user_id']),
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