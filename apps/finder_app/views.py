from __future__ import unicode_literals, division

from django.shortcuts import render, redirect, HttpResponse
from .models import *
import math
from django.contrib import messages
from django.core import serializers


# Create your views here.

def index(request):
	return render(request, 'finder_app/index.html')

def dash(request): 
	# Eric
	activeuser = User.objects.get(id=request.session['user_id'])
	allmsg = ''
	otheruser = ''
	msgcheck = False
	if 'writeTo' in request.session:
		otheruser = User.objects.get(id=request.session['writeTo'])
		allmsg = Message.objects.filter(written_by=activeuser).filter(written_for=otheruser).order_by('created_at') | Message.objects.filter(written_for=activeuser).filter(written_by=otheruser).order_by('created_at')
		msgcheck = True
	groupedmsg = Message.objects.raw('SELECT * FROM finder_app_message WHERE written_for_id ={} GROUP BY written_by_id'.format(activeuser.id))
	# END
	dashReviews = Review.objects.filter(written_for=request.session['user_id'])
	dashRating = 0
	if (len(dashReviews)):
		for eachDashReview in dashReviews:
			dashRating += eachDashReview.rating
		dashRating = round(dashRating/len(dashReviews), 1)

	if "searchID" in request.session:
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
		join_messages = []
		message_links = []

		categoryid = Category.objects.get(id=request.session["searchID"])
		activities = Activity.objects.filter(category = categoryid)

		for each in activities:
			lat.append(each.lat)
			lng.append(each.lng)
			pictures.append(each.created_by.photo.url)
			reviews = Review.objects.filter(written_for=each.created_by.id)
			rating = 0
			if (len(reviews)):
				for eachReview in reviews:
					rating += eachReview.rating
				rating = rating/len(reviews)
			ratings.append(round(rating, 1))
			rating_links.append('view_review/{}'.format(each.created_by.id))
			names.append('{} {}'.format(each.created_by.first_name, each.created_by.last_name))
			usernames.append(each.created_by.username)
			categories.append(each.category.name)
			descriptions.append(each.desc)
			wheres.append(each.where)
			starts.append(each.created_at.strftime('%I:%M%p %m/%d'))
			ends.append(each.endtime.strftime('%I:%M%p %m/%d'))
			joineds.append(len(each.joined_users.all()))
			max_users.append(each.max_users)
			if User.objects.get(id=request.session['user_id']) in each.joined_users.all():
				join_links.append('leave_activity/{}'.format(each.id))
				join_messages.append('You have already joined. Leave?')
			elif request.session['user_id'] == each.created_by.id:
				join_links.append('delete_activity/{}'.format(each.id))
				join_messages.append('You have created this event. Delete?')
			else:
				join_links.append('join_activity/{}'.format(each.id))
				join_messages.append('Would you like to join?')
			message_links.append('write_message/{}'.format(each.created_by.id))
		
		if "view_review_id" in request.session:
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
				'join_messages': ",".join(str(x) for x in join_messages),
				'message_links': ",".join(str(x) for x in message_links),
				'categories': Category.objects.all(),
				'dashrating': dashRating,
				'reviews': User.objects.get(id=request.session['view_review_id']).has_reviews.all(),
				#---------------------------------------------------------
				'user': activeuser,
				'allmsg': allmsg, 
				'otheruser': otheruser,
				'groupedmsg': groupedmsg,
				'msgcheck': msgcheck
				#------------------------------------------------------
			}
				
		else:	
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
				'join_messages': ",".join(str(x) for x in join_messages),
				'message_links': ",".join(str(x) for x in message_links),
				'categories': Category.objects.all(),
				'dashrating': dashRating,
				#---------------------------------------------------------
				'user': activeuser,
				'allmsg': allmsg, 
				'otheruser': otheruser,
				'groupedmsg': groupedmsg,
				'msgcheck': msgcheck
				#------------------------------------------------------
			}
		return render(request, 'finder_app/map.html', context)
	else:
		context = {
			'categories': Category.objects.all(),
			'dashrating': dashRating,	
			#---------------------------------------------------------
			'user': activeuser,
			'allmsg': allmsg, 
			'otheruser': otheruser,
			'groupedmsg': groupedmsg,
			'msgcheck': msgcheck
			#------------------------------------------------------	
		}
		return render(request, 'finder_app/map.html', context)

def process(request):
	result = User.objects.regValidation(request.POST, request.FILES)
	request.session['lat'] = request.POST['lat']
	request.session['lng'] = request.POST['lng']
	if result['status']:
		request.session['user_id'] = result['user'].id
	else: 
		for error in result['errors']:
			messages.error(request, error)
		return redirect('/')
	return redirect('/main')

def login(request):
	result = User.objects.loginValidation(request.POST)
	request.session['lat'] = request.POST['lat']
	request.session['lng'] = request.POST['lng']
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
		request.session['searchID'] = response['activity'].category.id
		request.session['lat'] = response['activity'].lat
		request.session['lng'] = response['activity'].lng
		return redirect('/main')
	else:
		for error in response['errors']:
			messages.error(request, error)
		return redirect('/main')

def searchActivity(request):
	request.session['searchID'] = request.POST['categoryId']
	return redirect('/main')

def clearSearch(request):
	del request.session['searchID']
	return redirect('/main')

def joinActivity(request, number):
	User.objects.get(id=request.session['user_id']).joined_activities.add(Activity.objects.get(id=number))
	return redirect('/main')

def leaveActivity(request, number):
	Activity.objects.get(id=number).joined_users.remove(User.objects.get(id=request.session['user_id']))
	return redirect('/main')

def deleteActivity(request, number):
	if request.session['user_id'] == Activity.objects.get(id=number).created_by.id:
		Activity.objects.get(id=number).delete()
	return redirect('/main')

def leaveReview(request, number):
	if request.method == "POST":
		del request.session['view_review_id']
		newReview = Review.objects.create(rating=int(request.POST['rating']),comment=request.POST['comment'],written_by=User.objects.get(id=request.session['user_id']))
		newReview.written_for.add(User.objects.get(id=number))
		newReview.save()
	return redirect('/main')

def viewReview(request, number):
	request.session['view_review_id'] = number
	return redirect('/main')

def exitReview(request):
	del request.session['view_review_id']
	return redirect('/main')
#--------------------------------------------------------------------------------------
def messagesid(request, number):
	request.session['writeTo'] = number
	return redirect('/main')

def closeMessages(request):
	del request.session['writeTo']
	return redirect('/main')

def processMessage(request):
	activeuser = User.objects.get(id=request.session['user_id'])
	otheruser = User.objects.get(id=request.session['writeTo'])
	Message.objects.create(message=request.POST['message'], written_by=activeuser, written_for=otheruser, created_at=datetime.datetime.now(), updated_at=datetime.datetime.now())
	return redirect('/main')
#----------------------------------------------------------------------------------------
