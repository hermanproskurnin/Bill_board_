from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from random import randint


class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Advertisement(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    advertisement_category = models.ManyToManyField(Category)
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)
    media_file = models.FileField(upload_to='media/', blank=True, null=True)

    def get_absolute_url(self):
        return reverse('Ad', args=[str(self.id)])

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True)
    approve = models.BooleanField(default=False)


class Mailing(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True)


