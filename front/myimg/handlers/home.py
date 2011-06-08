#!/usr/bin/python
# -*- coding: utf-8 -*-

import asyncmongo

from myimg.handlers.base import BaseHandler
from myimg.handlers.login import GoogleLoginHandler, FacebookLoginHandler
from myimg.models import User

class MainPageHandler(BaseHandler):

    def get(self):
        def on_current_user(current_user):
            if current_user:
                self.redirect('/dashboard')
            self.render("home.html")

        self.get_current_user(on_current_user)

class RegisterHandler(BaseHandler):

    def get(self):
        self.render("register.html")

class GoogleRegisterHandler(GoogleLoginHandler):
    def _on_auth(self, user):
        super(GoogleRegisterHandler, self)._on_auth(user, redirect=False)

        email = self.get_cookie('user')
        first_name = self.get_cookie('firstname')
        last_name = self.get_cookie('lastname')
        locale = self.get_cookie('locale')


        def on_user(user, error):
            def redirect_to_dashboard(*args, **kwargs):
                self.redirect('/dashboard')

            if not error:
                user = dict(email=email, name="%s %s" % (first_name, last_name), locale=locale)
                user.update({'security_key': User.get_security_key(email) })

                self.db.users.update({ email: email }, user, upsert=True, callback=redirect_to_dashboard)
            else:
                redirect_to_dashboard()

        self.db.users.find_one({"email": email}, callback=on_user)

class FacebookRegisterHandler(FacebookLoginHandler):
    pass

