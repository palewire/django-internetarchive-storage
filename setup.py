import os
from setuptools import setup
from distutils.core import Command


class TestCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import django
        from django.conf import settings
        settings.configure(
            IA_STORAGE_ACCESS_KEY=os.getenv('IA_STORAGE_ACCESS_KEY'),
            IA_STORAGE_SECRET_KEY=os.getenv('IA_STORAGE_SECRET_KEY'),
            IA_STORAGE_COLLECTION='test_collection',
            IA_STORAGE_CONTRIBUTOR='palewire',
            IA_STORAGE_CREATOR="palewire",
            IA_STORAGE_PUBLISHER='california-civic-data-coalition/django-internetarchive-storage',
            IA_STORAGE_MEDIATYPE="data",
            IA_STORAGE_SUBJECT=['test'],
            DATABASES={
                'default': {
                    'NAME': ':memory:',
                    'ENGINE': 'django.db.backends.sqlite3'
                }
            },
            INSTALLED_APPS=('ia_storage',),
            DEFAULT_AUTO_FIELD='django.db.models.BigAutoField',
            LOGGING = {
                'version': 1,
                'disable_existing_loggers': False,
                'handlers': {
                    'file': {
                        'level': 'DEBUG',
                        'class': 'logging.FileHandler',
                        'filename': os.path.join(os.path.dirname(__file__), 'tests.log'),
                    },
                    'console': {
                        'class': 'logging.StreamHandler',
                    },
                },
                'formatters': {
                    'verbose': {
                        'format': '%(levelname)s|%(asctime)s|%(module)s|%(message)s',
                        'datefmt': "%d/%b/%Y %H:%M:%S"
                    }
                },
                'loggers': {
                    'ia_storage': {
                        'handlers': ['console'],
                        'level': 'DEBUG',
                        'propagate': True,
                    },
                }
            }
        )
        from django.core.management import call_command
        django.setup()
        call_command('test', 'ia_storage')


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


setup(
    name='django-internetarchive-storage',
    version='0.0.1',
    description="A custom Django storage system for Internet Archive collections",
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    author='Ben Welsh',
    author_email='b@palewi.re',
    url='http://www.github.com/california-civic-data-coalition/django-internetarchive-storage',
    license="MIT",
    packages=("ia_storage",),
    install_requires=[
        'internetarchive',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
    ],
    project_urls={
        'Maintainer': 'https://github.com/california-civic-data-coalition',
        'Source': 'https://github.com/datadesk/california-civic-data-coalition/django-internetarchive-storage',
        'Tracker': 'https://github.com/datadesk/<california-civic-data-coalition/django-internetarchive-storage/issues'
    },
    cmdclass={'test': TestCommand}
)
