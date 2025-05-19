import pytest
from unittest.mock import patch, MagicMock
import requests
from github_app.github_client import fetch_and_group_commits


# Rate limiting testen
@patch("github_app.github_client.time.sleep", return_value=None)
@patch("github_app.github_client.requests.get")
def test_rate_limit_handling(mock_get, mock_sleep):
    # Status code 429 nabootsen
    response_429 = MagicMock()
    response_429.status_code = 429
    response_429.headers = {"Retry-After": "1"}
    response_429.json.return_value = []

    # Status code 200 nabootsen pagina 1 met een commit
    response_200_page1 = MagicMock()
    response_200_page1.status_code = 200
    response_200_page1.json.return_value = [{
        "commit": {
            "author": {"name": "Auteur 1"},
            "message": "Bericht 1"
        }
    }]

    # Status code 200 nabootsen pagina 2 met een commit
    response_200_page2 = MagicMock()
    response_200_page2.status_code = 200
    response_200_page2.json.return_value = [{
        "commit": {
            "author": {"name": "Auteur 2"},
            "message": "Bericht 2"
        }
    }]

    # Status code 200 nabootsen voor lege pagina. Stoppen loop.
    response_empty = MagicMock()
    response_empty.status_code = 200
    response_empty.json.return_value = []

    # Tests achter elkaar runnen met side_effect.
    mock_get.side_effect = [
        response_429,        # Rate limiting testen
        response_200_page1,  # Pagina 1 testen
        response_200_page2,  # Pagina 2 testen
        response_empty       # Lege pagina ophalen moet loop stoppen.
    ]

    result = fetch_and_group_commits("django/django", "2025-01-01", "2025-01-02")

    # Check data goed gegroepeerd
    assert "Auteur 1" in result
    assert result["Auteur 1"]["count"] == 1
    assert "Bericht 1" in result["Auteur 1"]["messages"]

    assert "Auteur 2" in result
    assert result["Auteur 2"]["count"] == 1
    assert "Bericht 2" in result["Auteur 2"]["messages"]

    # Controle of de functie 1 sec wacht na de 429 response
    mock_sleep.assert_called_with(1)


# Testen gebruik van ongeldige token (te vinden in .env) error 401
@patch("github_app.github_client.requests.get")
def test_unauthorized_token(mock_get):
    response_401 = MagicMock()
    response_401.status_code = 401
    response_401.text = "Bad credentials"
    mock_get.return_value = response_401

    # Controleerd ongeldige token door Exception met beschrijving te geven
    with pytest.raises(Exception, match="Unauthorized: Controleer of je toegangstoken geldig is."):
        fetch_and_group_commits("dummy/repo", "2025-01-01", "2025-01-02")


# Testen onvindbare repo error 404
@patch("github_app.github_client.requests.get")
def test_repo_not_found(mock_get):
    response_404 = MagicMock()
    response_404.status_code = 404
    response_404.text = "Not Found"
    mock_get.return_value = response_404

    # Controleerd niet gevonden repo door Exception met beschrijving te geven
    with pytest.raises(
            Exception, match="Repository niet gevonden: Controleer of de repo-naam klopt."):
        fetch_and_group_commits("dummy/repo", "2025-01-01", "2025-01-02")


# Testen of er verbinding is met ConnectionError
@patch("github_app.github_client.requests.get")
def test_connection_error(mock_get):
    mock_get.side_effect = requests.exceptions.ConnectionError("Kan geen verbinding maken.")
    with pytest.raises(Exception, match="Verbindingsfout"):
        fetch_and_group_commits("dummy/repo", "2025-01-01", "2025-01-02")


# Testen timeout
@patch("github_app.github_client.requests.get")
def test_timeout_error(mock_get):
    mock_get.side_effect = requests.exceptions.Timeout("De aanvraag duurde te lang.")
    with pytest.raises(Exception, match="Timeout"):
        fetch_and_group_commits("dummy/repo", "2025-01-01", "2025-01-02")
