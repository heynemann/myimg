#!/usr/bin/python
# -*- coding: utf-8 -*-
'''Models available to myimg front-end website'''

import datetime
import hashlib

class Document(object):
    pass

class User(Document):
    '''Defines a myimg user'''

    def __init__(self):
        self.fields = {
            'email': None,
            'name': None,
            'security_key': None,
            'locale': 'en-us',

            'is_admin': False,
            'date_modified': datetime.datetime.now()
        }

        self.collection = 'users'

    @classmethod
    def get_security_key(cls, email):
        md5 = hashlib.md5(email).hexdigest()[:16]

        return md5

class UserAccount(Document):

    def __init__(self):
        self.fields = {
            'user': None
        }

        self.collection = 'user_account'

class Photo(Document):

    def __init__(self):
        self.fields = {
            'user': None,
            'original_url': None,
            'date': datetime.datetime.now()
        }

