from django.db import models

class CountryInput(models.Model):
    countries = models.TextField()

    def __str__(self):
        return self.countries