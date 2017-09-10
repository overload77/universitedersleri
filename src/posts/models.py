from django.db import models


# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(null=False, blank=True)
    content = models.TextField()
    category = models.CharField(max_length=50)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
