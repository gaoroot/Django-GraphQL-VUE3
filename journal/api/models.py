from django.db import models


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.CharField(max_length=100000)
    date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
