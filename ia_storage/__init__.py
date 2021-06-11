import os
import logging
from urllib.parse import urljoin
from django.core.files import File
from django.core.files.storage import Storage
from django.utils.text import get_valid_filename
from django.utils.crypto import get_random_string
from django.utils.encoding import filepath_to_uri

logger = logging.getLogger(__name__)


class InternetArchiveStorage(Storage):

    def _open(self, name, mode='rb'):
        logger.debug(f"Opening {name}")
        # Get the file and open it
        # TK
        # Return it as a File object
        return File('')

    def _save(self, name, content):
        logger.debug(f"Saving {name}")
        # Save the content File object
        # TK
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
