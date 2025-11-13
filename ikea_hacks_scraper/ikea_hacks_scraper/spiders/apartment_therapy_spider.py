import scrapy
from ikea_hacks_scraper.items import IkeaHackItem
import re

class ApartmentTherapySpider(scrapy.Spider):
    name = 'apartmenttherapy'
    allowed_domains = ['apartmenttherapy.com']
    
    start_urls = [
        'https://www.apartmenttherapy.com/ikea-hacks',
    ]
    
    custom_settings = {
        'DOWNLOAD_DELAY': 2,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 4,
    }
    
    page_count = 0
    max_pages = 20
    
    def parse(self, response):
        """
        Parse article listing page
        """
        # Find article links
        article_links = response.css('article h2 a::attr(href)').getall()
        
        if not article_links:
            article_links = response.css('article a.post-title::attr(href)').getall()
        
        if not article_links:
            article_links = response.css('div.post-item a::attr(href)').getall()
        
        # Filter for IKEA-related articles
        ikea_links = [link for link in article_links if link and 'ikea' in link.lower()]
        
        self.logger.info(f'Found {len(ikea_links)} IKEA articles on page: {response.url}')
        
        # Follow each article
        for link in ikea_links:
            yield response.follow(link, callback=self.parse_article)
        
        # Pagination
        self.page_count += 1
        if self.page_count < self.max_pages:
            next_page = response.css('a.next::attr(href)').get()
            if not next_page:
                next_page = response.css('a[rel="next"]::attr(href)').get()
            
            if next_page:
                self.logger.info(f'Following next page {self.page_count + 1}')
                yield response.follow(next_page, callback=self.parse)
    
    def parse_article(self, response):
        """
        Parse individual article
        """
        item = IkeaHackItem()
        
        # Title
        item['title'] = response.css('h1.entry-title::text').get()
        if not item['title']:
            item['title'] = response.css('h1::text').get()
        
        if item['title']:
            item['title'] = item['title'].strip()
        
        # Content
        paragraphs = response.css('div.entry-content p::text').getall()
        if not paragraphs:
            paragraphs = response.css('article p::text').getall()
        
        item['content'] = ' '.join([p.strip() for p in paragraphs if p.strip()])
        
        # Author
        item['author'] = response.css('a.author-name::text').get()
        if not item['author']:
            item['author'] = response.css('span.author::text').get()
        if not item['author']:
            item['author'] = 'Apartment Therapy'
        else:
            item['author'] = item['author'].strip()
        
        # Date
        item['date'] = response.css('time::attr(datetime)').get()
        if not item['date']:
            item['date'] = response.css('meta[property="article:published_time"]::attr(content)').get()
        
        # URL
        item['url'] = response.url
        
        # Categories
        item['categories'] = response.css('a.category::text').getall()
        if not item['categories']:
            item['categories'] = ['IKEA', 'Home Decor']
        
        # Tags
        item['tags'] = ['ikea', 'hack', 'diy', 'home-decor']
        
        # Image
        item['image_url'] = response.css('meta[property="og:image"]::attr(content)').get()
        if not item['image_url']:
            item['image_url'] = response.css('article img::attr(src)').get()
        
        # Excerpt
        if item['content']:
            item['excerpt'] = item['content'][:200] + '...' if len(item['content']) > 200 else item['content']
        else:
            item['excerpt'] = item['title']
        
        if item['title']:
            self.logger.info(f'✓ Scraped: {item["title"][:60]}')
            yield item