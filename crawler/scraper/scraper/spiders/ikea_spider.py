import re
import scrapy

# adjust if your project/module name is different
from scraper.items import IkeaHackItem


class IkeaSpider(scrapy.Spider):
    name = "ikea"
    allowed_domains = ["ikeahackers.net"]
    start_urls = ["https://ikeahackers.net/category/hacks"]

    # Optional: be a bit gentle
    custom_settings = {
        "DOWNLOAD_DELAY": 1.0,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2,
    }

    def parse(self, response):
        """
        Parse the IKEA Hacks category listing page and follow article links.
        """
        # 1) get all <h2><a href="...">Article Title</a></h2> links
        raw_links = response.css("h2 a::attr(href)").getall()

        links = []
        for href in raw_links:
            if not href:
                continue
            full = response.urljoin(href)

            # stay on this site
            if "ikeahackers.net" not in full:
                continue

            # skip category/tag indexes
            if "/category/" in full or "/tag/" in full:
                continue

            # Keep only real post URLs which include /YYYY/ (e.g. /2025/11/...)
            if not re.search(r"/20\d{2}/", full):
                continue

            links.append(full)

        # dedupe while preserving order
        seen = set()
        article_links = []
        for url in links:
            if url not in seen:
                seen.add(url)
                article_links.append(url)

        self.logger.info(
            f"Found {len(article_links)} article links on {response.url}")

        # follow each article
        for url in article_links:
            yield response.follow(url, callback=self.parse_article)

        # pagination (page 2, 3, ...)
        next_page = response.css(
            "a.page-numbers.next::attr(href), a.next::attr(href)"
        ).get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_article(self, response):
        """
        Parse a single IKEA Hacks article page.
        """
        item = IkeaHackItem()

        # ---- TITLE ----
        title = response.css("h1::text").get()
        if title:
            title = title.strip()
        item["title"] = title

        # ---- AUTHOR ----
        author = (
            response.css("a[rel='author']::text").get()
            or response.css(".author a::text").get()
            or response.css(".author::text").get()
        )
        if author:
            author = author.strip(" ·\n\t")
        item["author"] = author

        # ---- DATE ----
        date = response.css("time::attr(datetime)").get()
        if not date:
            date = response.css("time::text").get()
        if date:
            date = date.strip()
        item["date"] = date

        # ---- URL ----
        item["url"] = response.url

        # ---- CATEGORIES ----
        # categories = response.css("a[rel='category tag']::text").getall()
        # categories = [c.strip() for c in categories if c.strip()]
        # if not categories:
        #     categories = ["IKEA Hacks"]
        # item["categories"] = categories
        raw_categories = response.xpath(
            "//h1[1]/following::a[contains(@href, '/category/')][position()<=10]/text()"
        ).getall()
        categories = [c.strip() for c in raw_categories if c.strip()]

        # de-duplicate preserving order
        seen = set()
        unique_categories = []
        for c in categories:
            if c not in seen:
                seen.add(c)
                unique_categories.append(c)

        if not unique_categories:
            unique_categories = ["IKEA Hacks"]

        item["categories"] = unique_categories

        # ---- TAGS ----
        # tags = response.css("a[rel='tag']::text").getall()
        # tags = [t.strip() for t in tags if t.strip()]
        # item["tags"] = tags
        raw_tags = response.css(
            "a[rel='tag']::text, .cb-tags a::text, .post-tags a::text").getall()
        tags = [t.strip() for t in raw_tags if t.strip()]
        item["tags"] = tags

        # ---- IMAGE URL ----
        image_url = (
            response.css("article img::attr(src)").get()
            or response.css("meta[property='og:image']::attr(content)").get()
        )
        if image_url:
            image_url = response.urljoin(image_url)
        item["image_url"] = image_url

        # ---- CONTENT ----
        # Take all text nodes after the first <h1> (post title), stop before "NEXT: See more" / "Related Posts".
        text_after_h1 = response.xpath("//h1[1]/following::text()").getall()

        content_parts = []
        for t in text_after_h1:
            t = t.strip()
            if not t:
                continue
            if t.startswith("NEXT: See more") or t.startswith("Related Posts"):
                break
            content_parts.append(t)

        content = " ".join(content_parts)
        item["content"] = content if content else None

        # ---- EXCERPT ----
        if content:
            excerpt = content[:200] + "..." if len(content) > 200 else content
        else:
            excerpt = title
        item["excerpt"] = excerpt

        if title:
            self.logger.info(f" Scraped: {title[:60]}")
            yield item
        else:
            self.logger.warning(f"Skipped: no title for {response.url}")
