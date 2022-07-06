```{include} _templates/nav.html
```

# django-internetarchive-storage

A custom Django storage system for Internet Archive collections

```{contents} Sections
:local:
:depth: 1
```

## Installation

Install the package from PyPI.

```zsh
pipenv install django-internetarchive-storage
```

## Getting started

Configure the minimum options in your `settings.py` file.

```python
IA_STORAGE_ACCESS_KEY = "<your access key>"
IA_STORAGE_SECRET_KEY = "<your secret key>"
```

Set the other optional metadata settings that you'd like. The ones you add will be set as the default to items you upload.

```python
IA_STORAGE_COLLECTION = ""
IA_STORAGE_TITLE = ""
IA_STORAGE_CONTRIBUTOR = ""
IA_STORAGE_CREATOR = ""
IA_STORAGE_PUBLISHER = ""
IA_STORAGE_MEDIATYPE = ""
IA_STORAGE_DATE = None
IA_STORAGE_SUBJECT = []
IA_STORAGE_EXTRA_METADATA = {}
```

Import this library's custom `FileField` to your model's file and add it to a database table.

```python
from django.db import models
from ia_storage.fields import InternetArchiveFileField


class Memento(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField()
    data = InternetArchiveFileField()
```

After you've created your table via database migrations, you should be able to save files to the Internet Archive. It will
require that you submit two arguments to the field's save method.

The first is the unique identifier where the file will be stored as an "item" on archive.org.

The second is the file object containing the data you'd like to save. The file object must have a name attribute. It will be bundled as a "file" in the archive.org system that is attached to the parent item.

A metadata keyword argument accepts the extra information that will be attached to the identifier. Here's the complete list that are supported.

* title
* collection
* mediatype
* contributor
* creator
* publisher
* date
* subject
* extra_metadata

In cases where you provide metadata input, the system will override any of the global configurations in settings.py.

Saving an object can be done with Django's File object.

```python
from django.core.files.base import File

obj = Memento.objects.create(name="palewi.re", url="https://palewi.re")
with open("path/to/my/file.txt", "r") as f:
    obj.data.save(
        "my-unique-identifier",
        File(f),
        metadata=dict(
            title="My file title",
            collection="test_collection",
            mediatype="data",
            publisher="My name",
            creator="palewi.re",
        ),
    )
```

It can also be done with Django's in-memory ContentFile object. You should include the name keyword so that the Internet Archive knows what to call your file inside the item.

```python
from django.core.files.base import ContentFile

obj = Memento.objects.create(name="palewi.re", url="https://palewi.re")
obj.data.save(
    "my-unique-identifier",
    ContentFile(b"This is only a test", name="file.txt"),
    metadata=dict(
        title="My file title",  # <-- Here we assume some of the other options are already handled in settings.py
        mediatype="data",
    ),
)
```

## Contributing

Install dependencies for development

```zsh
pipenv install --dev
```

Run tests

```zsh
pipenv run python setup.py test
```
