from django.urls import path
from .views import fetch_commits_view

urlpatterns = [
    path('fetch_commits/', fetch_commits_view, name='fetch_commits'),
]
