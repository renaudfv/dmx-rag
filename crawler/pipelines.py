from scrapy.pipelines.files import FilesPipeline
import os
from urllib.parse import urlparse

class CustomFilesPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        # Extract the filename from the URL
        parsed_url = urlparse(request.url)
        filename = os.path.basename(parsed_url.path)
        # Save the file directly in the root of FILES_STORE
        return filename