from distutils.core import setup

setup(
    name='django-image-streams',
    version='0.1.0dev',
    packages=['image_streams',],
    include_package_data=True,
    author='Gabriel Grant',
    author_email='g@briel.ca',
    license='LGPL',
    long_description=open('README').read(),
    url='http://github.org/gabrielgrant/django-image-streams/',
)

