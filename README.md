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

## Running Tests
Tests are written using pytest<br>
To run tests inside Docker:<br>
```
docker compose exec web pytest
```
Make sure you activate your virtual environment and install the dependencies from requirements.txt:<br>
```
pytest
```

## CLI Gebruik
Dates must be in YYYY-MM-DD format.<br>
Branch is optional, with main as default.<br>
Run the command inside Docker.<br>
Command:
```
docker compose exec web python manage.py fetch_commits <repository> <start_date> <end_date> [--branch=branch_name]
```
Example:
```
docker compose exec web python manage.py fetch_commits Jeffreybekker/github-commits-client 2025-05-19 2025-05-20 --branch=main
```

## Example Outputs
**When data is fetched from the GitHub API:** <br>
![image](https://github.com/user-attachments/assets/fe4f9521-2864-4b8e-8f0f-9dc8e5bf2fa5)

**When data is fetched from the cache:** <br>
![image](https://github.com/user-attachments/assets/e90150b2-7e54-49d9-82b1-d7a2c937409f)

**When there's no network connection or the repository does not exist:** <br>
![image](https://github.com/user-attachments/assets/8d78a4e9-3e7a-42e3-a667-c69784ffb3a0)
