from django.conf import settings
from django.db import models

class News(models.Model):
    title = models.CharField(max_length=120)

    def __str__(self):
        return self.title