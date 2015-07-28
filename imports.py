'''
Created on Jul 21, 2015

@author: Florida

Init file to initialize all variables;
'''

print ('called imports');



import webapp2
import time;

from htmlStrings import *;
import jinja2;
import os,sys;
import MySQLdb;
from google.appengine.ext import blobstore;
from google.appengine.ext import ndb;
from google.appengine.ext.webapp import blobstore_handlers
from gaesessions import get_current_session;