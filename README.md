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
2. **Create a .env-file in the root directory**<br>
More information about this at [Configuration](#configuration).
```
GITHUB_TOKEN = YOUR_TOKEN
```
3. **Install Docker**<br>
You can install Docker via https://www.docker.com/products/docker-desktop/.<br>
4. **Start the containers**<br>
Build the app in Docker:
```
docker compose up --build
```
After this step, you can run the CLI commands.

## Configuration
To access private repositories, a GitHub Personal Access Token is required. This token must be stored in a .env-file.

1. Generate a GitHub token:
    https://github.com/settings/tokens<br>
    Click on **Generate new token**, then **Generate new token classic**<br>
    At minimum, check:
    - repo
2. Greate a .env-file in the root of the project (where manage.py is located):
```
GITHUB_TOKEN = YOUR_RECENTLY_GENERATED_TOKEN
```
Without this token, the application can only be used for public repositories.

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
