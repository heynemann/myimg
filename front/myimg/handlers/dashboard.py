#!/usr/bin/python
# -*- coding: utf-8 -*-

import tornado.web

from myimg.handlers.base import BaseHandler
from myimg.models import UserAccount

class DashboardHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        def on_current_user(user):
            self.render("dashboard.html", user=user)
        self.get_current_user(on_current_user)

