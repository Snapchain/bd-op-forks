

import concurrent.futures
import os
from datetime import datetime, timedelta

import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# GitHub API endpoint for forks
API_URL = "https://api.github.com/repos/ethereum-optimism/optimism/forks"
# number of pages (# of forks / 100) 
NUM_PAGES = 31
# number of days since last update to consider a fork active
ACTIVE_THRESHOLD_IN_DAYS = 90

# Fetch forks asynchronously using threads
def get_forks(url):
    forks = []
    pages = range(1, NUM_PAGES + 1)
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(get_forks_page, url, page): page for page in pages}
        
        for future in concurrent.futures.as_completed(futures):
            page_forks = future.result()
            if page_forks:
                forks.extend(page_forks)

    return forks

# Fetch a single page of forks
def get_forks_page(url, page):
    response = requests.get(
        f"{url}?per_page=100&page={page}",
        headers={"Authorization": f"token {GITHUB_TOKEN}"}
    )
    if response.status_code == 200:
        page_forks = response.json()
        if not page_forks:
            return []
        return page_forks
    else:
        print(f"Error fetching page {page}: {response.status_code}")
        return []
    
# Filter functions
def is_organization(fork):
    return fork['owner']['type'] == 'Organization'

def is_not_organization(fork):
    return fork['owner']['type'] != 'Organization'

def is_active(fork):
    updated_at = datetime.strptime(fork["updated_at"], "%Y-%m-%dT%H:%M:%SZ")
    threshold = datetime.now() - timedelta(days=ACTIVE_THRESHOLD_IN_DAYS)
    return updated_at > threshold

def has_stars(fork):
    return fork["stargazers_count"] > 0

def forked_by_others(fork):
    return fork["forks_count"] > 0

def main():
    if not GITHUB_TOKEN:
        print("Please set your GitHub token as GITHUB_TOKEN in a .env file.")
        return

    # Fetch all forks.
    print("Fetching forks...")
    all_forks = get_forks(API_URL)
    print(f"Total forks found: {len(all_forks)}")
    
    # Filter for forks by organizations.
    forks = [fork for fork in all_forks if is_organization(fork)]
    print(f"Forks by organizations: {len(forks)}")

    # Filter for forks by individuals.
    # forks = [fork for fork in all_forks if is_not_organization(fork)]
    # print(f"Forks by individuals: {len(forks)}")

    # Filter for actively maintained forks.
    forks = [fork for fork in forks if is_active(fork)]
    print(f"Actively maintained forks: {len(forks)}")

    # Filter for forks with stars.
    # forks = [fork for fork in forks if has_stars(fork)]
    # print(f"Forks with stars: {len(forks)}")

    # Filter for forks that have been forked by others.
    forks = [fork for fork in forks if forked_by_others(fork)]
    print(f"Forks that have been forked by others: {len(forks)}")

    print("Filtered list of organizations:")
    for fork in forks:
        print(f"- {fork['owner']['login']} (URL: {fork['html_url']}) (Updated at: {fork['updated_at']})")

if __name__ == "__main__":
    main()