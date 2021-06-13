import io
from django.db import models
from django.test import TestCase
from ia_storage import InternetArchiveStorage
from django.db.models.fields.files import FieldFile, FileField
# from django.core.files.base import ContentFile
from django.utils.crypto import get_random_string

fs = InternetArchiveStorage()


class InternetArchiveFieldFile(FieldFile):

    def save(self, name, content, save=True, metadata={}):
        name = self.field.generate_filename(self.instance, name)
        self.name = self.storage.save(name, content, max_length=self.field.max_length, metadata=metadata)
        setattr(self.instance, self.field.attname, self.name)
        self._committed = True

        # Save the object because it has changed, unless save is False
        if save:
            self.instance.save()


class InternetArchiveFileField(FileField):
    attr_class = InternetArchiveFieldFile


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
