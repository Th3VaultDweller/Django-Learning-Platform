from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Subject(models.Model):
    """A representation of a learning subject"""

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        ordering = ["title"]
    
    def __str__(self):
        return self.title