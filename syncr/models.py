#!/usr/bin/python
# -*- coding: utf-8 -*-

from os.path import join, sep

class File(object):
    def __init__(self, basefolder, path, contents=None):
        self.path = path
        self.basefolder = basefolder
        if contents is None:
            self.read()
        else:
            self.contents = contents

    def read(self):
        path = join(self.basefolder, self.path.lstrip(sep))
        self.contents = open(path, 'r').read()

    @classmethod
    def load(cls, basefolder, path):
        f = File(basefolder, path)

        return f
