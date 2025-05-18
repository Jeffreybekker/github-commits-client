from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from github_app.github_client import fetch_and_group_commits
from github_app.cache_handler import get_cached_commits


class Command(BaseCommand):
    help = "Haal GitHub commits op binnen een tijdsperiode en groepeer deze per auteur."

    def add_arguments(self, parser):
        parser.add_argument("repository", type=str, help="Bijv. Alteza/uitdaging")
        parser.add_argument("start_date", type=str, help="Formaat: YYYY-MM-DD")
        parser.add_argument("end_date", type=str, help="Formaat: YYYY-MM-DD")
        parser.add_argument("--branch", type=str, default="main", help="Branch (default: main)")

    def handle(self, *args, **options):
        # Datumvalidatie
        try:
            start_date = datetime.strptime(options["start_date"], "%Y-%m-%d").date()
            end_date = datetime.strptime(options["end_date"], "%Y-%m-%d").date()
        except ValueError as e:
            raise CommandError(f"Fout in datumformaat: {e}. Gebruik het formaat YYYY-MM-DD.")

        if start_date > end_date:
            raise CommandError("Startdatum mag niet later zijn dan einddatum.")

        cache_key = f"{options['repository']}_{start_date}_{end_date}_{options['branch']}"

        try:
            data, duration, source = get_cached_commits(
                cache_key,
                lambda: fetch_and_group_commits(
                    repository=options["repository"],
                    start_date=str(start_date),  # naar string als je API dit verwacht
                    end_date=str(end_date),
                    branch=options["branch"],
                )
            )
        except Exception as e:
            self.stderr.write(f"{e}")
            return

        for author, info in data.items():
            self.stdout.write(f"\nAuteur: {author}, ({info['count']} commits)")
            for message in info["messages"]:
                self.stdout.write(f"- {message}")

        source_str = "cache" if source == "cache" else "API"
        self.stdout.write(
            self.style.SUCCESS(
                f"\nData opgehaald via {source_str} in {duration:.2f} milliseconden."))
