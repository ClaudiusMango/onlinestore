from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop, name='home'),
    path('', views.shop, name='shop'),
    path('products/<int:product_id>',views.product_details,name = 'product_details'),
    path('products/<str:category_name>',views.products_by_category,name = 'products_by_category'),
    path('products/<str:category_name>/<str:sub_category_name>',views.products_by_sub_category,name = 'products_by_sub_category'),
    path('productsearch/',views.product_search,name='product_search'),
    path('shoppingcart/',views.cart,name='cart'),
]