#!/usr/bin/python
# -*- coding: utf-8 -*-

import tornado.web
import tornado.auth

from myimg.handlers.base import BaseHandler

class ChooseLoginHandler(BaseHandler):
    def get(self):
        self.render('chooselogin.html')

class GoogleLoginHandler(BaseHandler, tornado.auth.GoogleMixin):

    @tornado.web.asynchronous
    def get(self):
        if self.get_argument("openid.mode", None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        self.authenticate_redirect()

    def _on_auth(self, user, redirect=True):
        if not user:
            self.clear_cookie('user')
            self.redirect('/?auth_failed')

        #{'locale': u'pt-br', 'first_name': u'Bernardo', 'last_name': u'Heynemann', 'name': u'Bernardo Heynemann', 'email': u'heynemann@gmail.com'}

        self.set_cookie('user', user['email'], expires_days=14)
        self.set_cookie('firstname', user['first_name'], expires_days=14)
        self.set_cookie('lastname', user['last_name'], expires_days=14)
        self.set_cookie('locale', user['locale'], expires_days=14)

        self._current_user = None

        if redirect:
            self._do_redirect()

    def _do_redirect(self):
        self.redirect(self.get_argument('next', '/'))

class FacebookLoginHandler(BaseHandler, tornado.auth.FacebookMixin):
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument("session", None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        self.authenticate_redirect()

    def _on_auth(self, user):
        if not user:
            self.redirect('/?auth_failed')

        # Save the user using, e.g., set_secure_cookie()


class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie('user')
        self.clear_cookie('firstname')
        self.clear_cookie('lastname')
        self.clear_cookie('locale')

        self.redirect('/')
