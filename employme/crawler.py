from ast import parse
import asyncio
from datetime import datetime
import json
from typing import List, Literal, Type, Optional
from urllib.parse import urlparse

from employme.items import Knowledge, SpiderNames
from employme.spiders import (
    ArticleSpider,
    WappalyzerSpider,
    StackoverflowSpider,
    Spider,
)

from redis import Redis
from loguru import logger as log


class Crawler:
    """
    Spider manager that runs spiders and implements caching
    """

    spiders = [
        StackoverflowSpider,
        ArticleSpider,
        WappalyzerSpider,
    ]

    def __init__(self, cache_kwargs=None, cache_max_age=60 * 60 * 60) -> None:
        self.redis = Redis(**(cache_kwargs or {}), decode_responses=True)
        self.cache_max_age = cache_max_age

    def process_query(self, query):
        """
        Process crawler input into query for spiders
        Since spiders urls as query
        """
        parsed = urlparse(query)
        # no netloc and no scheme -> means it's a domain.com
        if not parsed.scheme and not parsed.netloc:
            if parsed.path:
                query = f"http://{query}"
        # XXX: more url normalization here would be great
        query = query.strip("/")
        return query

    async def scrape(
        self, query: str, restrict_to: List[Literal[SpiderNames]] = None
    ) -> List[Knowledge]:
        """
        Initiate scrape for selected Spiders

        Parameters
        ----------
        query : str
            query to pass to spiders
        restrict_to : List[Literal[SpiderNames]], optional
            restrict scrape to specific spiders, by default None will impose no restrictions

        Returns
        -------
        knowledge:
            all knowledge data collected from used spiders
        """
        query = self.process_query(query)
        tasks = []
        for spider in self.spiders:
            if restrict_to and spider.name not in restrict_to:
                continue
            log.info(f"scheduling spider {spider.name} for {query}")
            tasks.append(self._scrape(spider, query))
        found_knowledge = [
            item for results in await asyncio.gather(*tasks) for item in results
        ]
        for kn in found_knowledge:
            kn.scraped_on = int(datetime.utcnow().timestamp())
        return found_knowledge

    async def _scrape(self, spider_cls: Type[Spider], query: str) -> List[Knowledge]:
        """cache/output wrapper for spider scrape function"""
        cache = self.get_cache(spider_cls, query)
        if cache is not None:
            return cache
        async with spider_cls() as scraper:
            found_knowledge = await scraper.scrape(query)
        if found_knowledge:
            self.set_cache(scraper, query, found_knowledge)
        return found_knowledge

    def set_cache(self, spider: SpiderNames, query: str, data: List[Knowledge]) -> int:
        """Cache Knowledge returned by spider+query combo"""
        data = {
            "date": datetime.utcnow().timestamp(),
            "knowledge": [d.dict() for d in data],
        }
        return self.redis.set(f"{spider.name}:{query}", json.dumps(data))

    def get_cache(self, spider: SpiderNames, query: str) -> Optional[List[Knowledge]]:
        """
        Retrieve Knowledge Cache of a spider+query combo
        Returns either a list of cached items or None if no cache exists
        """
        data = self.redis.get(f"{spider.name}:{query}")
        if data:
            data = json.loads(data)
            _now = datetime.utcnow()
            if (_now.timestamp() - data["date"]) < self.cache_max_age:
                return [Knowledge.parse_obj(d) for d in data["knowledge"]]
        return None
