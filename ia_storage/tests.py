import io
import os
from django.db import models
from django.test import TestCase
from urllib.parse import urljoin
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
        name = 'text.txt'
        filename = os.path.join(identifier, name)
        url = urljoin('https://archive.org/download/', filename)

        obj = TestModel.objects.create()
        content = {name: io.StringIO('A string with the file content')}
        obj.data.save(
            identifier,
            content,
            metadata=dict(
                title=f'django-internetarchive-storage: Test upload {suffix}'
            )
        )
        self.assertEqual(obj.data.name, filename)
        self.assertEqual(obj.data.url, url)

        # obj.data.open('rb')
        # self.assertEqual(obj.data.read(), 'A string with the file content')
        # obj.data.close()
