#!/usr/bin/python
# -*- coding: utf-8 -*-

from os.path import join, sep

class File(object):
    def __init__(self, path, filename, contents=None):
        self.path = path.lstrip(sep)
        self.filename = filename
        self.contents = contents

    @property
    def full_path(self):
        return join(self.path, self.filename.lstrip(sep))

    def read(self, basedir):
        self.contents = open(self.full_path, 'r').read()

    @classmethod
    def load(cls, path, filename):
        f = File(path, filename)

        return f

    @classmethod
    def load_from_model(cls, model):
        return File(model['path'], model['filename'])
