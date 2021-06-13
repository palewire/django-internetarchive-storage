# django-internetarchive-storage

A custom Django storage system for Internet Archive collections

## Installation

Install the package from PyPI.

```zsh
pip install django-internetarchive-storage
```

Configure the minimum options in your `settings.py` file.

```python
IA_STORAGE_ACCESS_KEY = '<your access key>'
IA_STORAGE_SECRET_KEY = '<your secret key>'
```

Set the other optional metadata settings that you'd like. The ones you add will be set as the default to items you upload.

```python
IA_STORAGE_COLLECTION = 'test_collection'
IA_STORAGE_TITLE = ''
IA_STORAGE_CONTRIBUTOR = ''
IA_STORAGE_CREATOR = ''
IA_STORAGE_PUBLISHER = ''
IA_STORAGE_MEDIATYPE = ''
IA_STORAGE_DATE = None
IA_STORAGE_SUBJECT = []
IA_STORAGE_EXTRA_METADATA = {}
```

Import this library's custom `FileField` to your model's file and add it to a database table.

```python
from django.db import models
from ia_storage.fields import InternetArchiveFileField

class TestModel(models.Model):
    data = InternetArchiveFileField()
```

## Contributing

Install dependencies for development

```zsh
pipenv install --dev
```

Run tests

```zsh
make test
```

Ship new version to PyPI

```zsh
make ship
```
