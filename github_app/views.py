from rest_framework.decorators import api_view
from rest_framework.response import Response
from github_app.services import fetch_commits


@api_view(['GET'])
def fetch_commits_view(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    commits = fetch_commits(start_date=start_date, end_date=end_date)
    return Response(commits)
