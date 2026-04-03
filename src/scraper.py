from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin, urlparse

headers = { 
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def fetch_website_contents(url, base_url=None):
    """
    Return the title and content of the website at the given url:
    truncate to 2000 characters as a sesnible limit
    If base_url is set, relative urls (e.g. /about) are resolved against it.
    Non-http(s) URLs (mailto:, unresolved relative paths, etc.) return a short placeholder.
    """
    if base_url is not None and urlparse(url).scheme not in ("http", "https"):
        url = urljoin(base_url, url)
    if urlparse(url).scheme not in ("http", "https"):
        return (
            "No title found\n\n"
            f"(Skipped non-HTTP URL after resolve: {url[:120]})\n"
        )[:2_000]
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.title.string if soup.title else "No title found"
    if soup.body:
        for irrelevant in soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()
        text = soup.body.get_text(separator="\n", strip=True)
    else:
        text = ""
    return (title + "\n\n" + text)[:2_000]


def fetch_website_links(url):
    """
    Return the links on the webiste at the given url
    I realize this is inefficient as we're parsing twice! This is to keep the code in the lab simple.
    Feel free to use a class and optimize it!
    Hrefs are normalized to absolute http(s) URLs so downstream prompts and models see full URLs.
    """
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    out = []
    for link in soup.find_all("a"):
        href = link.get("href")
        if not href:
            continue
        absolute = urljoin(url, href)
        if urlparse(absolute).scheme in ("http", "https"):
            out.append(absolute)
    return out

