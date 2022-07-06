import os
from distutils.core import Command

from setuptools import setup


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
            IA_STORAGE_ACCESS_KEY=os.getenv("IA_STORAGE_ACCESS_KEY"),
            IA_STORAGE_SECRET_KEY=os.getenv("IA_STORAGE_SECRET_KEY"),
            IA_STORAGE_COLLECTION="test_collection",
            IA_STORAGE_CONTRIBUTOR="palewire",
            IA_STORAGE_CREATOR="palewire",
            IA_STORAGE_PUBLISHER="california-civic-data-coalition/django-internetarchive-storage",
            IA_STORAGE_MEDIATYPE="data",
            IA_STORAGE_SUBJECT=["test"],
            DATABASES={
                "default": {"NAME": ":memory:", "ENGINE": "django.db.backends.sqlite3"}
            },
            INSTALLED_APPS=("ia_storage",),
            DEFAULT_AUTO_FIELD="django.db.models.BigAutoField",
            LOGGING={
                "version": 1,
                "disable_existing_loggers": False,
                "handlers": {
                    "file": {
                        "level": "DEBUG",
                        "class": "logging.FileHandler",
                        "filename": os.path.join(
                            os.path.dirname(__file__), "tests.log"
                        ),
                    },
                    "console": {
                        "class": "logging.StreamHandler",
                    },
                },
                "formatters": {
                    "verbose": {
                        "format": "%(levelname)s|%(asctime)s|%(module)s|%(message)s",
                        "datefmt": "%d/%b/%Y %H:%M:%S",
                    }
                },
                "loggers": {
                    "ia_storage": {
                        "handlers": ["console"],
                        "level": "DEBUG",
                        "propagate": True,
                    },
                },
            },
        )
        from django.core.management import call_command

        django.setup()
        call_command("test", "ia_storage")


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


def version_scheme(version):
    """
    Version scheme hack for setuptools_scm.

    Appears to be necessary to due to the bug documented here: https://github.com/pypa/setuptools_scm/issues/342

    If that issue is resolved, this method can be removed.
    """
    import time

    from setuptools_scm.version import guess_next_version

    if version.exact:
        return version.format_with("{tag}")
    else:
        _super_value = version.format_next_version(guess_next_version)
        now = int(time.time())
        return _super_value + str(now)


def local_version(version):
    """
    Local version scheme hack for setuptools_scm.

    Appears to be necessary to due to the bug documented here: https://github.com/pypa/setuptools_scm/issues/342

    If that issue is resolved, this method can be removed.
    """
    return ""


setup(
    name="django-internetarchive-storage",
    description="A custom Django storage system for Internet Archive collections",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="Ben Welsh",
    author_email="b@palewi.re",
    url="https://palewi.re/docs/django-internetarchive-storage",
    license="MIT",
    packages=("ia_storage",),
    install_requires=[
        "internetarchive",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
    ],
    project_urls={
        "Maintainer": "https://github.com/palewire",
        "Source": "https://github.com/palewire/django-internetarchive-storage",
        "Tracker": "https://github.com/palewire/django-internetarchive-storage/issues",
        "Docs": "https://palewi.re/docs/django-internetarchive-storage",
    },
    cmdclass={"test": TestCommand},
    setup_requires=["setuptools_scm"],
    use_scm_version={"version_scheme": version_scheme, "local_scheme": local_version},
)
