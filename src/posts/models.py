from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save

from .utils import unique_slug_generator

# Create your models here.

# class PostQuerySet(models.query.QuerySet):
#     def search(self, query):        # Post.objects.all()"queryset".search()
#         if query is None or query=='':
#             return self
#         else:
#             query = query.strip()
#             return self.filter(Q(title__icontains=query) | Q(content__icontains=query)).distinct()

class PostManager(models.Manager):
    def search(self, query):   #Post.objects.search(query) ...
        if query is None or query=='':
            return self.all()
        else:
            query = query.strip()
            return self.filter(Q(title__icontains=query) | Q(content__icontains=query)).distinct()


User = get_user_model()
class Post(models.Model):
    author = models.ForeignKey(User, default=1)

    title = models.CharField(max_length=50)   
    slug = models.SlugField(null=False, blank=True)
    content = models.TextField()
    category = models.CharField(max_length=50)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects   = PostManager()

    def __str__(self):
        return self.title



### DATABASE CALLBACKS ###
def post_pre_save(sender, instance, *args, **kwargs):
	if not instance.slug or instance.slug == '':
		instance.slug = unique_slug_generator(instance)


pre_save.connect(post_pre_save, sender=Post)