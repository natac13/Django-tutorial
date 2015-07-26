""" A collection of the urls that get inculded with mysite/urls.py which has
the code looking at the url patterns to map to the app's urls and views which
is this file, and polls/views.
"""

from django.conf.urls import url
from . import views

# url() is passed two args, one being the regular expression and the second is
# the view. there are also optional key word arguments that can be used.

# The regex is for after the domain name and does not include the GET or POST
# information so nothing in the query string which is after the '?'.

# Continuing from the polls/views.py file to explain the regular expressions.
# The (?P<question_id>[pattern]) is to name the group to pass as a key work
# argument to the functions in views. When the patterns get matched the url()
# function will call the views functions.
#
# To explain the regex it is
# r - is a raw string to python
# ^ - matches the beginning of the string in this case, what is after domain
# (?P<[var_name]>[pattern]) - the capture a group to match the pattern and
# give it the name var_name.
# $ - matches the end of string
#
# The url() takes the regex, then the view then 3 optional arguments. However
# the last ('prefix') will be got since it is only needed when using a string
# for the view argument which has been deprecated since Django 1.8.
#
# view - is a callable function.
#
# Key word arguments which get passed into the view function being called.
# This is just like how the named groups in the regex are passed to the
# function.
#
# name - is for url reverse calling... not sure what this means. From the docs
# it states that if is to call refer to the url from anywhere in Django in a
# clear manner.
urlpatterns = [
    # Ex. /polls/
    url(r'^$', views.IndexView.as_view(), name='index'),
    # Ex. /polls/5/
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    # Ex. /polls/5/results/
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(),
        name='results'),
    # Ex. /polls/5/vote
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]
