from openai import OpenAI
from scraper import fetch_website_contents, fetch_website_links

OLLAMA_BASE_URL = "http://localhost:11434/v1"
MODEL = "llama3.2"

links = fetch_website_links("https://github.com/AnubhavDas651629/ai-brochure-generator/blob/main/src/agent.py")