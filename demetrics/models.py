from django.db import models

class DateMetric(models.Model):
    date = models.DateField()
    sessions = models.IntegerField(max_length=999999999)
    organic_searches = models.IntegerField(max_length=999999999)
    users = models.IntegerField(max_length=999999999)
    page_views = models.IntegerField(max_length=999999999)
    dotjobssite = models.ForeignKey('DotJobsSite')    

    def __unicode__(self):
        return "%s - %s" % (self.dotjobssite, self.date)

class DotJobsSite(models.Model):
    url = models.URLField()
    name = models.CharField(max_length=255)
    google_analytics_account = models.ForeignKey('GoogleAnalyticsAccount')
    
    def __unicode__(self):
        return str(self.url)
        
class GoogleAnalyticsAccount(models.Model):
    account_id = models.CharField(max_length=25)
    account_name = models.CharField(max_length=255)
    
    def __unicode__(self):
        return "%s - %s" % (self.account_id,self.account_name)
