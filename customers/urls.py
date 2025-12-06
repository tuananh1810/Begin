from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from customers import views

urlpatterns = [
    path("api/customers", views.CustomersList.as_view()),
    path("api/customers/<int:pk>", views.CustomerDetail.as_view()),
    path("api/customers/order-count/", views.CustomerOrderCount.as_view()),
    path("api/customers/total-spent/", views.CustomerTotalSpent.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
