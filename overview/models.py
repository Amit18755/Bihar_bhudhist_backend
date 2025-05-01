# overview/models.py
from django.db import models

class Overview(models.Model):
    details = models.TextField()

    def __str__(self):
        return self.details  


class OverviewImage(models.Model):
    image = models.BinaryField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id}"
