#!/usr/bin/python
# -*- coding: utf-8 -*-

from thumby.handlers.base import BaseHandler
from thumby.handlers.login import GoogleLoginHandler, FacebookLoginHandler
from thumby.models import User, UserAccount

class MainPageHandler(BaseHandler):

    def get(self):
        if (self.get_current_user()):
            self.redirect('/dashboard')
        self.render("home.html")

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

        users = User.objects(email=email)

        if not users:
            user = User(email=email, name="%s %s" % (first_name, last_name), locale=locale)
            user.slug = user.get_unique_hash()
            user.security_key = user.get_security_key()
            user.save()

            account = UserAccount(user=user)
            account.save()

        self.redirect('/dashboard')

class FacebookRegisterHandler(FacebookLoginHandler):
    pass

