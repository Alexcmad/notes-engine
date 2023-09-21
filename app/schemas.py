from pydantic import BaseModel


class Keywords(BaseModel):
    term: str
    keywords: list


class Wiki(BaseModel):
    title: str
    url: str
    summary: str


class FileContent(BaseModel):
    filename: str
    content: str
    keywords: list


class GPTSummary(BaseModel):
    title: str
    summary: str
    search_term: str
