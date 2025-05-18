import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from github_app import services

@pytest.mark.django_db
def test_commits_fetch_and_cache(monkeypatch):
    client = APIClient()

    fake_commits = [{"sha": "abc123", "commit": {"message": "Test commit"}}]

    def mock_fetch_commits(*args, **kwargs):
        return fake_commits

    monkeypatch.setattr(services, "fetch_commits", mock_fetch_commits)

    url = reverse("fetch_commits")

    response = client.get(url + "?start_date=2025-01-01&end_date=2025-01-31")
    assert response.status_code == 200
    assert response.json() == fake_commits
