from django.core.management.base import BaseCommand
from forecasts.models import Ticker
import csv

class Command(BaseCommand):
    help = 'Import tickers from universe.csv into the Ticker model.'

    def handle(self, *args, **options):
        with open('universe.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0
            for row in reader:
                ticker, created = Ticker.objects.get_or_create(
                    ticker=row['ticker'],
                    defaults={'name': row['name']}
                )
                if not created:
                    ticker.name = row['name']
                    ticker.save()
                count += 1
            self.stdout.write(f'Successfully imported/updated {count} tickers.') 