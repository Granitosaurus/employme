from fastapi import Query
from requestr import Request
from newspaper import Article

from employme.spiders import Spider
from employme.items import Knowledge


class ArticleSpider(Spider):
    name = "article"
    

    async def scrape(self, query) -> Knowledge:
        url = self.url_from_query(query)
        resp = await self.dl.send(Request(url))
        # Only parse self.page_limit amount urls rather than whole website
        article = Article(url, language="en")
        article.download(input_html=resp.text)
        article.parse()
        article.nlp()
        return [
            Knowledge(
                skills=article.keywords,
                title=article.title,
                description=article.text,
                sources=[str(resp.url)],
                scraper=self.name,
            )
        ]
