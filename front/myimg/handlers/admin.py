#!/usr/bin/python
# -*- coding: utf-8 -*-

'''Admin handlers'''

import tornado.web

from thumby.handlers.base import BaseHandler, admin_authenticated

class AdminDashboardHandler(BaseHandler):
    '''handler for the first page of the website administration'''

    @admin_authenticated
    def get(self):
        self.write("Hello, admin")

