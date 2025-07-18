from django.db import models


class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='menu_images/', blank=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    items = models.ManyToManyField(MenuItem)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"Order #{self.id}"
