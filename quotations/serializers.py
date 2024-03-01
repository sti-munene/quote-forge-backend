
from rest_framework import serializers
from .models import  Quotation, LineItem


class LineItemsListSerializer(serializers.ListSerializer):
    def validate(self, attrs):
        # Here attrs contains list of Params You can validate it here
        pass

    def create(self, validated_data):
        line_items = [LineItem(**item) for item in validated_data]
        return LineItem.objects.bulk_create(line_items)


class LineItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = LineItem
        fields = '__all__'
        list_serializer_class = LineItemsListSerializer  # This specifies which list serializer class to use


class SlimQuotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quotation
        fields = ['id', 'created_on', 'last_modified']


class PreCreateLineItemSerializer(serializers.Serializer):
    description = serializers.CharField(required=True)
    rate = serializers.IntegerField(required=True)
    quantity = serializers.IntegerField(required=True)
    amount = serializers.IntegerField(required=True)
    
    # def validate(self, attrs):
    #     # Here attrs contains list of Params You can validate it here
    #     pass

    # def create(self, validated_data):
    #     line_items = [LineItem(**item) for item in validated_data]
    #     return LineItem.objects.bulk_create(line_items)



class QuotationCreateSerializer(serializers.ModelSerializer):    
    line_items = PreCreateLineItemSerializer(many=True, required=False)
    
    class Meta:
        model = Quotation
        fields = '__all__'


class AddLineItemsSerializer(serializers.Serializer):    
    line_items = PreCreateLineItemSerializer(many=True, required=True)
