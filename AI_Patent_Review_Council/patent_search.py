import difflib
import requests
from bs4 import BeautifulSoup
import urllib.parse

def search_google_patents(title, description, max_results=5):
    """
    Search Google Patents for existing patents matching the title + description.
    Returns: top_matches (list), max_score (float), error (None or str)
    """
    query = urllib.parse.quote_plus(f"{title} {description}")
    search_url = f"https://patents.google.com/?q={query}"
    
    try:
        response = requests.get(search_url, timeout=10)
        if response.status_code != 200:
            return [], 0, f"Failed to access Google Patents: Status {response.status_code}"
        
        soup = BeautifulSoup(response.content, 'html.parser')
        results = soup.select('search-result-item') or soup.select('tr[data-result]')  # fallback for some layouts
        matches = []

        seen_titles = set()
        for entry in results:
            link_tag = entry.find('a', href=True)
            if not link_tag:
                continue
            url = "https://patents.google.com" + link_tag['href']
            title_tag = entry.find('span', {'itemprop': 'title'})
            title_text = title_tag.get_text(strip=True) if title_tag else url.split("/")[-1]
            if title_text in seen_titles:
                continue
            seen_titles.add(title_text)

            sim_title = difflib.SequenceMatcher(None, title.lower(), title_text.lower()).ratio() * 100
            matches.append({
                "title": title_text,
                "url": url,
                "score": round(sim_title, 2)
            })

        matches = sorted(matches, key=lambda x: x["score"], reverse=True)
        top_matches = matches[:max_results]
        max_score = top_matches[0]["score"] if top_matches else 0
        return top_matches, max_score, None

    except Exception as e:
        return [], 0, f"Exception during search: {e}"
