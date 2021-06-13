import os
import logging
import urllib.request
import internetarchive
from urllib.parse import urljoin
from django.conf import settings
# from django.core.files import File
from django.core.files.storage import Storage
from django.utils.text import get_valid_filename
from django.utils.crypto import get_random_string

logger = logging.getLogger(__name__)


class InternetArchiveStorage(Storage):
    ACCESS_KEY = getattr(settings, 'IA_STORAGE_ACCESS_KEY', None)
    SECRET_KEY = getattr(settings, 'IA_STORAGE_SECRET_KEY', None)
    base_url = 'https://archive.org/download/'

    def _open(self, name, mode='rb'):
        logger.debug(f"Opening {name}")
        # Get the file and open it
        # TK
        # Return it as a File object
        return name

    def save(self, identifier, content, max_length=None, metadata={}):
        # Parse the file out of the content input
        if isinstance(content, dict):
            filename, fileobj = list(content.items())[0]

        name = self.get_available_name(identifier, filename, max_length=max_length)

        # Set the metadata what will be uploaded
        clean_metadata = {}
        if metadata.get('collection') or getattr(settings, 'IA_STORAGE_COLLECTION', None):
            clean_metadata['collection'] = metadata.get('collection') or getattr(settings, 'IA_STORAGE_COLLECTION', None)

        if metadata.get('title') or getattr(settings, 'IA_STORAGE_TITLE', None):
            clean_metadata['title'] = metadata.get('title') or getattr(settings, 'IA_STORAGE_TITLE', None)

        if metadata.get('mediatype') or getattr(settings, 'IA_STORAGE_MEDIATYPE', None):
            clean_metadata['mediatype'] = metadata.get('mediatype') or getattr(settings, 'IA_STORAGE_MEDIATYPE', None)

        if metadata.get('contributor') or getattr(settings, 'IA_STORAGE_CONTRIBUTOR', None):
            clean_metadata['contributor'] = metadata.get('contributor') or getattr(settings, 'IA_STORAGE_CONTRIBUTOR', None)

        if metadata.get('creator') or getattr(settings, 'IA_STORAGE_CREATOR', None):
            clean_metadata['creator'] = metadata.get('creator') or getattr(settings, 'IA_STORAGE_CREATOR', None)

        if metadata.get('publisher') or getattr(settings, 'IA_STORAGE_PUBLISHER', None):
            clean_metadata['publisher'] = metadata.get('publisher') or getattr(settings, 'IA_STORAGE_PUBLISHER', None)

        if metadata.get('date') or getattr(settings, 'IA_STORAGE_DATE', None):
            clean_metadata['date'] = metadata.get('date') or getattr(settings, 'IA_STORAGE_DATE', None)

        if metadata.get('subject') or getattr(settings, 'IA_STORAGE_SUBJECT', None):
            clean_metadata['subject'] = metadata.get('subject') or getattr(settings, 'IA_STORAGE_SUBJECT', None)

        if metadata.get('extra_metadata') or getattr(settings, 'IA_STORAGE_EXTRA_METADATA', {}):
            e = metadata.get('extra_metadata') or getattr(settings, 'IA_STORAGE_EXTRA_METADATA', {})
            clean_metadata.update(**e)

        # Prep the upload
        kwargs = dict(
            files=content,
            metadata=clean_metadata
        )

        if self.ACCESS_KEY and self.SECRET_KEY:
            kwargs['access_key'] = self.ACCESS_KEY
            kwargs['secret_key'] = self.SECRET_KEY

        # Print some debugging stuff
        logger.debug("Uploading item to archive.org")
        logger.debug(f"identifier: {identifier}")
        logger.debug(f"name: {name}")
        logger.debug(f"content: {content}")
        logger.debug(f"metadata: {clean_metadata}")

        # Do the upload
        item = internetarchive.upload(identifier, **kwargs)
        logger.debug(item)

        # Return the name saved to the backend
        return name

    def get_available_name(self, identifier, filename, max_length=None):
        """
        Return a filename that's free on the target storage system and
        available for new content to be written to.
        """
        # Merge the identifier and filename together
        path = os.path.join(identifier, filename)
        # Figure out if the name already exists on Internet Archive
        return path

    def url(self, name):
        return urljoin(self.base_url, name)

    def size(self, name):
        url = self.url(name)
        r = urllib.request.urlopen(url)
        return r.length

    # Stuff below here I haven't worked out yet

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
