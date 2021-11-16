import json
import asyncio
from typing import List
from requestr import Request
from parsel import Selector
from employme.spiders import Spider

from employme.items import Knowledge


class StackoverflowSpider(Spider):
    name = "stackoverflow"
    url_search = "https://stackoverflow.com/jobs?q={query}".format
    url_listing = "https://stackoverflow.com/jobs/{job_id}".format

    def url_from_query(self, query):
        return self.url_search(query=query)

    async def scrape_job(self, job_id) -> Knowledge:
        url = self.url_listing(job_id=job_id)
        resp = await self.dl.send(Request(url))
        sel = Selector(resp.text)
        schema_items = sel.xpath('//script[@type="application/ld+json"]/text()')
        for item in schema_items:
            data = json.loads(item.get())
            if data["@type"] == "JobPosting":
                return Knowledge(
                    skills=data["skills"],
                    title=data["title"],
                    description=data["description"],
                    sources=[str(resp.url)],
                    scraper=self.name,
                )

    async def scrape_listing(self, query) -> List[str]:
        resp = await self.dl.send(Request(self.url_from_query(query)))
        sel = Selector(resp.text)
        return sel.xpath(
            '//div[@class="listResults"]//div[not(preceding-sibling::div[contains(@class, "bb")])]/@data-jobid'
        ).extract()

    async def scrape(self, query: str) -> List[Knowledge]:
        job_ids = await self.scrape_listing(query)
        if not job_ids:
            return
        found_knowledge = []
        for knowledge in asyncio.as_completed(
            [self.scrape_job(job_id) for job_id in job_ids]
        ):
            found_knowledge.append(await knowledge)
        return found_knowledge
