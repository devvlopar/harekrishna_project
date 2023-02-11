from django.db import models
from seller.models import *
# Create your models here.

class Buyer(models.Model):
    first_name = models.CharField(max_length= 50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.email


class Cart(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)

    def __str__(self):
        return self.buyer.first_name



# models = database ke andar Tables = models.py ke andar class
# SQL : structured query langauge
# ORM : Object Relational Mapping
