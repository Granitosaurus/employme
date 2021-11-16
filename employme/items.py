from lib2to3.pytree import Base
import string
from typing import Optional, List, Literal
from pydantic import BaseModel, validator

SpiderNames = Literal["stackoverflow", "wappalyzer", "article"]


class Knowledge(BaseModel):
    """Container for scraper's results"""
    skills: List[str]
    title: Optional[str]
    description: Optional[str]
    sources: Optional[List[str]]
    scraper: Optional[str]
    scraped_on: Optional[int]  # timestamp

    @staticmethod
    def normalize_skill(text: str) -> str:
        return "".join(c for c in text.lower() if c not in string.punctuation + ' ')

    @validator("skills")
    def lowercase_skills(cls, values):
        return [cls.normalize_skill(v) for v in values]


class Target(BaseModel):
    """scrape target container"""
    homepage: Optional[str]  # i.e. product.com
    job_listing: Optional[str]  # i.e. stackoverflow.com/job/123
    token: Optional[str]  # no function yet - for future proofing abuse
    sources: Optional[List[SpiderNames]]  # list of spiders to use for scraping these


class KnowledgeResult(BaseModel):
    """API scrape requests result container"""
    messages: List[str]  # mesages genereted by KnowledgeInterpreter
    data: List[Knowledge]
    start: int  
    end: int  
    elapsed: int 

