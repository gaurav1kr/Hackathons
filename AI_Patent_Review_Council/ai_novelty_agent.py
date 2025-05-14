# ai_novelty_agent.py

import os
import requests
from difflib import SequenceMatcher

SERP_API_KEY = os.getenv("SERP_API_KEY")  # Set this in your environment variables
GOOGLE_PATENT_SEARCH_URL = "https://serpapi.com/search.json"

class PatentNoveltyAgent:
    def __init__(self, api_key=SERP_API_KEY):
        self.api_key = api_key

    def search_google_patents(self, query):
        params = {
            "engine": "google_patents",
            "q": query,
            "api_key": self.api_key
        }
        response = requests.get(GOOGLE_PATENT_SEARCH_URL, params=params)
        if response.status_code == 200:
            return response.json().get("organic_results", [])
        else:
            return []

    def evaluate_novelty(self, proposal_title, proposal_description):
        search_results = self.search_google_patents(proposal_title)

        for result in search_results:
            title_similarity = SequenceMatcher(None, proposal_title.lower(), result.get("title", "").lower()).ratio()
            desc_similarity = SequenceMatcher(None, proposal_description.lower(), result.get("snippet", "").lower()).ratio()

            if title_similarity > 0.6 or desc_similarity > 0.6:
                return "Reject", f"Found similar patent: {result.get('title')} (Similarity Score: {max(title_similarity, desc_similarity):.2f})"

        return "Approve", "No close matches found in Google Patents search."
