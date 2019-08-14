from django.db import models
from profiles.models import User
from django.utils import timezone
from django.urls import reverse

# Create your models here.


class News(models.Model):
    title = models.CharField(max_length=100)
    thumb = models.ImageField(default='1.png', upload_to='news_thumb')
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news:detail', kwargs={'pk': self.pk})