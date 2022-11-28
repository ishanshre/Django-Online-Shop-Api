from django.contrib import admin
from django.utils.html import format_html
from .models import *

# Register your models here.

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra: int = 0
    readonly_fields = ['thumbnail']

    def thumbnail(self, instance):
        if instance.image.name != "":
            return format_html(f'<img src="{instance.image.url}" class="thumbnail" />')
        return ""

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]

    class Media:
        css = {
            'all':['shop/css/styles.css']
        }


admin.site.register(Order)
admin.site.register(Customer)
admin.site.register(OrderItem)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Address)
admin.site.register(Promotion)
admin.site.register(Collection)
admin.site.register(Review)