from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class Cart(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.user)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='items')
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.product.name


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Ожидает обработки'
        PROCESSING = 'processing', 'В обработке'
        CANCELLED = 'cancelled', 'Отменён'
    # Майдонҳои мавҷудаатро нигоҳ дор
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='orders')
    total_price = models.DecimalField(max_digits=10,decimal_places=2)
    status = models.CharField(max_length=20,choices=Status.choices,default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order {self.id}'



class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items')
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10,decimal_places=2 )

    def __str__(self):
        return self.product.name

