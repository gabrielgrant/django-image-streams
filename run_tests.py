
# from http://www.travisswicegood.com/2010/01/17/django-virtualenv-pip-and-fabric/
import os

from django.conf import settings
from django.core.management import call_command

def main():
    # Dynamically configure the Django settings with the minimum necessary to
    # get Django running tests
    settings.configure(
        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.admin',
            'django.contrib.sessions',
            'django.contrib.sites',
            'image_streams',
            'image_streams.tests',
        ),
        # Django replaces this, but it still wants it. *shrugs*
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': '/tmp/django_test.db',
            }
        },
        MEDIA_ROOT = '/tmp/django_test_media/',
        ROOT_URLCONF = '',
        DEBUG = True,
		TEMPLATE_DEBUG = True,
		SITE_ID = 1,
    ) 
    
    #call_command('syncdb')
    
    # Fire off the tests
    call_command('test', 'image_streams')
    

if __name__ == '__main__':
    main()

