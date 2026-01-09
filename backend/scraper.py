import requests
from bs4 import BeautifulSoup
import re

def scrape_wikipedia(url: str):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        raise Exception(f"Failed to fetch URL: {e}")

    soup = BeautifulSoup(response.content, 'html.parser')

    # Title
    title_tag = soup.find('h1', id='firstHeading')
    title = title_tag.get_text().strip() if title_tag else "Unknown Title"

    # Content
    content_div = soup.find('div', id='mw-content-text')
    if not content_div:
        raise Exception("Could not find article content.")

    # Get all paragraphs for full text context (limit to first ~2000 words to avoid token limits if needed)
    paragraphs = content_div.find_all('p')
    full_text = "\n".join([p.get_text() for p in paragraphs])
    
    # Summary (first meaningful paragraph)
    summary = ""
    for p in paragraphs:
        text = p.get_text().strip()
        if len(text) > 50:
            summary = text
            break

    # Sections (h2 headlines)
    sections = []
    for h2 in content_div.find_all('h2'):
        span = h2.find('span', class_='mw-headline')
        if span:
            sections.append(span.get_text().strip())

    with open("scraped_debug.txt", "w", encoding="utf-8") as f:
        f.write(f"Title: {title}\n")
        f.write(f"Summary: {summary}\n")
        f.write("-" * 20 + "\n")
        f.write(full_text[:5000]) # Log first 5000 chars

    return {
        "title": title,
        "summary": summary,
        "text": full_text[:15000], # Limit text sent to LLM to avoid excessive usage/errors
        "sections": sections
    }
