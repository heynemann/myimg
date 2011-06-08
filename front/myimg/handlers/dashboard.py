#!/usr/bin/python
# -*- coding: utf-8 -*-

import tornado.web

from thumby.handlers.base import BaseHandler
from thumby.models import UserAccount

class DashboardHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        user = self.get_current_user()

        user_account = UserAccount.objects(user=user)[0]

        self.render("dashboard.html", user=user, user_account=user_account)

