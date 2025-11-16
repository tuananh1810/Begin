from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from orders import views

urlpatterns = [
    path("api/orders", views.OrderList.as_view()),
    path("api/orders/<int:pk>", views.OrderDetail.as_view()),
]