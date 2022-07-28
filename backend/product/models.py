from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)
    icon = models.ImageField(upload_to="media/category")

    def __str__(self):
        return self.name


# Create your models here.
class Product(models.Model):
    label = models.CharField(max_length=200)
    price = models.FloatField()
    image = models.ImageField(upload_to="media/product")
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.label


class Property(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to="media/property")
    metrics = models.CharField(max_length=100)

    def __str__(self):
        return self.name
