from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
from django.shortcuts import render, redirect
import bcrypt
import re
import datetime
import time

class UserManager(models.Manager):
	def reg_check(self, postData):


		name_match = r'^[a-zA-Z]+$'	
		# accepts only alpha characters in a name

		pass_require = r'(?=.*[A-Z]+)(?=.*[0-9]+)'
		# password requires at least one upper case letter and one number

		iso_hiredate_match = r'^(19|20)\d{2}\-(0[1-9]|1[0-2])\-(0[1-9]|1\d|2\d|3[01])$'

		alt_hiredate_match = r'^(0[1-9]|1[0-2])\/(0[1-9]|1\d|2\d|3[01])\/(19|20)\d{2}$'

		iso_current_date = (time.strftime("%Y-%m-%d"))

		hiredate = postData['hiredate']

		error_messages = []

		if len(postData['name']) < 3:
			error_messages.append('Name must contain at least 3 characters!')
			
		if not re.search(name_match, postData['name']):
			error_messages.append('Name must have only letters!')
			
		if len(postData['username']) < 3:
			error_messages.append('Username must contain at least 3 characters!')
			
		if not postData['password']:
			error_messages.append("Password cannot be blank! Password must be at least 8 characters and contain at least 1 capital letter and 1 number!")
		
		else:	
			if len(postData['password']) < 8:
				error_messages.append("Password cannot be less than 8 characters!")
				
			if not re.search(pass_require, postData['password']):
				error_messages.append("Password must contain at least 1 capital letter and 1 number!")
				
		if postData['confirm_password'] != postData['password']:
			error_messages.append("Confirm password and password must match!")

		if not postData['hiredate']:
			error_messages.append("Hire date must be entered!")

		if re.search(iso_hiredate_match, postData['hiredate']):	

			if postData['hiredate'] > iso_current_date:
				error_messages.append("Hire date cannot be after today's date!")
			
		elif re.search(alt_hiredate_match, postData['hiredate']):	

			hiredate = datetime.date(int(hiredate[6:]), int(hiredate[:2]), int(hiredate[3:-5])).isoformat()
			if hiredate > iso_current_date:
				error_messages.append("Hire date cannot be after today's date!")

		else:
			error_messages.append("Hire date must be entered in format of MM/DD/YYYY!")	
					
		response = {}				

		if error_messages:
			response['errors'] = error_messages
			response['created'] = False

		else:
			pw_hash = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
			new_user = self.create(name=postData['name'],username=postData['username'],hiredate=postData['hiredate'],pw_hash=pw_hash)
			response['created'] = True
			response['new_user'] = new_user

		return response

	def login_check(self, postData):

		error_messages = []
		username_check = User.objects.filter(username=postData['username'])
		response = {}

		if not username_check:
			error_messages.append("username does not exist in system! Please register!")
			response['login'] = False
		else:
			if bcrypt.hashpw(postData['password'].encode(), username_check[0].pw_hash.encode()) == username_check[0].pw_hash:
				response['login'] = True
				response['user'] = username_check[0]
			else:	
				error_messages.append("Password is invalid!")
				response['login'] = False

		response['errors'] = error_messages

		return response	
						
class User(models.Model):
	name=models.CharField(max_length=100)
	username=models.CharField(max_length=100)
	hiredate = models.CharField(max_length=10)
	pw_hash=models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add = True)
	objects = UserManager()
