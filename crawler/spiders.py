import scrapy
from scrapy.crawler import CrawlerProcess
import os

class SpecSheetSpider(scrapy.Spider):
    name = 'specsheet_spider'
    
    def __init__(self, start_urls=None, download_dir='downloads', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = start_urls or []
        self.download_dir = download_dir
        
        # Extract allowed domains from start_urls
        self.allowed_domains = [scrapy.utils.url.parse_url(url).hostname for url in self.start_urls]
        
        # Create download directory if it doesn't exist
        os.makedirs(self.download_dir, exist_ok=True)
    
    def parse(self, response):
        # Ensure the response is HTML
        if "text/html" not in response.headers.get("Content-Type", b"").decode("utf-8"):
            self.logger.warning(f"Skipping non-HTML response: {response.url}")
            return

        # Find PDF links
        pdf_links = response.css('a[href$=".pdf"]::attr(href)').getall()
        
        for pdf_link in pdf_links:
            full_pdf_url = response.urljoin(pdf_link)
            yield {
                'file_urls': [full_pdf_url],
                'source_url': response.url
            }
        
        # Follow other links for deeper crawling
        for next_page in response.css('a::attr(href)'):
            yield response.follow(next_page, self.parse)