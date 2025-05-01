from django.db import models

class OfficialLink(models.Model):
    title = models.CharField(max_length=255)
    details = models.TextField()
    links = models.URLField()
    bg_image = models.BinaryField()  # Store raw binary data (like base64)

    def __str__(self):
        return self.title
