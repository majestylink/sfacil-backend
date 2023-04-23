
from django.urls import path
from . import views

urlpatterns = [
    path('', views.CustomerView.as_view(), name='get_customers'),
]