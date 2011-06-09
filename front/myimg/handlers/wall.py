#!/usr/bin/python
# -*- coding: utf-8 -*-

import tornado.web

from myimg.handlers.base import BaseHandler

class WallHandler(BaseHandler):

    def get(self, user):
        self.render("wall.html")

