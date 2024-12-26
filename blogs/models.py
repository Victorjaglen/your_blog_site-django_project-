from django.db import models

class Blog(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(default='fallback.png', blank=True)

    def __str__(self):
        return self.title