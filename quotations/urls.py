from .views import QuotationViewSet, AddLineItemsViewSet
from django.urls import path

create_quote = QuotationViewSet.as_view({"post": "create"})
quote_detail = QuotationViewSet.as_view(
    {
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy",
    }
)


add_line_items = AddLineItemsViewSet.as_view(
    {
        "put": "update"
    }
)


urlpatterns = [
    path("create/", create_quote, name="create_quote"),
    path("<int:id>/", quote_detail, name="quote_detail"),
    
    path("add/line-items/<int:id>/", add_line_items, name="add_line_items"),
    
    
    
]
