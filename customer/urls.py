
from django.urls import path
from . import views

urlpatterns = [
    path('', views.CustomerView.as_view(), name='customers_view'),
    # path('<int:cust_id>/', views.CustomerView.as_view(), name='customers_view'),
]