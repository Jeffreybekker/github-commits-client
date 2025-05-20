# GitHub Commit client

## Beschrijving
Dit project haalt GitHub commits op via een Command Line Interface (CLI) die is gebouwd met Django. Het gebruikt Redis om data tijdelijk op te slaan. Zo worden er minder API verzoeken gedaan naar GitHub en worden de(zelfde) resultaten sneller geladen. Er wordt automatisch getest met pytest bij elke push via GitHub Actions. Ook controleert het met Flake8 op codekwaliteit. Verder is het project makkelijk te runnen via Docker.

## Functionaliteit

## Installatie
1. **Clone de repository**
```
git clone https://github.com/Jeffreybekker/github-commits-client.git
```
2. **Maak een .env bestand aan**
Je moet hiervoor een .env-bestand aanmaken.<br>
Meer informatie hoe je dit doet te vinden in configuratie.
```
GITHUB_TOKEN = JOUW_TOKEN
```
3. **Installeer Docker**
Docker is te installeren via https://www.docker.com/products/docker-desktop/.<br>
4. **Start de containers**
Bouw de app op in docker:
```
docker compose up --build
```
Na deze stap kan je de CLI commands runnen.

## Configuratie
Voor het opvragen van privé repositories is een GitHub Personal Access Token nodig. Deze token moet worden opgeslagen in een .env-bestand.

1. Maak een GitHub token aan:
    https://github.com/settings/tokens<br>
    Klik op **Generate new token** en dan **Generate new token (classic)**<br>
    Minimaal aanvinken:
    - repo
2. Maak een .env-bestand aan in de root van het project (hier staat ook manage.py).
```
GITHUB_TOKEN = JOUW_NET_AANGEMAAKTE_TOKEN
```
Zonder deze token kan de applicatie alleen worden gebruikt voor publieke repositories.

## Docker

## Tests Runnen

## CLI Gebruik
De datums zijn in YYYY-MM-DD format.<br>
Branch is optioneel, met default main.<br>
Dit command run je in docker.<br>
Command:
```
docker compose exec web python manage.py fetch_commits <repository> <start_date> <end_date> [--branch=branch_name]
```
Bijvoorbeeld:
```
docker compose exec web python manage.py fetch_commits Jeffreybekker/github-commits-client 2025-05-19 2025-05-20 --branch=main
```
