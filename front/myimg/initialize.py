#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
initializes the database atomically.
'''

import sys

from mongoengine import connect

from thumby.models import User

def initialize(port):
    '''
    This method creates database data. THIS NEEDS TO BE
    IDEMPOTENT (can be run many times with no side-effects).
    '''

    print "Initializing DB"

    connect('myimg_set', port=port)
    __create_admin_users()

def __create_admin_users():
    '''Creates users that can access the administration'''
    admins = (
        (u'Bernardo Heynemann', 'heynemann@gmail.com'),
        (u'Fábio Miranda Costa', 'fabiomcosta@gmail.com'),
        (u'Rafael Carício', 'rafael@caricio.com')
    )

    for name, email in admins:
        admin = User.objects(email=email)

        if not len(admin):
            print "User %s not found! Creating..." % name
            admin = User(email=email,
                         name=name,
                         locale='en-us',
                         is_admin=True)
            admin.save()
        else:
            print "User %s was already in the DB" % name

if __name__ == "__main__":
    port = len(sys.argv) > 1 and int(sys.argv[1]) or 27017
    initialize(port)

