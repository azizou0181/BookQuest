from django.core.management.base import BaseCommand
from ingest.loader import run_ingestion

class Command(BaseCommand):
    help = 'Ingest documents'

    def handle(self, *args, **options):
        run_ingestion()