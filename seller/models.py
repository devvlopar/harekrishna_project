from django.db import models

# Create your models here.
class Seller(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    gst_no = models.CharField(max_length=15)

    def __str__(self) -> str:
        return self.full_name