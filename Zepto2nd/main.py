from fastapi import FastAPI, HTTPException
import requests
from bs4 import BeautifulSoup
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
import os

app = FastAPI()

# Set up OpenAI API key
os.environ["OPENAI_API_KEY"] = "your-actual-api-key"  # Replace with actual key
llm = OpenAI(model="gpt-3.5-turbo")  # Specify the model

# Documentation sources
docs = {
    "segment": "https://segment.com/docs/",
    "mparticle": "https://docs.mparticle.com/",
    "lytics": "https://docs.lytics.com/",
    "zeotap": "https://docs.zeotap.com/home/en-us/"
}

# Improved Scrape documentation function
def fetch_docs(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return None
    soup = BeautifulSoup(response.text, "html.parser")
    text = " ".join([p.text.strip() for p in soup.find_all("p")])
    return text[:2000]  # Limit to 2000 chars for better API performance

@app.get("/ask")
def ask_cdp(question: str, platform: str):
    platform = platform.lower().strip()  # Fix extra spaces and uppercase issues
    
    if platform not in docs:
        raise HTTPException(status_code=400, detail="Invalid platform")
    
    doc_text = fetch_docs(docs[platform])
    if not doc_text:
        raise HTTPException(status_code=500, detail="Failed to fetch documentation")
    
    prompt = PromptTemplate(
        template="Answer this question based on the docs:\n{doc_text}\nQuestion: {question}",
        input_variables=["doc_text", "question"]
    )
    answer = llm(prompt.format(doc_text=doc_text, question=question))
    
    return {"answer": answer}

@app.get("/compare")
def compare_cdp(feature: str):
    comparison = {}
    for platform, url in docs.items():
        doc_text = fetch_docs(url)
        if doc_text:
            prompt = PromptTemplate(template="Find details about {feature} in this text:\n{doc_text}", 
                                    input_variables=["feature", "doc_text"])
            formatted_prompt = prompt.format(feature=feature, doc_text=doc_text)
            comparison[platform] = llm.invoke(formatted_prompt)
    return comparison
