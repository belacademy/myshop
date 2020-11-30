from django.db import models
from shop.models import Product


class Order(models.Model):
    full_name = models.CharField(max_length=100, null=True)
    #last_name = models.CharField(max_length=50)
    hellocash_id = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=13)
    system = models.CharField(max_length=20, default="lucy")
    tracenumber = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    #address = models.CharField(max_length=250)
    #postal_code = models.CharField(max_length=20)
    #city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    expires = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=15, null=True, blank=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
