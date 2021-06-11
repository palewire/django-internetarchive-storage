from django.db import models
from django.test import TestCase
from django.core.files.base import ContentFile
from ia_storage import InternetArchiveStorage

fs = InternetArchiveStorage()


class TestModel(models.Model):
    data = models.FileField(storage=fs)


class InternetArchiveStorageTests(TestCase):

    def setUp(self):
        pass

    def test_archive(self):
        obj = TestModel.objects.create()
        obj.data.save('test.txt', ContentFile('A string with the file content'))
        self.assertEqual(obj.data.name, 'test.txt')
