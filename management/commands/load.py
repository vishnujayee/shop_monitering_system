# storedata/management/commands/load_data.py

import csv
from django.core.management.base import BaseCommand
from storedata.models import Store, BusinessHour

class Command(BaseCommand):
    help = 'Load store data from CSV files'

    def handle(self, *args, **kwargs):
        self.load_store_data()
        self.load_business_hours()
        self.load_timezones()

    def load_store_data(self):
        with open('../../data_source/store status.csv') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Store.objects.update_or_create(
                    store_id=row['store_id'],
                    defaults={'timezone_str': row.get('timezone_str', 'America/Chicago')}
                )

    def load_business_hours(self):
        with open('../../data_source/Menu hours.csv') as file:
            reader = csv.DictReader(file)
            for row in reader:
                store = Store.objects.get(store_id=row['store_id'])
                BusinessHour.objects.update_or_create(
                    store=store,
                    day_of_week=int(row['dayOfWeek']),
                    defaults={
                        'start_time_local': row['start_time_local'],
                        'end_time_local': row['end_time_local']
                    }
                )

    def load_timezones(self):
        with open('../../data_source//bq-results-20230125-202210-1674678181880.csv') as file:
            reader = csv.DictReader(file)
            for row in reader:
                store = Store.objects.get(store_id=row['store_id'])
                timezone_str = row.get('timezone_str', 'America/Chicago')
                Store.objects.update_or_create(
                    store_id=row['store_id'],
                    defaults={'timezone_str': timezone_str}
                )
