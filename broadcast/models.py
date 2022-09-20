from django.db import models


# Create your models here.

class Categories(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Broadcast(models.Model):
    title = models.CharField(max_length=100)
    url = models.TextField(max_length=300)
    categories = models.ForeignKey(Categories, on_delete=models.PROTECT)
    total_view = models.IntegerField(default=0)
