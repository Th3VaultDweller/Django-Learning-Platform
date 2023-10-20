from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from .fields import OrderField

# Create your models here.


class Subject(models.Model):
    """A representation of a learning subject"""

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Course(models.Model):
    """A representation of a course that a student is in"""

    owner = models.ForeignKey(
        User, related_name="courses_created", on_delete=models.CASCADE
    )  # a teacher who created the course
    subject = models.ForeignKey(
        Subject, related_name="courses", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    overview = models.TextField()  # short info about the course
    created = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(User, 
                                      related_name="course_joined", 
                                      blank=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.title


class Module(models.Model):
    """A representaion of a course's module"""

    course = models.ForeignKey(Course, related_name="modules", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=["course"])

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.order}. {self.title}"


class Content(models.Model):
    """A representation of all of the content on the platform"""

    module = models.ForeignKey(
        Module, related_name="contents", on_delete=models.CASCADE
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={"model__in": ("text", "video", "file", "image")},
    )
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey("content_type", "object_id")
    order = OrderField(blank=True, for_fields=["module"])

    class Meta:
        ordering = ["order"]


class ItemBase(models.Model):
    """An abstract model for all media content"""

    owner = models.ForeignKey(
        User, related_name="%(class)s_related", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    creted = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Text(ItemBase):
    """A model for storing text content"""

    content = models.TextField()


class File(ItemBase):
    """A model for storing files such as PDFs"""

    file = models.FileField(upload_to="files")


class Video(ItemBase):
    """A model for storing video content"""

    video = models.URLField()


class Image(ItemBase):
    """A model for storing images"""

    image = models.FileField(upload_to="images")
