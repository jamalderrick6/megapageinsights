from django.db import models

class Domain(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()


class Url(models.Model):
    title = models.CharField(max_length=1000)

