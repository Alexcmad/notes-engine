"""
All OpenAI based code goes here
"""
import openai
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GPT_SECRET")
openai.api_key = api_key


def generate_keywords_from_term(search_term: str) -> dict:
    """
    :param search_term: The term to be searched
    :return: A list of keywords relevant to the search term
    """
    with open("static/keywords_context", "r") as file:
        context: str = file.read()
    generation_context: list[dict] = [{"role": "system", "content": context},
                                      {"role": "user", "content": search_term}]
    completion: dict = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=generation_context,
        temperature=0.2
    )
    str_terms: str = completion['choices'][0]['message']['content']
    list_terms: list = str_terms.split(', ')
    return {"term": search_term,
            "keywords": list_terms}


def generate_summary(keyword: str, search_term: str) -> dict:
    """
    Generates a summary of a keyword within the topic the search term
    :param keyword: Keyword to generate a summary about
    :param search_term: The original search term that the summary is being generated 'in terms of'
    :return:
    """
    context = f"Define {keyword} in under the topic {search_term}"
    generation_context: list[dict] = [
        {"role": "system", "content": "Your purpose is to generate definitions that summarize the topic in 250 words."},
        {"role": "user", "content": context}]

    completion: dict = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=generation_context,
        temperature=0.4
    )
    summary: str = completion['choices'][0]['message']['content']
    return {'search_term': search_term,
            'title': keyword,
            'summary': summary}


def generate_keywords_from_notes(notes: str) -> list:
    """
    :param notes: The text to be analyzed
    :return: A list of keywords relevant to the notes uploaded
    """
    with open("static/keywords_context_notes", "r") as file:
        context: str = file.read()
    if len(notes) > 500:
        notes = notes[:499]
    generation_context: list[dict] = [{"role": "system", "content": context},
                                      {"role": "user", "content": notes}]
    completion: dict = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=generation_context,
        temperature=0
    )
    str_terms: str = completion['choices'][0]['message']['content']
    list_terms: list = str_terms.split(', ')
    return list_terms
