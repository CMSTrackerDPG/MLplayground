from django.db import models


# Create your models here.
class Run(models.Model):
    run_number = models.IntegerField(unique=True)
    run_date   = models.DateTimeField(blank=True, null=True)

    year       = models.IntegerField(blank=True, null=True)
    period     = models.CharField(max_length=1, blank=True, null=True)

    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"run {self.run_number}"
