# GitHub Commit client

## Beschrijving
Dit project haalt GitHub commits op via een Command Line Interface (CLI) die is gebouwd met Django. Het gebruikt Redis om data tijdelijk op te slaan. Zo worden er minder API verzoeken gedaan naar GitHub en worden de(zelfde) resultaten sneller geladen. Er wordt automatisch getest met pytest bij elke push via GitHub Actions. Ook controleert het met Flake8 op codekwaliteit. 

## Functionaliteit

## Installatie

## Configuratie
Voor het opvragen van privé repositories is een GitHub Personal Access Token nodig. Deze token moet worden opgeslagen in een .env bestand.

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
