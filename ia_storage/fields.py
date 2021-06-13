from ia_storage.storage import InternetArchiveStorage
from django.db.models.fields.files import FieldFile, FileField

fs = InternetArchiveStorage()


class InternetArchiveFieldFile(FieldFile):

    def save(self, name, content, save=True, metadata={}):
        name = self.field.generate_filename(self.instance, name)
        self.name = self.storage.save(
            name,
            content,
            max_length=self.field.max_length,
            metadata=metadata
        )
        setattr(self.instance, self.field.attname, self.name)
        self._committed = True

        # Save the object because it has changed, unless save is False
        if save:
            self.instance.save()


class InternetArchiveFileField(FileField):
    attr_class = InternetArchiveFieldFile
