#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re
from os.path import expanduser, abspath, join, exists
import fnmatch
from glob import glob

def locate(pattern, matcher="fn", root=os.curdir, recursive=True):
    root_path = os.path.abspath(root)

    if recursive:
        return_files = []
        for path, dirs, files in os.walk(root_path):
            if matcher == 'fn':
                for filename in fnmatch.filter(files, pattern):
                    return_files.append(os.path.join(path, filename))
            if matcher == 'regex':
                for filename in files:
                    if re.match(pattern, filename):
                        return_files.append(os.path.join(path, filename))
        return return_files
    else:
        return glob(join(root_path, pattern))

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

        downloads = []
        uploads = []

        for filename in local_files:
            if not filename in user_files:
                uploads.append(filename)

        return {
            'download': downloads,
            'upload': uploads
        }
