from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Business(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    phone = models.CharField(max_length=128)
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Businesses"


class Product(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    price = models.PositiveBigIntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-last_modified']

# Terms & Conditions
# Quotation Object

class Customer(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    contact = models.CharField(max_length=128)
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)    
    
    def __str__(self):
        return f'{self.name}'


class Quotation(models.Model):
    title = models.CharField(max_length=128)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.business.name}'
    
    class Meta:
        ordering = ['-last_modified']


class LineItem(models.Model):
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE, related_name='line_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.created_on}'
