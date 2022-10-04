from django.db import models

from vendor.models import Vendor


class Category(models.Model):
    name = models.CharField(max_length=50)
    icon = models.ImageField(upload_to="category//%Y/%m/%d/")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'categories'
        verbose_name_plural = 'categories'
        ordering = ('name',)


# Create your models here.
class Product(models.Model):
    label = models.CharField(max_length=200)
    unit = models.CharField(max_length=2,
                            choices=(("kg", "Kilograms"), ("g", "Grams"), ("l", "Litre"), ("ml", "Millilitre"),
                                     ("in", "Inches")), default="kg")
    unit_price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='unit price')
    image = models.ImageField(upload_to="product//%Y/%m/%d/")
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='quantity', default=1)

    def __str__(self):
        return f"{self.label}"

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'
        ordering = ('label',)
