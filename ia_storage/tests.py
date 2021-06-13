import io
from django.db import models
from django.test import TestCase
from django.utils.crypto import get_random_string
from ia_storage.storage import InternetArchiveStorage
from ia_storage.fields import InternetArchiveFileField

fs = InternetArchiveStorage()


class TestModel(models.Model):
    data = InternetArchiveFileField(storage=fs)


class InternetArchiveStorageTests(TestCase):

    def setUp(self):
        pass

    def test_archive(self):
        suffix = get_random_string()
        identifier = f'django-internetarchive-storage-test-upload-{suffix}'
        content = {'text.txt': io.StringIO('A string with the file content')}
        obj = TestModel.objects.create()
        obj.data.save(
            identifier,
            content,
            metadata=dict(
                title=f'django-internetarchive-storage: Test upload {suffix}'
            )
        )
        # self.assertEqual(obj.data.name, identifier)
        # obj.data.open('rb')
        # self.assertEqual(obj.data.read(), 'A string with the file content')
        # obj.data.close()
