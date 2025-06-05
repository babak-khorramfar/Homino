from django.db import models


class City(models.Model):
    name = models.CharField(max_length=100)
    province = models.CharField(max_length=100, blank=True)  # در صورت نیاز

    def __str__(self):
        return self.name


class Region(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="regions")
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - {self.city.name}"
