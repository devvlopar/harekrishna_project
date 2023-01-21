from django.db import models

# Create your models here.

class Buyer(models.Model):
    first_name = models.CharField(max_length= 50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    address = models.CharField(max_length=100)


# models = database ke andar Tables = models.py ke andar class
# SQL : structured query langauge
# ORM : Object Relational Mapping
