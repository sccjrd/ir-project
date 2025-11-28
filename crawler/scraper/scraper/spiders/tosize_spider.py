import scrapy
from scraper.items import IkeaHackItem


class TosizeSpider(scrapy.Spider):
    name = "tosize"
    allowed_domains = ["tosize.it"]
    start_urls = [
        "https://www.tosize.it/en-it/diy/type/ikea-hacks"
    ]

    custom_settings = {
        "DOWNLOAD_DELAY": 1.0,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2,
    }

    def parse(self, response):
        """
        Parse the listing page of IKEA hacks and follow project links.
        """
        # Collect DIY project links
        project_links = response.css("article a::attr(href)").getall()
        if not project_links:
            project_links = response.css("a.project-link::attr(href)").getall()
        if not project_links:
            project_links = response.css(
                "div.project-item a::attr(href)").getall()
        if not project_links:
            project_links = response.css(
                "a[href*='/diy/']::attr(href)").getall()

        # Filter for project URLs: contain /diy/ but not /type/
        filtered = [
            link for link in project_links
            if link and "/diy/" in link and "/type/" not in link
        ]

        # Deduplicate while keeping order
        seen = set()
        final_links = []
        for href in filtered:
            full = response.urljoin(href)
            if full not in seen:
                seen.add(full)
                final_links.append(full)

        self.logger.info(
            f"[tosize] Found {len(final_links)} unique project links on: {response.url}"
        )

        for url in final_links[:20]:  # soft limit per page
            yield scrapy.Request(url, callback=self.parse_project)

        # Pagination
        next_page = (
            response.css("a.next::attr(href)").get()
            or response.css("link[rel='next']::attr(href)").get()
        )
        if next_page:
            next_url = response.urljoin(next_page)
            self.logger.info(f"[tosize] Following next page: {next_url}")
            yield scrapy.Request(next_url, callback=self.parse)

    def parse_project(self, response):
        """
        Parse an individual IKEA hack project page on Tosize.
        """
        item = IkeaHackItem()

        title = (
            response.css("h1::text").get()
            or response.css("h1 span::text").get()
            or response.css("title::text").get()
        )
        if title:
            title = title.strip()
        item["title"] = title

        # Content: description + article text
        content_parts = (
            response.css("div.description p::text").getall()
            or response.css("article p::text").getall()
            or response.css("div.content p::text").getall()
        )
        content = " ".join(p.strip() for p in content_parts if p.strip())
        item["content"] = content

        author = (
            response.css("span.author::text").get()
            or response.css(".author a::text").get()
            or "Tosize Community"
        )
        date = response.css("time::attr(datetime)").get()

        item["author"] = author
        item["date"] = date
        item["url"] = response.url
        item["categories"] = ["ikea-hacks", "diy"]
        item["tags"] = ["ikea", "hack", "diy"]

        image_url = response.css("article img::attr(src)").get()
        if not image_url:
            image_url = response.css("img::attr(src)").get()
        if image_url:
            image_url = response.urljoin(image_url)
        item["image_url"] = image_url

        if content:
            excerpt = (
                content[:200] + "..." if len(content) > 200 else content
            )
        else:
            excerpt = None
        item["excerpt"] = excerpt or title

        if title:
            self.logger.info(f"[tosize] - Scraped: {title[:60]}")
            yield item
        else:
            self.logger.warning(f"[tosize] Skipped (no title): {response.url}")
