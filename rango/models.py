from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.utils import timezone
import os

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Page(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title



def get_file_path(instance, filename):
    ext = 'jpg'
    filename = "%s.%s" % (instance, ext)
    return os.path.join('profile_images', filename)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to=get_file_path , blank=True)

    def __str__(self):
        return self.user.username

def anonymousProfile():
    return UserProfile.objects.get(name='default')
class Comment(models.Model):
    # when delete a user, we want to keep the comments he posted on blog posts, but say it was posted by an anonymous (or deleted) user
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    username = models.CharField(max_length=150)
    timesmp = models.DateTimeField(default=timezone.now)
    content = models.CharField(max_length=2000)
    
    def __str__(self):
        return self.content