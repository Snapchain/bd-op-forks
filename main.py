import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# GitHub API endpoint for forks
API_URL = "https://api.github.com/repos/ethereum-optimism/optimism/forks"

# GitHub Personal Access Token
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def get_forks(url):
    forks = []
    page = 1
    while True:
        response = requests.get(
            f"{url}?page={page}",
            headers={"Authorization": f"token {GITHUB_TOKEN}"}
        )
        if response.status_code == 200:
            page_forks = response.json()
            if not page_forks:
                break
            forks.extend(page_forks)
            page += 1
        else:
            print(f"Error fetching forks: {response.status_code}")
            break
    return forks

def is_organization(fork):
    return fork['owner']['type'] == 'Organization'

def main():
    if not GITHUB_TOKEN:
        print("Please set your GitHub token as GITHUB_TOKEN in a .env file.")
        return

    print("Fetching forks...")
    all_forks = get_forks(API_URL)
    
    print(f"Total forks found: {len(all_forks)}")
    
    org_forks = [fork for fork in all_forks if is_organization(fork)]
    
    print(f"Forks by organizations: {len(org_forks)}")
    print("\nList of organizations that forked the repository:")
    for fork in org_forks:
        print(f"- {fork['owner']['login']} (URL: {fork['html_url']})")

if __name__ == "__main__":
    main()