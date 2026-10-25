from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name='products')
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    price = models.IntegerField()
    stock = models.IntegerField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
