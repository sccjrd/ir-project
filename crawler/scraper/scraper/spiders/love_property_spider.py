import scrapy
from scraper.items import IkeaHackItem


class LovePropertySpider(scrapy.Spider):
    name = "loveproperty"
    allowed_domains = ["loveproperty.com"]
    start_urls = [
        "https://www.loveproperty.com/gallerylist/75470/genius-ikea-hacks-for-every-room"
    ]

    # Words that indicate junk/non-content items
    JUNK_KEYWORDS = [
        "store and/or access",
        "advertising",
        "personalised",
        "privacy",
        "consent",
        "cookie",
        "gdpr",
        "data",
        "profiles",
        "measure",
        "understand audiences",
        "develop and improve",
        "security",
        "fraud",
        "deliver and present",
        "communicate privacy",
        "match and combine",
        "link different devices",
        "identify devices",
    ]

    def is_junk_title(self, title: str) -> bool:
        """Check if title contains junk/privacy policy keywords."""
        if not title:
            return True
        title_lower = title.lower()
        return any(keyword in title_lower for keyword in self.JUNK_KEYWORDS)

    def parse(self, response):
        """
        Parse gallery/listicle page. Each gallery item / slide becomes one IkeaHackItem.
        If we find no slides, fall back to parsing as a single long-form article.
        """
        # Try multiple gallery/slide selectors
        gallery_items = response.css("div.gallery-item")
        if not gallery_items:
            gallery_items = response.css("article.gallery-slide")
        if not gallery_items:
            gallery_items = response.css("div.slide")
        if not gallery_items:
            # last resort: any div with h2/h3 inside
            gallery_items = response.css("div:has(h2), div:has(h3)")

        self.logger.info(
            f"[loveproperty] Found {len(gallery_items)} potential gallery items on: {response.url}"
        )

        # Page-level author/date (same for all slides)
        author = (
            response.css("span.author::text").get()
            or response.css(".author a::text").get()
            or "Love Property"
        )
        date = (
            response.css("time::attr(datetime)").get()
            or response.css(
                'meta[property="article:published_time"]::attr(content)'
            ).get()
        )

        if len(gallery_items) == 0:
            self.logger.info(
                "[loveproperty] No gallery items found, treating as single article"
            )
            item = self.parse_single_article(response)
            if item:
                yield item
        else:
            scraped_count = 0
            seen_titles = set()

            for idx, section in enumerate(gallery_items[:50]):
                title = (
                    section.css("h2::text").get()
                    or section.css("h3::text").get()
                    or section.css("h4::text").get()
                )
                if title:
                    title = title.strip()
                else:
                    continue

                # Skip junk / cookie-banner-like slides
                if self.is_junk_title(title):
                    self.logger.debug(
                        f"[loveproperty] Skipping junk item: {title[:50]}"
                    )
                    continue

                # Skip duplicate titles
                if title in seen_titles:
                    continue
                seen_titles.add(title)

                paragraphs = section.css("p::text").getall()
                content = " ".join(p.strip() for p in paragraphs if p.strip())

                # Skip if no real content
                if not content or len(content) < 50:
                    continue

                image = (
                    section.css("img::attr(src)").get()
                    or section.css("img::attr(data-src)").get()
                )

                item = IkeaHackItem()
                item["source"] = "loveproperty"
                item["title"] = title
                item["content"] = content
                item["author"] = author
                item["date"] = date
                item["url"] = response.url + f"#slide-{idx+1}"
                item["categories"] = ["ikea-hacks", "home-improvement"]
                item["tags"] = ["ikea", "hack", "diy", "home"]
                item["image_url"] = image

                excerpt = (
                    content[:200] + "..." if len(content) > 200 else content
                )
                item["excerpt"] = excerpt

                scraped_count += 1
                self.logger.info(
                    f"[loveproperty] - Scraped gallery item: {title[:60]}"
                )
                yield item

            self.logger.info(
                f"[loveproperty] Scraped {scraped_count} valid items (filtered junk/short slides)"
            )

        # Optionally follow a few related IKEA articles on the same site
        related_links = response.css('a[href*="ikea"]::attr(href)').getall()
        related_links = [
            link
            for link in related_links
            if "/gallery" in link or "/article" in link
        ]
        related_links = list(set(related_links))[:5]

        for link in related_links:
            full_url = response.urljoin(link)
            if full_url != response.url:
                self.logger.info(
                    f"[loveproperty] Following related article: {full_url}"
                )
                yield scrapy.Request(full_url, callback=self.parse)

    def parse_single_article(self, response):
        """Parse a single long-form article (fallback)."""
        item = IkeaHackItem()

        title = response.css("h1::text").get() or response.css(
            "title::text"
        ).get()
        if title:
            title = title.strip()
        item["title"] = title

        paragraphs = (
            response.css("article p::text").getall()
            or response.css("div.content p::text").getall()
            or response.css("p::text").getall()
        )
        content = " ".join(p.strip() for p in paragraphs if p.strip())
        item["content"] = content

        author = response.css("span.author::text").get() or "Love Property"
        date = (
            response.css("time::attr(datetime)").get()
            or response.css(
                'meta[property="article:published_time"]::attr(content)'
            ).get()
        )

        item["author"] = author
        item["date"] = date
        item["url"] = response.url
        item["categories"] = ["ikea-hacks", "home-improvement"]
        item["tags"] = ["ikea", "hack", "diy", "home"]

        image_url = response.css(
            'meta[property="og:image"]::attr(content)'
        ).get() or response.css("article img::attr(src)").get()
        item["image_url"] = image_url

        if content:
            excerpt = (
                content[:200] + "..." if len(content) > 200 else content
            )
        else:
            excerpt = None
        item["excerpt"] = excerpt or title

        if title and not self.is_junk_title(title):
            self.logger.info(
                f"[loveproperty] - Scraped single article: {title[:60]}"
            )
            return item

        self.logger.warning(
            f"[loveproperty] Skipped single article (no title or junk): {response.url}"
        )
        return None
