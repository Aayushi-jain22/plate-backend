from django.db import models

# Create your models here.
class Meal(models.Model):

    name = models.CharField(max_length=100)

    calories = models.IntegerField()

    protein_g = models.FloatField()

    carbs_g = models.FloatField()

    fat_g = models.FloatField()

    tags = models.JSONField(db_index=True)

    eaten_at = models.DateTimeField(db_index=True)


    class Meta:
        indexes = [
            models.Index(fields=['eaten_at']),
        ]


    def __str__(self):
        return self.name