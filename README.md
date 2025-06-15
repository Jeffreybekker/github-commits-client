# GitHub Commit Client

## Description  
This project fetches GitHub commits via a Command Line Interface (CLI) built with Django.  
It uses Redis to temporarily store data, reducing the number of API requests to GitHub and improving performance for repeated results.  
Automated testing is performed using `pytest` on every push via GitHub Actions. The code is also checked with `Flake8` for quality.  
The project is easy to run using Docker.

## Features  
- Fetch commits from GitHub  
- Grouping by author  
- Caching with Redis  
- Command Line Interface (CLI)  
- Error handling  
- Docker support  
- Unit and integration tests  
- Code linting with Flake8  

## Installation  

1. **Clone the repository**  
```
git clone https://github.com/Jeffreybekker/github-commits-client.git
```
2. **Maak een .env bestand aan**<br>
Je moet hiervoor een .env-bestand aanmaken.<br>
Meer informatie hoe je dit doet is te vinden in [Configuratie](#configuratie).
```
GITHUB_TOKEN = JOUW_TOKEN
```
3. **Installeer Docker**<br>
Docker is te installeren via https://www.docker.com/products/docker-desktop/.<br>
4. **Start de containers**<br>
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

## Tests Runnen
De testen zijn gemaakt met pytest.<br>
Om dit te testen in Docker gebruik:<br>
```
docker compose exec web pytest
```
Voor het testen buiten Docker, moet je virtual environment gebruiken en zorgen dat al je depencies zijn geïnstalleerd die in de requirements.txt staan.<br>
```
pytest
```

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

**Dit krijg je te zien als de data wordt opgehaald vanuit de API:** <br>
![image](https://github.com/user-attachments/assets/fe4f9521-2864-4b8e-8f0f-9dc8e5bf2fa5)

**Dit krijg je te zien als de data wordt opgehaald vanuit de cache:** <br>
![image](https://github.com/user-attachments/assets/e90150b2-7e54-49d9-82b1-d7a2c937409f)

**Voorbeeld wat er gebeurd als er geen netwerkverbinding is of de repository niet bestaat:** <br>
![image](https://github.com/user-attachments/assets/8d78a4e9-3e7a-42e3-a667-c69784ffb3a0)
