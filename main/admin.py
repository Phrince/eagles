from django.contrib import admin
from .models import *

# Register your models here.

class AppinfoAdmin(admin.ModelAdmin):
    list_display = ['id']

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    list_display = ['id', 'type', 'name', 'img', 'price', 'uploaded']

admin.site.register(Appinfo, AppinfoAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(product,ProductAdmin)
admin.site.register(Size)
admin.site.register(Contact)
admin.site.register(Customer)
admin.site.register(Cart)
admin.site.register(Order)
