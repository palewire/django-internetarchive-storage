import os
import logging
import internetarchive
from urllib.parse import urljoin
from django.conf import settings
# from django.core.files import File
from django.core.files.storage import Storage
from django.utils.text import get_valid_filename
from django.utils.crypto import get_random_string
from django.utils.encoding import filepath_to_uri

logger = logging.getLogger(__name__)


class InternetArchiveStorage(Storage):
    ACCESS_KEY = getattr(settings, 'IA_STORAGE_ACCESS_KEY', None)
    SECRET_KEY = getattr(settings, 'IA_STORAGE_SECRET_KEY', None)

    def _open(self, name, mode='rb'):
        logger.debug(f"Opening {name}")
        # Get the file and open it
        # TK
        # Return it as a File object
        return name

    def save(self, name, content, max_length=None):
        name = self.get_available_name(name, max_length=max_length)
        return self._save(name, content)

    def _save(self, name, content):
        # Validate the file
        files = content['file']

        # Pull metadata from the content input
        kwargs = content.get('metadata', {})

        # Set the metadata what will be uploaded
        metadata = {}
        if kwargs.get('collection') or getattr(settings, 'IA_STORAGE_COLLECTION', None):
            metadata['collection'] = kwargs.get('collection') or getattr(settings, 'IA_STORAGE_COLLECTION', None)

        if kwargs.get('title') or getattr(settings, 'IA_STORAGE_TITLE', None):
            metadata['title'] = kwargs.get('title') or getattr(settings, 'IA_STORAGE_TITLE', None)

        if kwargs.get('mediatype') or getattr(settings, 'IA_STORAGE_MEDIATYPE', None):
            metadata['mediatype'] = kwargs.get('mediatype') or getattr(settings, 'IA_STORAGE_MEDIATYPE', None)

        if kwargs.get('contributor') or getattr(settings, 'IA_STORAGE_CONTRIBUTOR', None):
            metadata['contributor'] = kwargs.get('contributor') or getattr(settings, 'IA_STORAGE_CONTRIBUTOR', None)

        if kwargs.get('creator') or getattr(settings, 'IA_STORAGE_CREATOR', None):
            metadata['creator'] = kwargs.get('creator') or getattr(settings, 'IA_STORAGE_CREATOR', None)

        if kwargs.get('publisher') or getattr(settings, 'IA_STORAGE_PUBLISHER', None):
            metadata['publisher'] = kwargs.get('publisher') or getattr(settings, 'IA_STORAGE_PUBLISHER', None)

        if kwargs.get('date') or getattr(settings, 'IA_STORAGE_DATE', None):
            metadata['date'] = kwargs.get('date') or getattr(settings, 'IA_STORAGE_DATE', None)

        if kwargs.get('subject') or getattr(settings, 'IA_STORAGE_SUBJECT', None):
            metadata['subject'] = kwargs.get('subject') or getattr(settings, 'IA_STORAGE_SUBJECT', None)

        if kwargs.get('extra_metadata') or getattr(settings, 'IA_STORAGE_EXTRA_METADATA', {}):
            e = kwargs.get('extra_metadata') or getattr(settings, 'IA_STORAGE_EXTRA_METADATA', {})
            metadata.update(**e)

        # Prep the upload
        kwargs = dict(
            files=files,
            metadata=metadata
        )

        if self.ACCESS_KEY and self.SECRET_KEY:
            kwargs['access_key'] = self.ACCESS_KEY
            kwargs['secret_key'] = self.SECRET_KEY

        # Print some debugging stuff
        logger.debug(f"Uploading item to archive.org")
        logger.debug(f"name: {name}")
        logger.debug(f"content: {content}")
        logger.debug(f"metadata: {metadata}")
        logger.debug(f"kwargs: {kwargs}")

        # Do the upload
        item = internetarchive.upload(name, **kwargs)
        logger.debug(item)

        # Return the name saved to the backend
        return name

    def get_valid_name(self, name):
        """
        Return a filename, based on the provided filename, that's suitable for
        use in the target storage system.
        """
        return get_valid_filename(name)

    def get_alternative_name(self, file_root, file_ext):
        """
        Return an alternative filename, by adding an underscore and a random 7
        character alphanumeric string (before the file extension, if one
        exists) to the filename.
        """
        return '%s_%s%s' % (file_root, get_random_string(7), file_ext)

    def get_available_name(self, name, max_length=None):
        """
        Return a filename that's free on the target storage system and
        available for new content to be written to.
        """
        # Figure out if the name already exists on Internet Archive
        return name

    def delete(self, name):
        if not name:
            raise ValueError('The name must be given to delete().')
        name = self.path(name)
        # If the file or directory exists, delete it from the filesystem.
        try:
            if os.path.isdir(name):
                os.rmdir(name)
            else:
                os.remove(name)
        except FileNotFoundError:
            # FileNotFoundError is raised if the file or directory was removed
            # concurrently.
            pass

    def exists(self, name):
        return os.path.lexists(self.path(name))

    def listdir(self, path):
        path = self.path(path)
        directories, files = [], []
        with os.scandir(path) as entries:
            for entry in entries:
                if entry.is_dir():
                    directories.append(entry.name)
                else:
                    files.append(entry.name)
        return directories, files

    def size(self, name):
        return os.path.getsize(self.path(name))

    def url(self, name):
        if self.base_url is None:
            raise ValueError("This file is not accessible via a URL.")
        url = filepath_to_uri(name)
        if url is not None:
            url = url.lstrip('/')
        return urljoin(self.base_url, url)
