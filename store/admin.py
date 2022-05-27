from django.contrib import admin

# Register your models here.
from . models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin

admin.site.site_header="WAEC CYBER INVENTORY ADMIN"
class ViewAdmin(ImportExportModelAdmin):
    pass

admin.site.register(Brand,ViewAdmin)
admin.site.register(Category,ViewAdmin)

admin.site.register(Product,ViewAdmin)
admin.site.register(Receiver,ViewAdmin)
admin.site.register(Issuer,ViewAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)



