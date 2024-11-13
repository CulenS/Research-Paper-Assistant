# model.py
import requests
from bs4 import BeautifulSoup
from transformers import pipeline, AutoModelForQuestionAnswering, AutoTokenizer

# Initialize the question-answering pipeline for extracting specific spans of text
tokenizer = AutoTokenizer.from_pretrained("deepset/bert-base-cased-squad2")
qa_model = AutoModelForQuestionAnswering.from_pretrained("deepset/bert-base-cased-squad2")
qa_pipeline = pipeline("question-answering", model=qa_model, tokenizer=tokenizer)

# Summarization model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def fetch_papers(query, max_results=5):
    """
    Fetch research papers from arXiv based on a query.
    
    Args:
    query (str): The topic of research.
    max_results (int): The number of papers to fetch.

    Returns:
    list: A list of dictionaries containing information about each paper.
    """
    base_url = "http://export.arxiv.org/api/query?"
    search_query = f"search_query=all:{query}&start=0&max_results={max_results}"
    response = requests.get(base_url + search_query)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, features="xml")
        papers = []
        entries = soup.find_all('entry')
        for entry in entries:
            paper_info = {
                "title": entry.title.text,
                "summary": entry.summary.text,
                "authors": [author.text for author in entry.find_all('author')],
                "published": entry.published.text
            }
            papers.append(paper_info)
        return papers
    else:
        return []

def summarize_paper(paper_summary):
    """
    Summarize the given paper summary text.

    Args:
    paper_summary (str): The summary text of the paper.

    Returns:
    str: A summarized version of the paper summary.
    """
    summary = summarizer(paper_summary, max_length=130, min_length=30, do_sample=False)
    return summary[0]['summary_text']

def answer_question_with_span(question, context):
    """
    Answer a question based on the context provided and highlight the exact part of the context.

    Args:
    question (str): The question to be answered.
    context (str): The context from which to derive the answer.

    Returns:
    dict: The answer and the exact span of text.
    """
    result = qa_pipeline(question=question, context=context)
    answer = result["answer"]
    start_index = result["start"]
    end_index = result["end"]
    exact_part = context[start_index:end_index]
    return {
        "answer": answer,
        "exact_part": exact_part
    }

def extract_key_information(papers):
    """
    Extract key information from multiple papers, such as contributions, methodology, and conclusions.

    Args:
    papers (list): List of dictionaries containing information about each paper.

    Returns:
    dict: A dictionary summarizing key information from all papers.
    """
    contributions = []
    methodologies = []
    conclusions = []

    for paper in papers:
        # Extract contributions, methodologies, and conclusions using simple keyword matching
        summary = paper['summary'].lower()
        if "contribution" in summary or "propose" in summary or "introduce" in summary:
            contributions.append(paper['summary'])
        if "method" in summary or "approach" in summary:
            methodologies.append(paper['summary'])
        if "conclude" in summary or "result" in summary or "find" in summary:
            conclusions.append(paper['summary'])

    return {
        "contributions": contributions,
        "methodologies": methodologies,
        "conclusions": conclusions
    }
