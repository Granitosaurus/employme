import re
from time import time
from requestr import Downloader


class Spider:
    name = NotImplemented

    def __init__(self) -> None:
        self.dl = Downloader(limit=1)
        self.stats = self.dl.stats

    async def __aenter__(self):
        await self.open()
        return self

    async def __aexit__(self, *args, **kwargs):
        await self.close()

    async def open(self):
        """populates startup stats"""
        self.stats["start"] = time()

    async def close(self):
        """calculate some end stats and close connections"""
        self.stats["end"] = time()
        self.stats["elapsed"] = self.stats["end"] - self.stats["start"]
        await self.dl.close()
    
    def url_from_query(self, query):
        if re.match("https*://.+", query):
            return query
        return f"https://{query}"


from employme.spiders.article import ArticleSpider
from employme.spiders.analyze import WappalyzerSpider
from employme.spiders.stackoverflow import StackoverflowSpider
