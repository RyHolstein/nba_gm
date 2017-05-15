from __future__ import unicode_literals
from django.db import models


import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class UserManager(models.Manager):
    #-----------------registerAccount-----------------#
    def register_account(self, data):
        errors = [] #collects the errors from the form validation
        #-----------------username-----------------#
        if data['username'] == '':
            errors.append("username must not be Blank")
        elif len(data['username']) < 5:
            errors.append('The First Name field must be longer than 5 characters!')
        try: #check to see if the username is already being Used
            User.objects.get(username = data['username'])
            errors.append('Username is already being used')
        except:
            pass
        #-----------------email-----------------#
        if data['email'] == '':
            errors.append("email must not be Blank")
        if not EMAIL_REGEX.match(data['email']):
            errors.append('Email Must be Correct Format')

        try:
            User.objects.get(email = data['email'])
            errors.append('email is already being used')
        except:
            pass
        #-----------------password-----------------#
        if data['password'] == '':
            errors.append('Password cannot be blank!')
        elif len(data['password']) < 6:
            errors.append('Password must be at least 6 characters long!')

        if not data['password'] == data['confirm_password']:
            errors.append('password fields have to match')
        print errors


        #-----------------validations complete-----------------#
        if len(errors) == 0: #if there are no errors then add the user to the database
            hashed = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()) #need to encrypt the password for security purposes
            user = User.objects.create(username=data['username'], email=data['email'], password=hashed)

            return {'user': user, 'errors': None}
        else:
            #return the errors that we received
            return {'user': None, 'errors': errors}

#-----------------Login-----------------#
    def login_account(self, data):
        errors = []
        try:
            User.objects.get(username=data['username'])
            print 'same user'
            #email is already registered
        except:
            #email is NOT already registered
            print 'different user'
            errors.append('Username is incorrect')
            return {'user': None, 'errors':errors }

        #check if the password is correct
        if User.objects.get(username=data['username']).password.encode('utf-8') == bcrypt.hashpw(data['password'].encode('utf-8'), User.objects.get(username=data['username']).password.encode('utf-8')):
            user = User.objects.get(username=data['username'])
            print 'same pass'
            return {'user':user, 'errors': None}
        else:
            print 'different pass'
            errors.append('Pass is incorrect')
            return {'user': None, 'errors':errors }


# ---------------------Tables--------------------- #

#here is the table for User
class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
