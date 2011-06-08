#!/usr/bin/python
# -*- coding: utf-8 -*-

import functools
import urllib
import urlparse

import tornado.web

from thumby.models import User

class BaseHandler(tornado.web.RequestHandler):

    def get_current_user(self):
        email = self.get_cookie('user', None)

        if not email:
            return None

        user = User.objects(email=email)
        if len(user):
            return user[0]

        return None

def admin_authenticated(method):
    """Decorate methods with this to require that the user be logged in."""
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if self.current_user and not self.current_user.is_admin:
            raise tornado.web.HTTPError(404)

        if not self.current_user:
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
    return wrapper
