from django.db import models


class Book(models.Model):
    COVER_CHOICES = {
        "HARD": "Hard",
        "SOFT": "Soft",
    }

    Title = models.CharField(max_length=255)
    Author = models.CharField(max_length=255)
    Cover = models.CharField(max_length=8, choices=COVER_CHOICES)
    Inventory = models.PositiveIntegerField()
    Daily_fee = models.DecimalField(decimal_places=2, max_digits=7)

    def __str__(self):
        return self.Title
