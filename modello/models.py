from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField(default=0)

class Site(models.Model):
    name = models.CharField(max_length=200)
    location = models.TextField()

class Void(models.Model):
    pass
