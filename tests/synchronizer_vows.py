#!/usr/bin/python
# -*- coding: utf-8 -*-

from os.path import expanduser, join

from pyvows import Vows, expect

from syncr.synchronizer import Synchronizer

my_pictures_folder = join(expanduser('~'), 'Pictures')
@Vows.batch
class SynchronizerVows(Vows.Context):

    class WhenDefaultFolder(Vows.Context):
        def topic(self):
            return Synchronizer(None)

        def should_have_proper_pictures_folder(self, topic):
            expect(topic.folder).to_equal(my_pictures_folder)

    class WhenSpecifiedFolder(Vows.Context):
        def topic(self):
            return Synchronizer(None, folder='/tmp')

        def should_have_proper_pictures_folder(self, topic):
            expect(topic.folder).to_equal('/tmp')

    class WhenInvalidFolder(Vows.Context):
        def topic(self):
            return Synchronizer(None, folder='/tmp/invalid')

        def should_be_an_error(self, topic):
            expect(topic).to_be_an_error()

        def should_be_a_value_error(self, topic):
            expect(topic).to_be_an_error_like(ValueError)



