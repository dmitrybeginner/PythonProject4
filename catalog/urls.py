from django.urls import path

from .apps import CatalogConfig
from .views import (
    ContactsView, ProductCreateView, ProductDeleteView, ProductDetailView,
    ProductListView, ProductUpdateView, ProductUnpublishView, ProductPublishView,
    CategoryProductListView
)

app_name = CatalogConfig.name

urlpatterns = [
    path("", ProductListView.as_view(), name="product_list"),
    path("contacts/", ContactsView.as_view(), name="contacts"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("product/create/", ProductCreateView.as_view(), name="product_create"),
    path("product/<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"),
    path("product/<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"),
    path("product/<int:pk>/unpublish/", ProductUnpublishView.as_view(), name="product_unpublish"),
    path("product/<int:pk>/publish/", ProductPublishView.as_view(), name="product_publish"),
    path("category/<int:category_id>/products/", CategoryProductListView.as_view(), name="category_products"),
]