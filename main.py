from fastapi import FastAPI
import urllib.request
from bs4 import BeautifulSoup
import numpy as np
from sentence_transformers import SentenceTransformer, util
from datetime import datetime as dt

app = FastAPI()


def main():
    # ------------------------ Loading Data ------------------------
    model = SentenceTransformer("distilbert-base-nli-stsb-wkpooling")

    # Load data from ARXIV
    url = "http://export.arxiv.org/api/query?search_query=cat:cs.AI+AND+cs.CL&start=0&max_results=50&sortBy=submittedDate&sortOrder=descending"
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, "html.parser")

    titles_list = soup.find_all("title")
    dates_list = soup.find_all("updated")

    with open("favorited_papers.txt") as f:  # needs to be updated to work with Mendeley API
        sample_topics = f.readlines()

    """
    # This eventually could be updated to be more topically / involves knowledge graphs - keeping code 
    topics = {"question answering": [], "privacy and justice": [], "knowledge graph": []}
    topics_list = list(topics.keys())
    sentence_embeddings = model.encode(topics_list, convert_to_tensor=True)
    # topics[topics_list[greatest_index]] = title.string
    """

    sentence_embeddings = model.encode(
        sample_topics, convert_to_tensor=True
    )  # embed the previous papers list


    prospective_papers = []
    for title_date, title in zip(dates_list, titles_list):
        # if dt.today().date() == dt.strptime(title_date.string.split("T")[0], '%Y-%m-%d').date():  # check to make sure is published today
        if (
            dt(2020, 9, 24).date()
            == dt.strptime(title_date.string.split("T")[0], "%Y-%m-%d").date()
        ):  # for testing purposes
            query_embedding = model.encode(title.string, convert_to_tensor=True)
            cos_scor = util.pytorch_cos_sim(query_embedding, sentence_embeddings)
            cos_scor = cos_scor.cpu()
            greatest_index = np.argmax(cos_scor.numpy())
            if cos_scor[0][greatest_index] > 0.65:
                prospective_papers.append(title.string)

    return prospective_papers

@app.get("/")
async def root():
    return {"Hello!": "Navigate to /get_names"}

@app.get("/get_names")
async def return_names():
    return main()




    