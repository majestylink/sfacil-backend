from django.urls import path
from . import views

app_name = 'purchase'

urlpatterns = [
    path('', views.PurchaseIndexView.as_view(), name='orders'),
    path('<int:customer_id>/', views.DistributorOrderAPIView.as_view(), name='customer_orders'),
    path('retails/', views.RetailOrderAPIView.as_view(), name='retail_orders'),
    path('earnings/', views.EarningsView.as_view(), name='earnings'),
]
