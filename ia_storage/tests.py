import io
from django.db import models
from django.test import TestCase
from ia_storage import InternetArchiveStorage
# from django.core.files.base import ContentFile
from django.utils.crypto import get_random_string

fs = InternetArchiveStorage()


class TestModel(models.Model):
    data = models.FileField(storage=fs)


class InternetArchiveStorageTests(TestCase):

    def setUp(self):
        pass

    def test_archive(self):
        suffix = get_random_string()
        identifier = f'django-internetarchive-storage-test-upload-{suffix}'
        content = dict(
            files={'text.txt': io.StringIO('A string with the file content')},
            metadata=dict(
                title=f'django-internetarchive-storage: Test upload {suffix}'
            )
        )
        obj = TestModel.objects.create()
        obj.data.save(
            identifier,
            content
        )
        # self.assertEqual(obj.data.name, identifier)
        # obj.data.open('rb')
        # self.assertEqual(obj.data.read(), 'A string with the file content')
        # obj.data.close()
