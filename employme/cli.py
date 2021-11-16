import asyncio
from employme.scrapers.stackoverflow import StackOverflowJobsScraper

async def run():
    async with StackOverflowJobsScraper() as scraper:
        async for knowledge in scraper.scrape('nolk.com'):
            print(knowledge['title'], knowledge['skills'], knowledge['url'])


if __name__ == "__main__":
    scraper = StackOverflowJobsScraper()
    asyncio.run(run())
