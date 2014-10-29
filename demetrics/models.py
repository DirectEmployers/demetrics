from django.db import models

class DateMetric(models.Model):
    date = models.DateField()
    sessions = models.IntegerField(max_length=999999999)
    organic_searches = models.IntegerField(max_length=999999999)
    users = models.IntegerField(max_length=999999999)
    page_views = models.IntegerField(max_length=999999999)
    dotjobssite = models.ForeignKey('DotJobsSite')    

    def __unicode__(self):
        return str(self.date)

class DotJobsSite(models.Model):
    url = models.URLField()
    name = models.CharField(max_length=255)
    
    def __unicode__(self):
        return str(self.url)
