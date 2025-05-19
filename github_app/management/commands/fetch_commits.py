from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from github_app.github_client import fetch_and_group_commits
from github_app.cache_handler import get_cached_commits


class Command(BaseCommand):
    help = "GitHub commits ophalen binnen een bepaalde tijd en groepeer deze per auteur."

    # Repository, startdatum, einddatum benodigd. Branch optioneel.
    # Voorbeeld python manage.py fetch_commits Alteza/uitdaging 2025-05-15 2025-05-19
    def add_arguments(self, parser):
        parser.add_argument("repository", type=str, help="Bijv. Alteza/uitdaging")
        parser.add_argument("start_date", type=str, help="Formaat: YYYY-MM-DD")
        parser.add_argument("end_date", type=str, help="Formaat: YYYY-MM-DD")
        parser.add_argument("--branch", type=str, default="main", help="Branch (default: main)")

    def handle(self, *args, **options):
        # String proberen om te zetten naar datumobject, anders ValueError.
        try:
            start_date = datetime.strptime(options["start_date"], "%Y-%m-%d").date()
            end_date = datetime.strptime(options["end_date"], "%Y-%m-%d").date()
        except ValueError as e:
            raise CommandError(f"Fout in datumformaat: {e}. Gebruik het formaat YYYY-MM-DD.")

        if start_date > end_date:
            raise CommandError("Startdatum mag niet later zijn dan einddatum.")

        # Aanmaken sleutel voor caching.
        cache_key = f"{options['repository']}_{start_date}_{end_date}_{options['branch']}"

        # Als data in cache zit, wordt die gebruikt. Anders data ophalen via GitHub API.
        try:
            data, duration, source = get_cached_commits(
                cache_key,
                lambda: fetch_and_group_commits(
                    repository=options["repository"],
                    start_date=str(start_date),
                    end_date=str(end_date),
                    branch=options["branch"],
                )
            )
        # Fouten weergeven bij errors.
        except Exception as e:
            self.stderr.write(f"{e}")
            return

        # Bericht weergeven
        for author, info in data.items():
            self.stdout.write(f"\nAuteur: {author}, ({info['count']} commits)")
            for message in info["messages"]:
                self.stdout.write(f"- {message}")

        # Data uit cache of API en geeft de verstreken tijd aan.
        source_str = "cache" if source == "cache" else "API"
        self.stdout.write(
            self.style.SUCCESS(
                f"\nData opgehaald via {source_str} in {duration:.2f} milliseconden."))
