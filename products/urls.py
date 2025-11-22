from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from products.views import category_views,supplier_views, product_views

urlpatterns = [
    path("api/categories", category_views.CategoryList.as_view()),
    path("api/categories/<int:pk>", category_views.CategoryDetail.as_view()),
    path("api/suppliers", supplier_views.SupplierList.as_view()),
    path("api/suplliers/<int:pk>", supplier_views.SpplierDetail.as_view()),
    path("api/products", product_views.ProductList.as_view()),
    path("api/products/<int:pk>", product_views.ProductDetail.as_view()),
    path("api/product-supplier-category-create/", product_views.ProductSupplierCategoryCreate.as_view()),
    path("products/", product_views.ProductListView.as_view()),
    path("suppliers/", supplier_views.SupplierListView.as_view()),
    path("categories/", category_views.CategoryListView.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)
