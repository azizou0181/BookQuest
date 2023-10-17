from django.core.management.base import BaseCommand
from webapp.logic import main

class Command(BaseCommand):
    help = 'Ingest documents'

    def handle(self, *args, **options):
        main()
        self.stdout.write(self.style.SUCCESS('Documents ingested successfully.'))
