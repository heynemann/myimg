#!/usr/bin/python
# -*- coding: utf-8 -*-

import functools
import urllib
import urlparse

from pymongo import Connection
import asyncmongo
import tornado.web

from myimg.models import User

class BaseHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        if not hasattr(self, '_db'):
            self._db = asyncmongo.Client(pool_id='myimg',
                                         host=self.dbhost,
                                         port=self.dbport,
                                         maxcached=10,
                                         maxconnections=50,
                                         dbname=self.dbname)
        return self._db

    @property
    def block_db(self):
        if not hasattr(self, '_block_db'):
            self._block_db = Connection(host=self.dbhost,
                                        port=self.dbport)[self.dbname]
        return self._block_db

    def get_current_user(self, callback=None):
        email = self.get_cookie('user', None)

        if not email:
            if callback:
                callback(None)
            else:
                return None

        def on_return_current_user(response, error=None):
            if not error:
                callback(response)
            callback(None)

        if callback:
            self.db.users.find_one({ 'email': email }, callback=on_return_current_user)
        else:
            user = self.block_db.users.find_one({ 'email': email })
            on_return_current_user(user)

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
