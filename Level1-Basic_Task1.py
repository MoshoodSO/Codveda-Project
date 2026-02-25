#############################################################################
#### Task 1: Data Collection and Web Scraping
###### Description: Collect data from a website using web scraping techniques.
##############################################################################

# Import packages
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re
import requests
import time
import random


# URL path link
BASE_URL = "https://www.airlinequality.com/airline-reviews/ethiopian-airlines/"
PARAMS = {
    "sortby": "post_date:Desc",
    "pagesize": "10000"
}
HEADERS = {
    "User-Agent": "MyScraperBot/1.0 (contact: youremail@example.com)"
}

# function to get the page
def fetch_page(url, params=None):
    resp = requests.get(url, params=params, headers=HEADERS)
    resp.raise_for_status()
    return resp.text


# accessing the page
def parse_reviews(html):
    soup = BeautifulSoup(html, "html.parser")
    reviews = []

    # Each review begins with an h6 or h3 tag containing the title
    for header in soup.find_all(["h3", "h6"]):
        title = header.get_text(strip=True).strip('“”')
        entry = {"title": title}

        # The next sibling likely contains details and body
        next_node = header.find_next_sibling()
        text_chunks = []
        # Collect text until the next header tag
        while next_node and not next_node.name in ["h3", "h6"]:
            text_chunks.append(next_node.get_text(separator="\n", strip=True))
            next_node = next_node.find_next_sibling()
        text = "\n".join(text_chunks).strip()

        # Simple parsing: split by '|' if present
        parts = text.split("|", 1)
        if len(parts) == 2:
            entry["verified"] = parts[0].strip()
            content = parts[1].strip()
        else:
            entry["verified"] = None
            content = parts[0].strip()

        entry["content"] = content
        reviews.append(entry)

    return reviews

def main():
    html = fetch_page(BASE_URL, PARAMS)
    reviews = parse_reviews(html)

    # Optionally convert to DataFrame
    df = pd.DataFrame(reviews)
    print(df.head())
    df.to_csv("data/ethopian_airways_reviews.csv", index=False, encoding="utf-8")

if __name__ == "__main__":
    main()

# output
print("Operation performed successfully!!!")
# end of code

