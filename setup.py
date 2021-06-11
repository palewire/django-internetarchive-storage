import os
from setuptools import setup


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
)
