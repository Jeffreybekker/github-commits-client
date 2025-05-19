import requests
import time
from dotenv import load_dotenv
import os

# Laden van .env bestand waar de token inzit.
load_dotenv()


# Haalt de data op, handelt bij errors en verwerkt data.
def fetch_and_group_commits(repository, start_date, end_date, branch="main", max_tries=3):
    url = f"https://api.github.com/repos/{repository}/commits"
    token = os.getenv("GITHUB_TOKEN")

    headers = {"Authorization": f"token {token}"} if token else {}
    params = {
        "sha": branch,
        "since": f"{start_date}T00:00:00Z",
        "until": f"{end_date}T23:59:59Z",
        "per_page": 100,
    }

    all_commits = []  # Hier worden de commits opgeslagen.
    page = 1  # Elke API call krijg een andere pagina.
    retries = 0  # Maximaal 3 retries, rate limiting.

    while True:
        params["page"] = page
        # Afhandelen netwerk errors.
        try:
            response = requests.get(url, params=params, headers=headers, timeout=10)
        except requests.exceptions.ConnectionError:
            raise Exception("Verbindingsfout: Kan geen verbinding maken met GitHub.")
        except requests.exceptions.Timeout:
            raise Exception("Timeout: GitHub duurde te lang om te antwoorden.")
        except requests.exceptions.RequestException as f:
            raise Exception(f"Onbekende netwerkfout: {f}")

        # Afhandelen HTTP errors.
        if response.status_code == 401:
            raise Exception("Unauthorized: Controleer of je toegangstoken geldig is.")

        elif response.status_code == 404:
            raise Exception("Repository niet gevonden: Controleer of de repo-naam klopt.")

        elif response.status_code == 429:
            retry_after = response.headers.get("Retry-After")
            wait_time = int(retry_after) if retry_after else 60
            print(f"Rate limit bereikt. Wacht {wait_time} seconden en probeer opnieuw...")
            time.sleep(wait_time)
            retries += 1
            if retries > max_tries:
                raise Exception("Max retries overschreden door rate limiting")
            continue

        # Elke andere error dan 200.
        elif response.status_code != 200:
            raise Exception(f"GitHub API error: {response.status_code} {response.text}")

        # Opgehaalde commits in all_commits plaatsen tot er geen commits meer zijn.
        commits = response.json()
        if not commits:
            break

        all_commits.extend(commits)
        page += 1
        retries = 0

    if not all_commits:
        return {}

    # Voor elke commit: haal auteur en bericht op.
    # Tel commits per auteur en verzamel de berichten.
    grouped = {}
    for commit in all_commits:
        auteur = commit.get("commit", {}).get("author", {}).get("name", "Niet beschikbaar")
        bericht = commit.get("commit", {}).get("message", "Niet beschikbaar")

        if auteur not in grouped:
            grouped[auteur] = {"count": 0, "messages": []}

        grouped[auteur]["count"] += 1
        grouped[auteur]["messages"].append(bericht)

    return grouped
