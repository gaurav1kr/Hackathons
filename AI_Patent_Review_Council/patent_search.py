from serpapi import GoogleSearch
import difflib

def search_google_patents(title, description, max_results=5):
    """
    Uses SerpAPI to search Google Patents and compute similarity scores.
    Returns (matches_list, match_count, error_message)
    """
    api_key = "1d7a2d0fa1a6ed0de7c28fbf5139ebb0fb261e3c4c5bf105d0b3976ea971b5b9"  # Replace with your actual SerpAPI key
    query = f"{title} {description} site:patents.google.com"

    try:
        search = GoogleSearch({
            "q": query,
            "api_key": api_key,
            "engine": "google",
            "num": max_results
        })
        results = search.get_dict()
        organic = results.get("organic_results", [])

        matches = []
        for item in organic:
            page_title = item.get("title", "Unknown Title")
            page_link = item.get("link", "")
            title_score = difflib.SequenceMatcher(None, title.lower(), page_title.lower()).ratio() * 100
            description_score = title_score  # Approximate since no snippet comparison
            avg_score = round((title_score + description_score) / 2, 2)

            matches.append({
                "title": page_title,
                "url": page_link,
                "score": avg_score
            })

        matches.sort(key=lambda x: x["score"], reverse=True)
        return matches, len(matches), None

    except Exception as e:
        return [], 0, str(e)
