from django.db import models
from django.conf import settings
from django.utils import timezone

def news_picture_path(instance, filename):
    return f'news_pics/{instance.creator}/{instance.id}/{filename}'


class News(models.Model):
    """Creating 'news' table in DB"""
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.CharField(max_length=999, blank=True, null=True)
    img = models.ImageField(upload_to=news_picture_path, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    def save(self, *args, **kwargs):
        if self.creator.is_superuser:
            super().save(*args, **kwargs)
        else:
            raise PermissionError("Only administrators can create news.")
    def __str__(self):
        return f"{self.creator} send news"

