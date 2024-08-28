from django.db import models
class Store(models.Model):
    store_id = models.CharField(max_length=100, unique=True)
    timezone_str = models.CharField(max_length=50, default='America/Chicago')

class BusinessHour(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    day_of_week = models.IntegerField()  # 0 = Monday, 6 = Sunday
    start_time_local = models.TimeField()
    end_time_local = models.TimeField()

class StoreStatus(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    timestamp_utc = models.DateTimeField()
    status = models.CharField(max_length=50)

class Report(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    report_id = models.CharField(max_length=100, unique=True)
    uptime_last_hour = models.FloatField(default=0.0)  # in minutes
    uptime_last_day = models.FloatField(default=0.0)   # in hours
    uptime_last_week = models.FloatField(default=0.0)  # in hours
    downtime_last_hour = models.FloatField(default=0.0)  # in minutes
    downtime_last_day = models.FloatField(default=0.0)   # in hours
    downtime_last_week = models.FloatField(default=0.0)  # in hours
    status = models.CharField(max_length=50, default='Running')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    csv_file = models.FileField(upload_to='reports/', null=True, blank=True)
