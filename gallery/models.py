from django.db import models

class Place(models.Model):
    heading = models.CharField(max_length=255)
    district = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.heading

class PlaceImage(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='images')
    image = models.BinaryField()  # Storing the image as binary

    def __str__(self):
        return f"Image for {self.place.heading}"
