from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Shop, ProductCategory, ProductSubCategory, Product, ProductFeature, ProductImage, Order

admin.site.unregister(Group)

admin.site.register(Shop)

class ProductSubCategoryAdmin(admin.StackedInline):
    model = ProductSubCategory
    can_delete = True
    verbose_name_plural = 'Product Sub-Categories'

class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name']
    inlines = [ProductSubCategoryAdmin]

admin.site.register(ProductCategory,ProductCategoryAdmin)


class ProductImageAdmin(admin.StackedInline):
    model = ProductImage
    can_delete = True
    verbose_name_plural = 'Product Images'

class ProductFeatureAdmin(admin.StackedInline):
    model = ProductFeature
    can_delete = True
    verbose_name_plural = 'Product Features'

class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name','product_category','price']
    inlines = [ProductFeatureAdmin, ProductImageAdmin]

admin.site.register(Product,ProductAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display=['customer_name','date_ordered','completed']
    fieldsets=[('Order details', {'fields': ('shop','order_details','completed' )})]
    readonly_fields = ('order_details','shop')
    
admin.site.register(Order,OrderAdmin)
