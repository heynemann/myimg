#!/usr/bin/python
# -*- coding: utf-8 -*-
'''Models available to thumby front-end website'''

import datetime
import hashlib

from mongoengine import *

class User(Document):
    '''Defines a thumby user'''

    email = StringField(max_length=500, required=True)
    name = StringField(max_length=500, required=True)
    slug = StringField(max_length=500, required=True)
    security_key = StringField(max_length=16, required=True)
    locale = StringField(max_length=10, required=True, default='en-us')

    #optional fields
    is_admin = BooleanField(required=True, default=False)
    date_modified = DateTimeField(default=datetime.datetime.now)

    def get_security_key(self):
        md5 = hashlib.md5(self.email).hexdigest()[:16]

        return md5

    def get_unique_hash(self, length=4):
        md5 = hashlib.md5(self.email).hexdigest()[:length]

        has_user = len(User.objects(slug=md5))
        if has_user:
            return self.get_unique_hash(length + 1)

        return md5

class Hit(EmbeddedDocument):

    url = StringField()
    referrer = StringField()
    ip = StringField()

class UserAccount(Document):

    user = ReferenceField(User)
    hits = ListField(EmbeddedDocumentField(Hit))
