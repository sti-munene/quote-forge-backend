from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import QuotationCreateSerializer, AddLineItemsSerializer, SlimQuotationSerializer
from utils.pagination import CustomBasePaginationSet
from .models import Quotation, LineItem
from utils.api_exceptions import (
    CustomApiException
)
from business.models import Business
from .serializers import SlimQuotationSerializer


class QuotationViewSet(viewsets.ModelViewSet):
    """
    Creates, Updates, Lists and Retrieves data for the
    quotation model. Requires user making the request to be authenticated.
    """

    serializer_class = QuotationCreateSerializer
    queryset = Quotation.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = CustomBasePaginationSet
    lookup_url_kwarg = "id"  # the url kwarg name
    # lookup_field = 'id'  # the field to look for in the model

    def get_object(self):
        """Fetch the quotation related to the user."""
        try:
            quotation_id = self.kwargs.get("id")            
            quotation = Quotation.objects.get(id=quotation_id)
            
            return quotation
        except Quotation.DoesNotExist:
            raise CustomApiException(404, "Quotation does not exist.")

    def get_queryset(self):
        user = self.request.user
        business = Business.objects.get(user=user)        
        quotations = Quotation.objects.filter(business=business)
        return quotations

    def create(self, request, *args, **kwargs):
        serializer = QuotationCreateSerializer(data=request.data)        
        serializer.is_valid(raise_exception=True)
        quote = serializer.save()
        
        headers = self.get_success_headers(serializer.data)
        ser = SlimQuotationSerializer(quote)

        return Response(
            ser.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
                
        if page is not None:
            # SlimQuotationSerializer
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, *args, **kwargs):
        user = request.user
        instance = self.get_object()
        self.perform_destroy(instance)
            
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddLineItemsViewSet(viewsets.ViewSet):
    """
    Add line items for a project data for the
    quotation model. Requires user making the request to be authenticated.
    """

    serializer_class = AddLineItemsSerializer
    queryset = Quotation.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = CustomBasePaginationSet
    lookup_url_kwarg = "id"  # the url kwarg name

    def get_object(self):
        try:
            quotation_id = self.kwargs.get("id")            
            quotation = Quotation.objects.get(id=quotation_id)
            
            return quotation
        except Quotation.DoesNotExist:
            raise CustomApiException(404, "Quotation does not exist.")

    def update(self, request, *args, **kwargs):        
        quote = self.get_object()
        serializer = AddLineItemsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        line_items = serializer.data['line_items']
        
        for item in line_items:
            LineItem.objects.create(
                quotation=quote, 
                description=item['description'],
                amount=item['amount'],
                rate=item['rate'],
                quantity=item['quantity'],
            )

        if getattr(quote, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            quote._prefetched_objects_cache = {}

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
