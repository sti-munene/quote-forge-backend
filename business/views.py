from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import SlimQuotationSerializer
from utils.api_exceptions import (
    CustomApiException
)
from utils.pagination import CustomBasePaginationSet
from .models import Product, Quotation
from .serializers import ProductSerializer, QuotationSerializer, BusinessSerializer, CustomerSerializer
from .models import Business, Customer

class ProductViewSet(viewsets.ModelViewSet):
    """
    Creates, Updates, Lists and Retrieves data for the
    product model. Requires user making the request to be authenticated.
    """

    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    # permission_classes = [IsAuthenticated]
    pagination_class = CustomBasePaginationSet
    lookup_url_kwarg = "id"  # the url kwarg name
    # lookup_field = 'id'  # the field to look for in the model

    def get_object(self):
        """Fetch the product related to the user."""
        try:
            print(self.request)
            print(self.kwargs)
            
            product_id = self.kwargs.get("id")            
            product = Product.objects.get(id=product_id)
            
            return product
        except Product.DoesNotExist:
            raise CustomApiException(404, "Product does not exist.")

    def get_queryset(self):
        business = Business.objects.first()
        products = Product.objects.filter(business=business)
        
        return products

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            raise CustomApiException(400, 'Invalid')

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            {
                "data": serializer.data,
                "message": "Product created.",
            },
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
            {
                "data": serializer.data,
                "message": "Product updated.",
            },
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, *args, **kwargs):
        user = request.user
        instance = self.get_object()
        self.perform_destroy(instance)
            
        return Response(status=status.HTTP_204_NO_CONTENT)


class QuotationViewSet(viewsets.ModelViewSet):
    """
    Creates, Updates, Lists and Retrieves data for the
    quotation model. Requires user making the request to be authenticated.
    """

    serializer_class = QuotationSerializer
    queryset = Quotation.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = CustomBasePaginationSet
    lookup_url_kwarg = "id"  # the url kwarg name
    # lookup_field = 'id'  # the field to look for in the model

    def get_object(self):
        """Fetch the quotation related to the user."""
        try:
            print(self.request)
            print(self.kwargs)
            
            quotation_id = self.kwargs.get("id")            
            quotation = Quotation.objects.get(id=quotation_id)
            
            return quotation
        except Quotation.DoesNotExist:
            raise CustomApiException(404, "Quotation does not exist.")

    def get_queryset(self):
        user = self.request.user
        business = Business.objects.get(user=user)
        
        print(business)
        quotations = Quotation.objects.filter(business=business)
        return quotations

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            raise CustomApiException(400, 'Invalid')

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            {
                "data": serializer.data,
                "message": "Quotation created.",
            },
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
            {
                "data": serializer.data,
                "message": "Quotation updated.",
            },
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, *args, **kwargs):
        user = request.user
        instance = self.get_object()
        self.perform_destroy(instance)
            
        return Response(status=status.HTTP_204_NO_CONTENT)




class MyBusinessViewSet(viewsets.ViewSet):
    serializer_class = BusinessSerializer
    queryset = Business.objects.all()
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        business = Business.objects.get(user=user)
        serializer = BusinessSerializer(business)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BusinessViewSet(viewsets.ModelViewSet):
    """
    Creates, Updates, Lists and Retrieves data for the
    business model. Requires user making the request to be authenticated.
    """

    serializer_class = BusinessSerializer
    queryset = Business.objects.all()
    # permission_classes = [IsAuthenticated]
    pagination_class = CustomBasePaginationSet
    lookup_url_kwarg = "id"  # the url kwarg name
    # lookup_field = 'id'  # the field to look for in the model

    def get_object(self):
        """Fetch the business info."""
        try:
            business_id = self.kwargs.get("id")            
            business = Business.objects.get(id=business_id)
            return business
        except Business.DoesNotExist:
            raise CustomApiException(404, "Business does not exist.")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            raise CustomApiException(400, 'Invalid')

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            {
                "data": serializer.data,
                "message": "Business created.",
            },
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def retrieve(self, request, *args, **kwargs):
        # instance = self.get_object()
        
        user = request.user
        
        if user.is_anonymous:
            return Response({}, status=status.HTTP_400_BAD_REQUESTT)

        
        business = Business.objects.get(user=user)
        serializer = BusinessSerializer(business)
        print(serializer.data)
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
            {
                "data": serializer.data,
                "message": "Business updated.",
            },
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, *args, **kwargs):
        user = request.user
        instance = self.get_object()
        self.perform_destroy(instance)
            
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomerViewSet(viewsets.ModelViewSet):
    """
    Creates, Updates, Lists and Retrieves data for the
    Customer model. Requires user making the request to be authenticated.
    """

    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    # permission_classes = [IsAuthenticated]
    pagination_class = CustomBasePaginationSet
    lookup_url_kwarg = "id"  # the url kwarg name
    # lookup_field = 'id'  # the field to look for in the model

    def get_object(self):
        """Fetch the business info."""
        try:
            customer_id = self.kwargs.get("id")            
            customer = Customer.objects.get(id=customer_id)
            return customer
        except Customer.DoesNotExist:
            raise CustomApiException(404, "Customer does not exist.")

    def get_queryset(self):
        # business = Business.objects.first()
        customers = Customer.objects.all()
        return customers

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            raise CustomApiException(400, 'Invalid')

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            {
                "data": serializer.data,
                "message": "Customer created.",
            },
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
            {
                "data": serializer.data,
                "message": "Customer updated.",
            },
            status=status.HTTP_200_OK,
        )


    def destroy(self, request, *args, **kwargs):
        user = request.user
        instance = self.get_object()
        self.perform_destroy(instance)
            
        return Response(status=status.HTTP_204_NO_CONTENT)
