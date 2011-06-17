#!/usr/bin/python
# -*- coding: utf-8 -*-

import functools
import urllib
import urlparse

import tornado.web

from myimg.models import User

class BaseHandler(tornado.web.RequestHandler):

    def initialize(self, db=None, sync_db=None):
        self.db = db
        self.sync_db = sync_db

    def get_current_user(self, callback=None):
        email = self.get_cookie('user', None)

        if not email:
            return None

        return self.sync_db.users.find_one({ 'email': email })

def admin_authenticated(method):
    """Decorate methods with this to require that the user be logged in."""
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):

        def on_current_user(current_user):
            if current_user and not current_user.is_admin:
                raise tornado.web.HTTPError(404)

            if not current_user:
                if self.request.method in ("GET", "HEAD"):
                    url = self.get_login_url()
                    if "?" not in url:
                        if urlparse.urlsplit(url).scheme:
                            # if login url is absolute, make next absolute too
                            next_url = self.request.full_url()
                        else:
                            next_url = self.request.uri
                        url += "?" + urllib.urlencode(dict(next=next_url))
                    self.redirect(url)
                    return
                raise tornado.web.HTTPError(403)
            return method(self, *args, **kwargs)
        
        self.get_current_user(on_current_user)

    return wrapper
