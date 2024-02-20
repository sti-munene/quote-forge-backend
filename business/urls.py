from .views import MyBusinessViewSet, BusinessViewSet
from django.urls import path

create_business = BusinessViewSet.as_view({"post": "create"})
retrieve_user_business = MyBusinessViewSet.as_view({"get": "retrieve"})
business_detail = BusinessViewSet.as_view(
    {
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy",
    }
)

urlpatterns = [
    path("", retrieve_user_business, name="retrieve_user_business"),
    path("create/", create_business, name="create_business"),
    path("<int:id>/", business_detail, name="business_detail"),
]
