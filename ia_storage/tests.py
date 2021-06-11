from django.db import models
from django.test import TestCase
from django.core.files import File
from django.test.utils import override_settings
from ia_storage import InternetArchiveStorage

fs = InternetArchiveStorage()


class TestModel(models.Model):
    data = models.FileField(storage=fs)


@override_settings(MEDIA_ROOT='foobar')
class InternetArchiveStorageTests(TestCase):

    def setUp(self):
        self.test_file = File('Testing')

    def test_archive(self):
        TestModel.objects.create(
            data=self.test_file
        )
