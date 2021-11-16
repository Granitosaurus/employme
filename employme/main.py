import asyncio
from datetime import datetime

from starlette.responses import FileResponse
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from employme.items import Target, KnowledgeResult
from employme.crawler import Crawler
from employme.interpreter import KnowledgeInterpreter


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:52330",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return FileResponse('employme/index.html')


@app.post("/scrape")
async def scrape_item(
    target: Target, data: bool = False, cache_max_age: int = 60 * 60 * 60
) -> KnowledgeResult:
    start = datetime.utcnow().timestamp()

    crawler = Crawler(cache_max_age=cache_max_age)
    tasks = []
    if target.homepage:
        tasks.append(crawler.scrape(target.homepage, restrict_to=["wappalyzer"]))
    if target.job_listing:
        tasks.append(crawler.scrape(target.job_listing, restrict_to=["article"]))
    
    found_knowledge = [item for results in await asyncio.gather(*tasks) for item in results]

    knowledge_interpreter = KnowledgeInterpreter()
    messages = list(knowledge_interpreter.interpret(found_knowledge))

    end = datetime.utcnow().timestamp()
    result = {
        "messages": messages,
        "start": start,
        "end": end,
        "elapsed": end - start,
    }
    if data:
        result["data"] = found_knowledge
    return result
