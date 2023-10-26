"""
URL configuration for sfacil project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import path, include
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def home(request):
    return Response({"success": True, "message": "Hello World🎊❤️"})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('api/customers/', include('customer.urls')),
    path('api/purchases/', include('purchase.urls')),
    path('api/products/', include('product.urls')),
    path('api/transactions/', include('transaction.urls')),
    path('api/inventories/', include('inventory.urls')),
    path('api/account/', include('account.urls')),
]
