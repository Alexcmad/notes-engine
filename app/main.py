"""
The main driver code of the app (solution) goes here
FASTAPI stuff
"""
import os

from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from . import wiki, openAI, file_reader, schemas


app = FastAPI()
app.mount("/../static", StaticFiles(directory="static"))


@app.get('/')
def root() -> dict:
    return {"status": "working"}


@app.get('/wiki/{term}', response_model=schemas.Wiki)
def wiki_search(search_term: str) -> dict:
    """

    :param search_term:
    :return: A json object containing the url, name, and summary of the seaerch term
    """
    wiki_data: dict = wiki.wiki_search(search_term)
    return wiki_data


@app.get('/generate/terms/{term}', response_model=schemas.Keywords)
def generate_terms(search_term: str) -> dict:
    """

    :param search_term: The term being used to generate keywords
    :return: A json object containing a list of 10 keywords related to the search term
    """
    generated_terms: dict = openAI.generate_keywords(search_term)
    return generated_terms


@app.post('/upload', response_model=schemas.FileContent)
def upload_file(file: UploadFile) -> dict:

    """

    :param file: the file to be uploaded
    :return: A Json object containing the content of the file
    """

    ext: str = file.filename.split(".")[1]

    extension_dict: dict ={
        "pdf": file_reader.read_pdf,
        "docx": file_reader.read_docx,
        "doc": file_reader.read_docx,
        "txt": file_reader.read_txt
    }

    with open(file.filename, "wb") as f:
        f.write(file.file.read())
    response: dict = extension_dict.get(ext)(file.filename)
    os.remove(file.filename)
    return response
