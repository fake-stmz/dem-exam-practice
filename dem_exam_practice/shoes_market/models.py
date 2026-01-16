from django.db import models

# Create your models here.
class MeasureUnit(models.Model):
    name = models.CharField()


class Supplier(models.Model):
    name = models.CharField()


class Producer(models.Model):
    name = models.CharField()


class Category(models.Model):
    name = models.CharField()


class Status(models.Model):
    name = models.CharField()


class PickupPoint(models.Model):
    postcode = models.IntegerField()
    city = models.CharField()
    street = models.CharField()
    house = models.IntegerField()


class Product(models.Model):
    article = models.CharField(primary_key=True)
    name = models.CharField()
    measure_unit = models.ForeignKey(MeasureUnit, on_delete=models.CASCADE, related_name="product")
    price = models.IntegerField()
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name="product")
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE, related_name="product")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="product")
    discount = models.IntegerField()
    quantity = models.IntegerField()
    description = models.TextField()
    picture = models.CharField()
