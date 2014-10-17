from django.db import models

class Metric(models.Model):
    date = models.DateField()
    sessions = models.IntegerField(max_length=999999999)
    visitors = models.IntegerField(max_length=999999999)
    unique_visitors = models.IntegerField(max_length=999999999)

    def __unicode__(self):
        return str(self.date)

