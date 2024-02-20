from django.contrib import admin
from .models import Business, Product, Quotation, Customer, LineItem


admin.site.register(Business)
admin.site.register(Product)

admin.site.register(Quotation)
admin.site.register(Customer)
admin.site.register(LineItem)
