from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('', views.ProductAPIView.as_view(), name='get_products'),
]
