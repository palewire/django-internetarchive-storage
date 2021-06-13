import io
import os
import time
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

    def test_stringio(self):
        suffix = get_random_string()
        identifier = f'django-internetarchive-storage-test-upload-{suffix}'
        name = 'text.txt'
        filename = os.path.join(identifier, name)
        url = urljoin('https://archive.org/download/', filename)
        content = 'A string with the file content'

        # Upload the first object
        obj = TestModel.objects.create()
        obj.data.save(
            identifier,
            {name: io.StringIO(content)},
            metadata=dict(
                title=f'django-internetarchive-storage: Test upload {suffix}'
            )
        )
        self.assertEqual(obj.data.name, filename)
        self.assertEqual(obj.data.url, url)

        # Wait 30 seconds for the URL to show up on the web
        print("Sleeping 60 seconds")
        time.sleep(60)

        # Start checking stuff on the web
        self.assertEqual(obj.data.size, 30)

        obj.data.open()
        self.assertEqual(obj.data.read().decode("utf-8"), content)
        obj.data.close()

        # Throw an error if an object is re-uploaded with the same name
        with self.assertRaises(FileExistsError):
            obj2 = TestModel.objects.create()
            obj2.data.save(
                identifier,
                {name: io.StringIO(content)}
            )

        # Delete the file
        obj.data.delete()
