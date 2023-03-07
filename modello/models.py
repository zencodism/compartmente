from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField(default=0)
    def __str__(self):
        return f"Product: {self.name}"

class Site(models.Model):
    name = models.CharField(max_length=200)
    location = models.TextField()
    def __str__(self):
        return f"Site: {self.name}"

class Staff(models.Model):
    name = models.CharField(max_length=200)
    site = models.ForeignKey('modello.Site', on_delete=models.CASCADE)
    def __str__(self):
        return f"Staff: {self.name}"


class Tenant(models.Model):
    name = models.CharField(max_length=200)
    active = models.BooleanField(default=False)

    def __str__(self):
        return f"Tenant: {self.name}"
