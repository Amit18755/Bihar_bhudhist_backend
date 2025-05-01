from django.db import models

class TouristPlace(models.Model):
    place_name = models.CharField(max_length=255)
    place_address = models.CharField(max_length=255, blank=True, null=True)
    place_description = models.TextField()
    place_image = models.BinaryField()  # images saved in binary form (base64)

    def __str__(self):
        return self.place_name
