from django.contrib.admin.utils import model_format_dict
from django.db import models
from django.contrib.auth.models import User

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
    picture = models.ImageField(default="picture.png", upload_to="product_images/")

    def discount_price(self):
        return round(self.price - self.price * self.discount * 0.01, 2)


class Order(models.Model):
    order_date = models.DateField()
    delivery_date = models.DateField()
    pickup_point = models.ForeignKey(PickupPoint, on_delete=models.CASCADE, related_name="order")
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="order")
    receive_code = models.IntegerField()
    status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name="order")


class ProductInOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_in_order")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="product_in_order")
    quantity = models.IntegerField()
