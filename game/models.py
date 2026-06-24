from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    inventory = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name
    class Meta:
        ordering = ['name']

class Customer(models.Model):
    MEMBER_CHOICES = [ 
        ('B', 'Bronze'),
        ('S', 'Silver'), 
        ('G', 'Gold'),
    ]
    membership_level = models.CharField(max_length=1, choices=MEMBER_CHOICES, default='B')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=200)
    birth_date = models.DateField(null=True)
 
class Order(models.Model):
    placed_at = models.DateTimeField(auto_now_add=True)
    PAYMENT_CHOICES = [
        ('p', 'Pending'),
        ('c', 'Complete'),
        ('f', 'Failed'),
    ]
    payment_status = models.CharField(max_length=1, choices=PAYMENT_CHOICES, default='p')
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    

class Address(models.Model):
    street = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20, null=True)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True)





