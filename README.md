# GitHub Commit client

## Beschrijving

## Functionaliteit

## Installatie

## Configuratie
Voor het opvragen van privé repositories is een GitHub Personal Access Token nodig. Deze token moet worden opgeslagen in een .env bestand.

1. Maak een GitHub token aan:
    https://github.com/settings/tokens<br>
    Klik op **Generate new token** en dan **Generate new token (classic)**<br>
    Minimaal aanvinken:
    - repo
2. Maak een .env-bestand aan in de root van het project (hier staat ook manage.py in)
```
GITHUB_TOKEN = JOUW_NET_AANGEMAAKTE_TOKEN
```
Zonder deze token kan de applicatie alsnog worden gebruikt, maar alleen voor publieke repositories.

## Docker

## Tests Runnen

## CLI Gebruik
