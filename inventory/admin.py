from django.contrib import admin

from .models import *

admin.site.register(RawMaterialCategory)
admin.site.register(RawMaterial)
admin.site.register(RawMaterialTransaction)
admin.site.register(Supplier)
admin.site.register(Notification)
admin.site.register(Accessory)
admin.site.register(CoverMaterial)
admin.site.register(AccessoryTransaction)
admin.site.register(CoverMaterialTransaction)
