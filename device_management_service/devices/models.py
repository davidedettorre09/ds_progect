from django.db import models

class Device(models.Model):
    description = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    max_hourly_consumption = models.FloatField()
    owner_id = models.IntegerField()  # Questo campo sarà popolato dal token JWT

    def __str__(self):
        return self.description
