from hashlib import blake2b
from django.db import models

class Domain(models.Model):
    hash_value = models.CharField(
        max_length=32, blank=False, null=False, unique=True)
    title = models.CharField(max_length=50)
    sitemap = models.CharField(max_length=100, default='')
    description = models.TextField()
    created_at = models.DateTimeField(null=True)
    last_updated_at = models.DateTimeField(null=True)
    total_urls = models.IntegerField()

    def save(self, *args, **kwargs):
        super(Domain, self).save(*args, **kwargs)
        if not self.hash_value:
            self.hash_value = blake2b(
                key=type(self).__name__.lower().encode(), digest_size=16)
            self.hash_value.update(str(self.id).encode())
            self.hash_value = self.hash_value.hexdigest()
            self.save(update_fields=['hash_value'])




class Url(models.Model):
    hash_value = models.CharField(
        max_length=32, blank=False, null=False, unique=True)
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=1000)
    has_insights = models.BooleanField(default=False)
    last_updated_at = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        super(Url, self).save(*args, **kwargs)
        if not self.hash_value:
            self.hash_value = blake2b(
                key=type(self).__name__.lower().encode(), digest_size=16)
            self.hash_value.update(str(self.id).encode())
            self.hash_value = self.hash_value.hexdigest()
            self.save(update_fields=['hash_value'])

