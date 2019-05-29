import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

class SetupStatus():
    setup_status = 0

    def finish_setup(self):
        setup_status = 1