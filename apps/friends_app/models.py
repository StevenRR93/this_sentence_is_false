# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

import datetime
import re

class UsersManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        #print(Users.objects.filter(email = postData['email']).exists())
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should have more than 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should have more than 2 characters"
        if len(postData['password']) < 8:
            errors['password'] = "Password should be more than 8 characters"
        if (not re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', postData['email'])):
            errors['email'] = "E-mail address should be a valid e-mail address"
        if (Users.objects.filter(email = postData['email']).exists()):
            errors['email'] = "E-mail address already used"
        if len(postData['alias']) < 2:
            errors["alias"] = "Alias should have more than 2 characters"
        if (Users.objects.filter(alias = postData['alias']).exists()):
            errors['alias'] = "Alias already used"
        if postData['birthday'] == None:
            errors['birtday'] = "Date of birth is not valid"
        return errors

class FriendManager(models.Manager):
    def basic_validator(self, id1, id2):
        errors = {}
        if (id1 == id2):
            errors["friend1_id"] = "You cannot add yourself"
        elif (Friendship.objects.filter(friend1_id = int(id1), friend2_id = int(id2)).exists()):
            errors["friend1_id"] = "You are already friends"
        return errors

class Users(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    alias = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    def __repr__(self):
        return "<Users object: {} {} {} {} {}>".format(self.id, self.first_name, self.last_name, self.email, self. alias)
    # *************************
    # Connect an instance of UsersManager to our Users model overwriting
    # the old hidden objects key with a new one with extra properties!!!
    objects = UsersManager()
    # *************************

class Friendship(models.Model):
    friend1 = models.ForeignKey(Users, on_delete=models.CASCADE, related_name= "friend1")
    friend2 = models.ForeignKey(Users, on_delete=models.CASCADE, related_name= "friend2")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    def __repr__(self):
        return "<Friendship object: {} {}>".format(self.friend1.id, self.friend2.id) #, self.user
    # *************************
    # Connect an instance of UsersManager to our Users model overwriting
    # the old hidden objects key with a new one with extra properties!!!
    objects = FriendManager()
    # *************************

