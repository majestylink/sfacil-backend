from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('', views.ProductAPIView.as_view(), name='get_products'),
    path('product-categories/', views.ProductCategoryView.as_view(), name='get_product_categories'),
    path('product-brands/', views.ProductBrandView.as_view(), name='get_product_brands'),
]
