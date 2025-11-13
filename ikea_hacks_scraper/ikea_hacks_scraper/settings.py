# Scrapy settings for ikea_hacks_scraper project

BOT_NAME = "ikea_hacks_scraper"

SPIDER_MODULES = ["ikea_hacks_scraper.spiders"]
NEWSPIDER_MODULE = "ikea_hacks_scraper.spiders"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Politeness settings - consolidated
DOWNLOAD_DELAY = 2  
CONCURRENT_REQUESTS = 8
CONCURRENT_REQUESTS_PER_DOMAIN = 4

# User agent 
USER_AGENT = 'Mozilla/5.0 (compatible; IkeaHacksScraper/1.0; Educational IR Project)'

# Auto-throttle extension 
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 3
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0

# Disable cookies
COOKIES_ENABLED = False

# Log level 
LOG_LEVEL = 'INFO'

# Feed export encoding
FEED_EXPORT_ENCODING = "utf-8"