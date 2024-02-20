from rest_framework import serializers
from .models import Product, Customer, Quotation, LineItem, Business

class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'business']


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class LineItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    
    class Meta:
        model = LineItem
        fields = '__all__'


class SlimQuotationSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    
    class Meta:
        model = Quotation
        fields = ['id', 'title', 'customer', 'created_on', 'last_modified']


class QuotationSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    business = BusinessSerializer()
    line_items = LineItemSerializer(many=True)
    
    class Meta:
        model = Quotation
        fields = '__all__'
