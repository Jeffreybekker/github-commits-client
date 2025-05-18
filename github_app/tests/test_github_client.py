import pytest
from unittest.mock import patch, MagicMock
import requests
from github_app.github_client import fetch_and_group_commits  # pas aan naar jouw import


@patch("github_app.github_client.time.sleep", return_value=None)
@patch("github_app.github_client.requests.get")
def test_rate_limit_handling(mock_get, mock_sleep):
    # Mock 429 response met Retry-After
    response_429 = MagicMock()
    response_429.status_code = 429
    response_429.headers = {"Retry-After": "1"}
    response_429.json.return_value = []

    # Mock 200 response pagina 1 met commits
    response_200_page1 = MagicMock()
    response_200_page1.status_code = 200
    response_200_page1.json.return_value = [{
        "commit": {
            "author": {"name": "Auteur 1"},
            "message": "Bericht 1"
        }
    }]

    # Mock 200 response pagina 2 met commits
    response_200_page2 = MagicMock()
    response_200_page2.status_code = 200
    response_200_page2.json.return_value = [{
        "commit": {
            "author": {"name": "Auteur 2"},
            "message": "Bericht 2"
        }
    }]

    # Mock 200 response lege pagina (stoppen)
    response_empty = MagicMock()
    response_empty.status_code = 200
    response_empty.json.return_value = []

    # Zet side_effect zodat elke call iets teruggeeft
    mock_get.side_effect = [
        response_429,        # 1e call: rate limit
        response_200_page1,  # 2e call: pagina 1
        response_200_page2,  # 3e call: pagina 2
        response_empty       # 4e call: lege pagina -> stop loop
    ]

    result = fetch_and_group_commits("django/django", "2025-01-01", "2025-01-02")

    # Check dat de data correct is gegroepeerd
    assert "Auteur 1" in result
    assert result["Auteur 1"]["count"] == 1
    assert "Bericht 1" in result["Auteur 1"]["messages"]

    assert "Auteur 2" in result
    assert result["Auteur 2"]["count"] == 1
    assert "Bericht 2" in result["Auteur 2"]["messages"]

    # Check dat time.sleep werd aangeroepen met 1 (Retry-After)
    mock_sleep.assert_called_with(1)


@patch("github_app.github_client.requests.get")
def test_unauthorized_token(mock_get):
    response_401 = MagicMock()
    response_401.status_code = 401
    response_401.text = "Bad credentials"
    mock_get.return_value = response_401

    with pytest.raises(Exception, match="Unauthorized: Controleer of je toegangstoken geldig is."):
        fetch_and_group_commits("dummy/repo", "2025-01-01", "2025-01-02")


@patch("github_app.github_client.requests.get")
def test_repo_not_found(mock_get):
    response_404 = MagicMock()
    response_404.status_code = 404
    response_404.text = "Not Found"
    mock_get.return_value = response_404

    with pytest.raises(
            Exception, match="Repository niet gevonden: Controleer of de repo-naam klopt."):
        fetch_and_group_commits("dummy/repo", "2025-01-01", "2025-01-02")


@patch("github_app.github_client.requests.get")
def test_connection_error(mock_get):
    mock_get.side_effect = requests.exceptions.ConnectionError("Kan geen verbinding maken.")
    with pytest.raises(Exception, match="Verbindingsfout"):
        fetch_and_group_commits("dummy/repo", "2025-01-01", "2025-01-02")


@patch("github_app.github_client.requests.get")
def test_timeout_error(mock_get):
    mock_get.side_effect = requests.exceptions.Timeout("De aanvraag duurde te lang.")
    with pytest.raises(Exception, match="Timeout"):
        fetch_and_group_commits("dummy/repo", "2025-01-01", "2025-01-02")
