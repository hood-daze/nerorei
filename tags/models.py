from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=400)

    def __str__(self):
        return self.name
