from ia_storage.storage import InternetArchiveStorage
from django.db.models.fields.files import FieldFile, FileField


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

    def delete(self, save=True):
        if not self:
            return

        identifier, filename = self.name.split("/")
        self.storage.delete(identifier, filename)

        self.name = None
        setattr(self.instance, self.field.attname, self.name)
        self._committed = False

        if save:
            self.instance.save()


class InternetArchiveFileField(FileField):
    attr_class = InternetArchiveFieldFile

    def __init__(self, verbose_name=None, name=None, upload_to='', storage=InternetArchiveStorage, **kwargs):
        return super().__init__(
            verbose_name=verbose_name,
            name=name,
            upload_to=upload_to,
            storage=storage,
            **kwargs
        )
