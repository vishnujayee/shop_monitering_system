# storedata/tasks.py

import csv
import uuid
from datetime import datetime, timedelta
import pytz
from celery import shared_task
from django.core.files.base import ContentFile
from django.utils.timezone import make_aware
from .models import Store, Report, BusinessHour, StoreStatus

@shared_task
def update_store_status():
    with open('../shop/data_source/store status.csv') as file:
        reader = csv.DictReader(file)
        for row in reader:
            store = Store.objects.get(store_id=row['store_id'])
            timestamp_utc = make_aware(datetime.strptime(row['timestamp_utc'], '%Y-%m-%d %H:%M:%S'))
            StoreStatus.objects.update_or_create(
                store=store,
                timestamp_utc=timestamp_utc,
                defaults={'status': row['status']}
            )

@shared_task
def generate_report():
    report_id = str(uuid.uuid4())
    stores = Store.objects.all()
    report_data = []

    for store in stores:
        timezone = pytz.timezone(store.timezone_str)
        now_utc = datetime.utcnow()
        now_local = timezone.normalize(pytz.utc.localize(now_utc).astimezone(timezone))
        
        # Calculate uptime/downtime based on status in the database
        uptime_last_hour, downtime_last_hour = calculate_uptime_downtime(store, timezone, timedelta(hours=1))
        uptime_last_day, downtime_last_day = calculate_uptime_downtime(store, timezone, timedelta(days=1))
        uptime_last_week, downtime_last_week = calculate_uptime_downtime(store, timezone, timedelta(weeks=1))
        
        # Create report entry
        report = Report.objects.create(
            store=store,
            report_id=report_id,
            uptime_last_hour=uptime_last_hour,
            uptime_last_day=uptime_last_day,
            uptime_last_week=uptime_last_week,
            downtime_last_hour=downtime_last_hour,
            downtime_last_day=downtime_last_day,
            downtime_last_week=downtime_last_week,
            status='Running'
        )

        report_data.append([
            store.store_id,
            uptime_last_hour,
            uptime_last_day,
            uptime_last_week,
            downtime_last_hour,
            downtime_last_day,
            downtime_last_week
        ])

    # Generate CSV file
    csv_file = ContentFile('')
    writer = csv.writer(csv_file)
    writer.writerow(['store_id', 'uptime_last_hour', 'uptime_last_day', 'uptime_last_week', 'downtime_last_hour', 'downtime_last_day', 'downtime_last_week'])
    writer.writerows(report_data)
    
    final_report = Report.objects.filter(report_id=report_id).first()
    final_report.csv_file.save(f'report_{report_id}.csv', csv_file)
    
    Report.objects.filter(report_id=report_id).update(status='Complete')

    return report_id

def calculate_uptime_downtime(store, timezone, time_delta):
    now = datetime.utcnow()
    start_time_utc = now - time_delta

    # Convert UTC time to local time
    now_local = timezone.normalize(pytz.utc.localize(now).astimezone(timezone))
    start_time_local = timezone.normalize(pytz.utc.localize(start_time_utc).astimezone(timezone))

    # Get business hours for the store for the days in the time range
    business_hours = BusinessHour.objects.filter(store=store, day_of_week__in=[start_time_local.weekday(), now_local.weekday()])

    # If no business hours are found, assume the store is open 24/7
    if not business_hours.exists():
        return calculate_uptime_downtime_24_7(store, start_time_utc, now)

    active_minutes = 0
    inactive_minutes = 0

    for status in StoreStatus.objects.filter(store=store, timestamp_utc__range=[start_time_utc, now]):
        # Convert the status timestamp to local time
        status_time_local = timezone.normalize(pytz.utc.localize(status.timestamp_utc).astimezone(timezone))
        if is_during_business_hours(status_time_local, business_hours):
            if status.status == 'active':
                active_minutes += 1
            else:
                inactive_minutes += 1

    # Convert minutes to hours for day/week calculations
    if time_delta >= timedelta(days=1):
        return active_minutes / 60, inactive_minutes / 60
    return active_minutes, inactive_minutes

def calculate_uptime_downtime_24_7(store, start_time_utc, now_utc):
    statuses = StoreStatus.objects.filter(store=store, timestamp_utc__range=[start_time_utc, now_utc])
    active_minutes = sum(1 for status in statuses if status.status == 'active')
    inactive_minutes = sum(1 for status in statuses if status.status == 'inactive')
    return active_minutes, inactive_minutes

def is_during_business_hours(timestamp_local, business_hours):
    for bh in business_hours:
        if bh.start_time_local <= timestamp_local.time() <= bh.end_time_local:
            return True
    return False
