from django.db import models

class Data(models.Model):
    date = models.DateField()
    category = models.CharField(max_length=100)
    value = models.IntegerField()

    def __str__(self):
        return f"{self.date} - {self.category} - {self.value}"
