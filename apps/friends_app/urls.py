from django.conf.urls import url
from views import *
urlpatterns = [ 
   url(r'^$', main, name = 'main'), 
    url(r'^main$', main, name = 'main'),
    url(r'^login$', login, name = 'login'),
    url(r'^register$', register, name = 'register'),
    url(r'^friends$', friends, name = 'friends'),
    url(r'^register/([0-9]+)$', success_reg, name = 'success_reg'),
    url(r'^add/([0-9]+)$', add, name = 'add'),
    url(r'^signout$', signout, name = 'signout'),
    url(r'^destroy/([0-9]+)$', destroy, name = 'destroy'),
    url(r'^users/([0-9]+)$', users, name = 'users'),
]