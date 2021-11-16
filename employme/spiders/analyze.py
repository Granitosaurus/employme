import asyncio
import re
from collections import Counter
from itertools import islice
from typing import List

from employme.items import Knowledge
from employme.spiders import Spider
from loguru import logger as log
from requestr import Request, Response
from Wappalyzer import Wappalyzer, WebPage
from yarl import URL


class WappalyzerSpider(Spider):
    name = "wappalyzer"
    url_priority = re.compile("about|hire|app|blog|work|stack|technology|careers")

    def __init__(self, page_limit=5) -> None:
        super().__init__()
        self.wappalyzer = Wappalyzer.latest()
        self.page_limit = page_limit

    def extract_urls(self, resp: Response) -> List[str]:
        urls = set(u.split("#", 1)[0] for u in resp.tree.xpath("//a/@href").extract())
        priority = set()
        for url in urls:
            if self.url_priority.search(url):
                priority.add(url)
        to_follow = [resp.url.join(URL(path)) for path in priority]
        to_follow.extend(
            [resp.url.join(URL(path)) for path in urls.difference(priority)]
        )
        log.info(
            f"found {len(urls)} links on homepage; {len(to_follow)} can be followed"
        )
        # TODO: filter out "#fragments"
        for url in to_follow:
            if url == resp.url:
                continue
            if url.host == resp.url.host:
                yield url

    async def scrape(self, query) -> Knowledge:
        responses = [await self.dl.send(Request(self.url_from_query(query)))]
        log.info(f"analyzing tech stack of {query}, got {responses[0]}")
        # Only parse self.page_limit amount urls rather than whole website
        urls = list(islice(self.extract_urls(responses[0]), self.page_limit - 1))
        log.info(f"found {len(urls)} links to follow up")
        for resp_fut in asyncio.as_completed(
            [self.dl.send(Request(url)) for url in urls]
        ):
            responses.append(await resp_fut)

        total = Counter()
        for resp in responses:
            web_page = WebPage(str(resp.url), html=resp.text, headers=resp.headers)
            found = self.wappalyzer.analyze(web_page)
            total.update(found)
        log.info(f"found skills: {dict(total)}")
        return [
            Knowledge(
                skills=list(total.keys()),
                scraper=self.name,
                sources=[str(resp.url) for resp in responses],
            )
        ]
