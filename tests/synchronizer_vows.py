#!/usr/bin/python
# -*- coding: utf-8 -*-

from os.path import expanduser, join, abspath, dirname

from pyvows import Vows, expect

from syncr.synchronizer import Synchronizer

my_pictures_folder = join(expanduser('~'), 'Pictures')

fixture_folder = abspath(join(dirname(__file__), 'fixtures'))
files_folder = join(fixture_folder, 'files')

@Vows.batch
class SynchronizerVows(Vows.Context):

    class WhenDefaultFolder(Vows.Context):
        def topic(self):
            return Synchronizer({}, None)

        def should_have_proper_pictures_folder(self, topic):
            expect(topic.folder).to_equal(my_pictures_folder)

    class WhenSpecifiedFolder(Vows.Context):
        def topic(self):
            return Synchronizer({}, None, folder='/tmp')

        def should_have_proper_pictures_folder(self, topic):
            expect(topic.folder).to_equal('/tmp')

    class WhenInvalidFolder(Vows.Context):
        def topic(self):
            return Synchronizer({}, None, folder='/tmp/invalid')

        def should_be_an_error(self, topic):
            expect(topic).to_be_an_error()

        def should_be_a_value_error(self, topic):
            expect(topic).to_be_an_error_like(ValueError)

    class Syncing(Vows.Context):

        class WhenNothingToSync(Vows.Context):
            def topic(self):
                return Synchronizer({}, MockApi(), folder=join(files_folder, 'nothing_to_sync')).sync()

            def should_be_a_dict(self, topic):
                expect(topic).to_be_instance_of(dict)

            def should_have_down_key(self, topic):
                expect(topic).to_include('download')

            def should_have_up_key(self, topic):
                expect(topic).to_include('upload')

            def should_have_empty_down(self, topic):
                expect(topic['download']).to_be_empty()

            def should_have_empty_up(self, topic):
                expect(topic['upload']).to_be_empty()

class MockApi(object):
    def get_files(self, context):
        return []

    def get_local_files(self, context, folder):
        return []
