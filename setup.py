from distutils.core import setup

setup(
    name='pi_reminder',
    version='0.1',
    packages=['google-api-python-client, httplib2, oauth2client, unicornhat'],
    url='https://github.com/johnwargo/pi_remind',
    license='MIT',
    author='John M. Wargo',
    author_email='john@johnwargo.com',
    description='Raspberry Pi-based Google Calendar reminder system'
)
