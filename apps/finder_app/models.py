# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import bcrypt, re, datetime
from datetime import timedelta
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

# Create your models here.
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class dbManager(models.Manager):
    def regValidation(self, postData, filesData):
        response = {
            'status': True,
        }
        dob_checker = datetime.datetime.today().strftime('%Y-%m-%d')
        # WE NEED TO CHANGE THE YEAR +10
        errors = []
        if len(postData['first']) < 1 or len(postData['last']) < 1 or len(postData['username']) < 1 or len(postData['email']) < 1 or len(postData['phonenum']) < 1 or len(postData['password']) < 1 or len(postData['dob'])<1:
        	errors.append('Please fill all requried fields!')
        if not EMAIL_REGEX.match(postData['email']):
        	errors.append('Invalid Email')
        if postData['password'] != postData['confirm']:
        	errors.append('Passwords did not match!')
        if postData['dob']>dob_checker:
                errors.append("You should be at least 10 years old")
        if len(postData['password']) < 8:
        	errors.append('Weak password, try 8 or more characters!')
        email = User.objects.filter(email=postData['email'])
        if len(email) > 0:
        	errors.append("Email already taken")
        username = User.objects.filter(username=postData['username'])
        if len(username) > 0:
        	errors.append("Username already taken")
        if len(errors) > 0:
        	response['status'] = False
        	response['errors'] = errors
        else: 
        	PW = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
        	response['user'] = User.objects.create(first_name=postData['first'], last_name=postData['last'], username=postData['username'], password=PW, email=postData['email'], phonenumber=postData['phonenum'], dob=postData['dob'], photo=filesData['image'])
        return response

    def loginValidation(self, postData):
    	response = {
        	'status': False,
    	}
    	errors = []
    	users = User.objects.filter(username=postData['logusername'])
    	if len(users) < 1:
    		errors.append('Incorrect Email/Password, Try again')
    		response['errors'] = errors
    		return response
    	PW = bcrypt.checkpw(postData['logpassword'].encode(), users[0].password.encode())
    	if PW == True:
    		response['status'] = True
    		response['user'] = users[0]
    	else: 
    		errors.append('Incorrect Email/Password, Try again')
    		response['errors'] = errors
    	return response
        
    def activityValidation(self,postData):
        response = {
            'status': True
        }
        errors = []
        if len(postData['desc']) == 0:
            errors.append("Fill out description so people know what you are doing")
        if len(postData['newCategory']) == 0:
            categoryInput = Category.objects.get(id=postData['categoryId'])
        else:
            existing = Category.objects.filter(name=postData['newCategory'])
            if len(existing) > 0:
                response['status'] = False
                errors.append("This category exists already")
            else:
                categoryInput = Category.objects.create(name=postData['newCategory'])
        if len(errors) == 0:
            HOURS = str(postData['duration'])[:2]
            MINUTES = str(postData['duration'])[-2:]
            endtime = datetime.datetime.now() + timedelta(hours=int(HOURS)) + timedelta(minutes=int(MINUTES))
            created_at = datetime.datetime.now()
            updated_at = datetime.datetime.now()
            response['activity'] = Activity.objects.create(category=categoryInput,desc=postData['desc'],lat=postData['actLat'],lng=postData['actLng'],where=postData['where'],endtime=endtime,created_by=User.objects.get(id=postData['activeUser']),created_at=created_at, updated_at=updated_at, max_users=int(postData['max_users']))
        response['errors'] = errors
        return response		

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    photo = ProcessedImageField(upload_to="media",
                                processors=[ResizeToFill(200, 200)],
                                format='JPEG',
                                options={'quality': 60})
    phonenumber = models.IntegerField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = dbManager()
    dob = models.DateField()

class Category(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Activity(models.Model):
    lat = models.CharField(max_length=255)
    lng = models.CharField(max_length=255)
    desc = models.TextField()
    where = models.CharField(max_length=255)
    endtime = models.DateTimeField()
    max_users = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    category = models.ForeignKey(Category, related_name="activities")
    created_by = models.OneToOneField(User, related_name="created_activity")
    joined_users = models.ManyToManyField(User, related_name="joined_activities")
    objects = dbManager()

class Review(models.Model):
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    written_for = models.ManyToManyField(User, related_name="written_by")

