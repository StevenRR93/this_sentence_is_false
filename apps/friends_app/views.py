# -*- coding: utf-8 -*-
#Steven Ramirez
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect

from .models import Users
from .models import Friendship
from django.contrib import messages
from django.contrib.messages import error
import time
import bcrypt

def main(request):
    is_signed_in = request.session.get('is_signed_in', False)
    if (is_signed_in == True):
        return redirect('/friends')
    return render(request, 'main.html')

def login(request):
    if (request.method == "POST"):
        try:
            user = Users.objects.get(email = request.POST['email'])
            if (bcrypt.checkpw(request.POST['password'].encode('utf8'), user.password.encode('utf8'))):
                request.session['first_name'] = user.first_name
                request.session['last_name'] = user.last_name
                request.session['alias'] = user.alias
                request.session['email'] = request.POST['email']
                request.session['id'] = user.id
                request.session['is_signed_in'] = True
                return redirect('/friends')
            else: 
                messages.error(request, 'Incorrect password.')
                return redirect('/main')
        except:
            messages.error(request, 'E-mail address not found, please enter a valid e-mail.')
            return redirect('/main')
    else:
        return redirect('/main')
    
def register(request):
    if (request.method == "POST"):
        errors = Users.objects.basic_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/main')
        elif (request.POST['password'] == request.POST['confirmpw']):
            errors = Users.objects.basic_validator(request.POST)
            salt = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            user = Users.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = salt, alias = request.POST['alias'])
            user.save()
            return redirect('register/'+str(user.id))
        else:
            return redirect('/main')
    else:
        return redirect('/main')

def success_reg(request, idnum):
    user = Users.objects.get(id = idnum)
    return render(request, 'register.html', {'user': user})

def friends(request):
    if request.session['is_signed_in'] == False:
        return redirect('/main')
    user = Users.objects.get(id = request.session['id'])
    try:                                                                                                                                
        myfriends = Friendship.objects.filter(friend1_id = user.id )
        if not myfriends.exists():
            myfriends = None
    except:
        myfriends = None
    flist = Friendship.objects.filter(friend1_id = user.id ).values("friend2_id").distinct()
    other_users = Users.objects.exclude(id = request.session['id'] )
    for i in flist:
        other_users = other_users.exclude(id = int(i['friend2_id']))
    try:                                                                                                               
        a = 1
        
        if not other_users.exists():
            other_users = None
    except:
        other_users = None
    #print("myfriends", myfriends)
    #print("others", other_users)
    #print(Friendship.objects.filter(friend1_id = user.id))
    return render(request, 'friends.html', {'myfriends' : myfriends, 'other_users' : other_users} )


def signout(request):
    if request.session['is_signed_in'] == False:
        return redirect('/main')
    request.session['first_name'] = None
    request.session['last_name'] = None
    request.session['email'] = None
    request.session['id'] = None
    request.session['is_signed_in'] = False
    return redirect('/main')

def add(request, idnum):
    if request.session['is_signed_in'] == False:
        return redirect('/main')
    errors = Friendship.objects.basic_validator(request.session["id"], idnum)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/main')
    try: 
        Users.objects.get(id = idnum)
        Friendship.objects.create(friend1_id = request.session['id'], friend2_id = idnum)
        Friendship.objects.create(friend2_id = request.session['id'], friend1_id = idnum)
    except:
        messages.error(request, "Unable to add friend :(")
        return redirect('/friends')
    return redirect('/friends')

def destroy(request, idnum):
    if request.session['is_signed_in'] == False:
        return redirect('/main')
    try:
        Friendship.objects.filter(friend1_id = request.session['id'], friend2_id = idnum).delete()
        Friendship.objects.filter(friend2_id = request.session['id'], friend1_id = idnum).delete()
    except:
        messages.error(request, 'Friend not found.')
    return redirect('/friends')

def users(request, idnum):
    if request.session['is_signed_in'] == False:
        return redirect('/main')
    try:                                                                                                                                
        friends = Friendship.objects.filter(friend1_id = idnum )
        if not friends.exists():
            friends = None
    except:
        friends = None
    try:
        user = Users.objects.get(id = idnum)
    except:
        users = None
    return render(request, 'users/users.html', {'friends' : friends, 'user':user})

# Create your views here.

