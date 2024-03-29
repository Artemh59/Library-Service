from django.db import models


class Book(models.Model):
    COVER_CHOICES = {
        "HARD": "Hard",
        "SOFT": "Soft",
    }

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.CharField(max_length=8, choices=COVER_CHOICES)
    inventory = models.IntegerField()
    daily_fee = models.DecimalField(decimal_places=2, max_digits=7)

    def __str__(self):
        return self.title
