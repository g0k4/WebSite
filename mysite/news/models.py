from django.db import models
from profiles.models import User
from django.utils import timezone
from django.urls import reverse


class News(models.Model):
    title = models.CharField(max_length=100)
    thumb = models.ImageField(default='default_new.jpg', upload_to='news_thumb/')
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.title


    def get_absolute_url(self):
       return reverse('news:detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    new = models.ForeignKey(News, on_delete=models.CASCADE)

    def __str__(self):
        return self.content


    def get_absolute_url(self):
       return reverse('news:detail', kwargs={'pk': self.new.pk})