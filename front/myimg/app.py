#!/usr/bin/python
# -*- coding: utf-8 -*-

'''Application for running tornado front-end website'''

import os
from os.path import dirname, join, exists
from optparse import OptionParser

import tornado.ioloop
import tornado.web
from mongoengine import connect

from thumby.handlers import MainPageHandler, AdminDashboardHandler, \
        GoogleLoginHandler, RegisterHandler, GoogleRegisterHandler, DashboardHandler, \
        FacebookRegisterHandler, FacebookLoginHandler

from thumby.handlers import ChooseLoginHandler, LogoutHandler

def create_pid_file(pid_path):
    pid = os.getpid()
    with open(pid_path, 'w') as pid_file:
        pid_file.write(str(pid))

def destroy_pid_file(pid_path):
    if exists(pid_path):
        os.remove(pid_path)

def main():
    '''runs front-end server at specified por or 8000'''

    parser = OptionParser()
    parser.add_option("-i", "--dbhost", dest="dbhost", help="dbhost", default='0.0.0.0')
    parser.add_option("-t", "--dbport", type="int", dest="dbport", help="dbport", default=27017)
    parser.add_option("-p", "--port", type="int", dest="port", help="port", default=8000)
    parser.add_option("-d", "--pid", dest="pid", help="pid file", default=None)
    parser.add_option('-m', '--daemon', dest='daemon', action='store_true', default=False)
    parser.add_option("-l", "--log", dest="log", help="log path", default='/var/logs/thumby.log')

    (options, args) = parser.parse_args()

    settings = {
        'template_path': join(dirname(__file__), "templates"),
        "static_path": join(dirname(__file__), "static"),
        "cookie_secret": "TVktVkVSWS1TRUNVUkUtVEhVTUJZLUtFWQ==",
        "login_url": "/login",
    }

    application = tornado.web.Application([
        (r'/', MainPageHandler),
        (r'/register/?', RegisterHandler),
        (r'/register/google/?', GoogleRegisterHandler),
        (r'/register/facebook/?', FacebookRegisterHandler),
        (r'/admin/?', AdminDashboardHandler),
        (r'/login/?', ChooseLoginHandler),
        (r'/logout/?', LogoutHandler),
        (r'/login/google/?', GoogleLoginHandler),
        (r'/login/google/?', FacebookLoginHandler),
        (r'/dashboard/?', DashboardHandler),
    ], **settings)

    if options.pid:
        create_pid_file(options.pid)

    connect('thumby-set', host=options.dbhost, port=options.dbport)

    application.listen(options.port)

    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        if options.pid:
            destroy_pid_file(options.pid)
        print "Tornado instance at port %d finished by user interrupt." % options.port

if __name__ == "__main__":
    main()
