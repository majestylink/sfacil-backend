from django.urls import path
from . import views

app_name = 'purchase'

urlpatterns = [
    path('<int:customer_id>/', views.OrderAPIView.as_view(), name='customer_orders'),
]
