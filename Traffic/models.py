from re import T
from django.db import models
from django.conf import settings
from django.utils import timezone
import math
# Create your models here.

class Updates(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    author_username = models.CharField(blank=True,max_length=100000)
    long = models.DecimalField(max_digits=40,decimal_places=20)
    lang = models.DecimalField(max_digits=40,decimal_places=20)
    adress = models.TextField()
    localty = models.CharField(blank=True,max_length=100000)
    recommendations = models.TextField(blank=True,null=True)
    date_posted = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return 'update @ {}'.format(self.adress)

    def whenlast(self):
        now = timezone.now()
        
        diff= now - self.date_posted
        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds
            
            if seconds == 1:
                return str(seconds) +  "sec ago"
            
            else:
                return str(seconds) + " sec ago"

            

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + " min ago"
            
            else:
                return str(minutes) + " min ago"



        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " hr ago"

            else:
                return str(hours) + " hrs ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days
        
            if days == 1:
                return str(days) + " day ago"

            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)
            

            if months == 1:
                return str(months) + " month ago"

            else:
                return str(months) + " months ago"


        if diff.days >= 365:
            years= math.floor(diff.days/365)

            if years == 1:
                return str(years) + " year ago"

            else:
                return str(years) + " years ago"