import io
import os
import logging
import requests
import urllib.request
import internetarchive
from urllib.parse import urljoin
from django.conf import settings
from django.core.files.storage import Storage
from django.core.files.base import ContentFile, File

logger = logging.getLogger(__name__)


class InternetArchiveStorage(Storage):
    ACCESS_KEY = getattr(settings, 'IA_STORAGE_ACCESS_KEY', None)
    SECRET_KEY = getattr(settings, 'IA_STORAGE_SECRET_KEY', None)
    base_url = 'https://archive.org/download/'

    def _open(self, name, mode='rb'):
        logger.debug(f"Opening {name}")
        url = self.url(name)
        r = requests.get(url)
        return File(io.BytesIO(r.content))

    def save(self, identifier, content, max_length=None, metadata={}):
        # Parse the file out of the content input
        if isinstance(content, dict):
            filename, fileobj = list(content.items())[0]
            files = {filename: fileobj}
        elif isinstance(content, (File, ContentFile)):
            filename = os.path.basename(content.name)
            files = {filename: content.file}
        else:
            raise ValueError("Inputs must be File or ContentFile objects, or a file dict in the style requested by IA")

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
            files=files,
            metadata=clean_metadata
        )

        if self.ACCESS_KEY and self.SECRET_KEY:
            kwargs['access_key'] = self.ACCESS_KEY
            kwargs['secret_key'] = self.SECRET_KEY

        # Log some debugging stuff
        logger.debug("Uploading item to archive.org")
        logger.debug(f"identifier: {identifier}")
        logger.debug(f"name: {name}")
        logger.debug(f"content: {files}")
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
        exists = self.exists(identifier, filename)
        if exists:
            raise FileExistsError(f'File name of {filename} already exists in identifier {identifier}')
        # Assuming we are okay, return the path
        return path

    def url(self, name):
        return urljoin(self.base_url, name)

    def size(self, name):
        url = self.url(name)
        r = urllib.request.urlopen(url)
        return r.length

    def exists(self, identifier, filename):
        # Query the file list from the API
        logger.debug(f"Seeing if {identifier}/{filename} exists")
        results = list(internetarchive.get_files(identifier, filename))
        logger.debug(f"results: {results}")
        return len(results) > 0

    def delete(self, identifier, filename):
        kwargs = {}
        if self.ACCESS_KEY and self.SECRET_KEY:
            kwargs['access_key'] = self.ACCESS_KEY
            kwargs['secret_key'] = self.SECRET_KEY
        logger.debug(f"Deleting {identifier}/{filename}")
        internetarchive.delete(identifier, filename, **kwargs)
