from django.db import models

# Create your models here.
from django.template.defaultfilters import truncatechars


class Categories(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Broadcast(models.Model):
    title = models.CharField(max_length=100)
    url = models.TextField(max_length=300)
    categories = models.ForeignKey(Categories, on_delete=models.PROTECT)
    total_view = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class News(models.Model):
    title = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='images/')
    desc = models.TextField()

    @property
    def short_desc(self):
        return truncatechars(self.desc, 100)

    def __str__(self):
        return self.title


class PlayerProfile(models.Model):
    name = models.CharField(max_length=100)
    profile = models.ImageField(upload_to='profile/')
    desc = models.TextField()

    def __str__(self):
        return self.name

    @property
    def short_desc(self):
        return truncatechars(self.desc, 100)
