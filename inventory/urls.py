from django.urls import path

from .views import RawMaterialAPIView, RawMaterialCategoryAPIView, SupplierAPIView, RawMaterialTransactionAPIView, \
    AccessoryAPIView, CoverMaterialAPIView, AccessoryTransactionAPIView, CoverMaterialsTransactionAPIView

urlpatterns = [
    path('raw-materials/', RawMaterialAPIView.as_view(), name="raw_materials"),
    path('raw-materials-category/', RawMaterialCategoryAPIView.as_view(), name="raw_materials_category"),
    path('supplier/', SupplierAPIView.as_view(), name="supplier"),
    path('raw-materials-transactions/', RawMaterialTransactionAPIView.as_view(), name="supplier"),
    path('accessories-transactions/', AccessoryTransactionAPIView.as_view(), name="accessory_transactions"),
    path('cover-materials-transactions/', CoverMaterialsTransactionAPIView.as_view(), name="cover_materials_transactions"),
    path('accessories/', AccessoryAPIView.as_view(), name="accessory"),
    path('cover-materials/', CoverMaterialAPIView.as_view(), name="cover_materials"),
]
