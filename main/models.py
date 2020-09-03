from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Search(models.Model):
    search = models.CharField(max_length=200)
    search_date = models.DateTimeField("search date", default=timezone.now)
    slug = models.CharField(max_length=40, default=1)

    def __str__(self):
        return self.search