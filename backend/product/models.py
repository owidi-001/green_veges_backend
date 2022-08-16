from django.db import models

from vendor.models import Vendor


class Category(models.Model):
    name = models.CharField(max_length=50)
    icon = models.ImageField(upload_to="media/category")

    def __str__(self):
        return self.name


# Create your models here.
class Product(models.Model):
    label = models.CharField(max_length=200)
    unit_price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='unit price')
    image = models.ImageField(upload_to="media/product")
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='quantity', default=1)

    def __str__(self):
        return self.label

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'
        ordering = ('label',)

    def total_price(self):
        return self.quantity * self.unit_price

    total_price = property(total_price)

    # product
    # def get_product(self):
    #     return self.content_type.get_object_for_this_type(id=self.object_id)
    #
    # def set_product(self, product):
    #     self.content_type = ContentType.objects.get_for_model(type(product))
    #     self.object_id = product.pk

    # product = property(get_product, set_product)


class Property(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to="media/property")
    metrics = models.CharField(max_length=100)

    def __str__(self):
        return self.name
