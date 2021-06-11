from django.db import models
from django.test import TestCase
from django.test.utils import override_settings


class TestModel(models.Model):
    pass


@override_settings(MEDIA_ROOT='foobar')
class InternetArchiveStorageTests(TestCase):

    def setUp(self):
        pass

    def test_archive(self):
        pass
