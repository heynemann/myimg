#!/usr/bin/python
# -*- coding: utf-8 -*-

from os.path import expanduser, abspath, join, exists

class Synchronizer():
    def __init__(self, context, api, folder=None):
        self.context = context
        self.api = api
        self.folder = folder
        self.__fix_folder()

    def __fix_folder(self):
        if self.folder is None:
            self.folder = self.__guess_pic_folder()
        if self.folder is None:
            raise ValueError("No folder found for pictures.")
        if not exists(self.folder):
            raise ValueError("The specified folder(%s) does not exist." % self.folder)

    def __guess_pic_folder(self):
        home = expanduser('~')
        folder = join(home, 'Pictures')
        if not exists(folder):
            folder = join(home, 'Pictures')

        if not exists(folder):
            return None

        return abspath(folder)

    def sync(self):
        user_files = self.api.get_files(self.context)
        local_files = self.api.get_local_files(self.context, self.folder)

        return {
            'download': [],
            'upload': []
        }
