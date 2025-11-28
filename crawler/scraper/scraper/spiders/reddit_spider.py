# scraper/scraper/spiders/reddit_spider.py

import json
from datetime import datetime

import scrapy
from scraper.items import IkeaHackItem


class RedditIkeaHacksSpider(scrapy.Spider):
    name = "reddit"
    allowed_domains = ["www.reddit.com", "reddit.com"]
    subreddit = "ikeahacks"

    max_posts = 500  # hard cap

    # Per-spider settings: ignore robots.txt for this spider only, and be gentle
    custom_settings = {
        "ROBOTSTXT_OBEY": False,
        "DOWNLOAD_DELAY": 2,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
    }

    custom_headers = {
        "User-Agent": "Mozilla/5.0 (compatible; IkeaHacksIR/1.0; +https://example.com)"
    }

    def start_requests(self):
        # start from newest posts
        self.post_count = 0
        url = f"https://www.reddit.com/r/{self.subreddit}/new.json?limit=100"
        yield scrapy.Request(url, headers=self.custom_headers, callback=self.parse)

    def parse(self, response):
        if self.post_count >= self.max_posts:
            self.logger.info(
                f"[reddit] Reached max_posts={self.max_posts}, stopping.")
            return

        data = json.loads(response.text)
        children = data.get("data", {}).get("children", [])

        self.logger.info(
            f"[reddit] Got {len(children)} posts from {response.url} "
            f"(total so far: {self.post_count})"
        )

        for child in children:
            if self.post_count >= self.max_posts:
                self.logger.info(
                    f"[reddit] Hit max_posts={self.max_posts} mid-page, not yielding more."
                )
                break

            post = child.get("data", {})

            item = IkeaHackItem()
            item["source"] = "reddit"

            # Title, URL, author
            item["title"] = post.get("title")
            item["url"] = "https://www.reddit.com" + post.get("permalink", "")
            item["author"] = post.get("author")

            # Date from UNIX timestamp
            created = post.get("created_utc")
            if created:
                item["date"] = datetime.utcfromtimestamp(
                    created).isoformat() + "Z"
            else:
                item["date"] = None

            # Categories & tags
            item["categories"] = ["reddit", self.subreddit]

            tags = []
            flair = post.get("link_flair_text")
            if flair:
                tags.append(flair)
            item["tags"] = tags

            # Text content (for text posts)
            selftext = (post.get("selftext") or "").strip()
            item["content"] = selftext or None

            # Image (if any)
            image_url = None
            if post.get("post_hint") in ("image", "link"):
                image_url = post.get(
                    "url_overridden_by_dest") or post.get("url")
            item["image_url"] = image_url

            # Excerpt
            if item["content"]:
                excerpt = item["content"][:200]
                if len(item["content"]) > 200:
                    excerpt += "..."
            else:
                excerpt = item["title"]
            item["excerpt"] = excerpt

            score = item.get("score", 0) 
            removed = item.get("removed_by_category")

            if item["title"] and removed is None and score >= 1:
                self.post_count += 1
                self.logger.info(
                    f"[reddit] - {item['title'][:60]} (total={self.post_count})"
                )
                yield item
            else:
                self.logger.info(
                    f"[reddit] - Skipping post "
                    f"(title={bool(item.get('title'))}, removed_by_category={removed}, score={score})"
                )    

        # Pagination with "after" cursor
        after = data.get("data", {}).get("after")
        if after and self.post_count < self.max_posts:
            next_url = (
                f"https://www.reddit.com/r/{self.subreddit}/new.json"
                f"?limit=100&after={after}"
            )
            self.logger.info(
                f"[reddit] Following after={after} (current total={self.post_count})"
            )
            yield scrapy.Request(
                next_url, headers=self.custom_headers, callback=self.parse
            )
        else:
            self.logger.info(
                f"[reddit] No more pages or reached max_posts={self.max_posts}. Done."
            )
