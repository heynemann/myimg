#!/usr/bin/python
# -*- coding: utf-8 -*-

from os.path import expanduser, join, abspath, dirname

from pyvows import Vows, expect

from syncr.synchronizer import Synchronizer, locate
from syncr.models import File

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

        class WhenUploads(Vows.Context):
            class BecauseNotPresentOnServer(Vows.Context):
                def topic(self):
                    return Synchronizer({}, MockApi([]), folder=join(files_folder, 'not_present_on_server', 'from')).sync()

                def should_have_upload_collection(self, topic):
                    expect(topic['upload']).not_to_be_empty()

                def should_have_one_upload(self, topic):
                    expect(topic['upload']).to_length(1)

                def upload_should_be_file_object(self, topic):
                    expect(topic['upload'][0]).to_be_instance_of(File)

                def should_have_common(self, topic):
                    expect(topic['upload'][0].path).to_equal('/common.jpg')

            #class BecauseDifferentAndNewerThanServer(Vows.Context):
                #def topic(self):
                    #return Synchronizer({}, MockApi([{
                        
                    #}]), folder=join(files_folder, 'different_than_server', 'from')).sync()


class MockApi(object):
    def __init__(self, to=[]):
        self.to = to

    def get_files(self, context):
        return self.to

    def get_local_files(self, context, folder):
        return locate('(.+?)[.](jpe?g|gif|png)', matcher='regex', root=folder)

