from django.shortcuts import redirect, render
from .forms import CheckOutForm, ProductSearchForm
from .getcart import cartData
from django.urls import reverse
from .models import Order, OrderItem, Product, ProductCategory, ProductSubCategory, Product, ProductCategory, Shop
import urllib.parse
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from .utils import send_order_notification

def shop(request):
    shop = Shop.objects.all()[0]
    current_category = 'all'
    page_title = shop.shop_name
    paginator = Paginator(shop.products.all(), 12)
    try:
        page_number = request.GET.get('page')
    except:
        page_number = 1
    page_obj = paginator.get_page(page_number)
    context = {
        'shop':shop,
        'current_category':current_category,
        'products':page_obj,
        'page_title':page_title,
        'page_obj':page_obj,
        'cart':cartData(request)
    }
    return render(request,'shops/shop.html',context)

def product_details(request, product_id):
    product = Product.objects.get(id = product_id)
    page_title = 'Product details'
    context = {
        'shop':product.shop,
        'current_category':product.product_category.category,
        'product':product,
        'page_title':page_title,
        'cart':cartData(request)
    }
    return render(request,'shops/productdetails.html',context)

def products_by_category(request,category_name):
    name = urllib.parse.unquote_plus(category_name)
    category = ProductCategory.objects.get(category_name = name)
    products = category.products
    page_title = category.category_name

    paginator = Paginator(products, 12)
    try:
        page_number = request.GET.get('page')
    except:
        page_number = 1
    page_obj = paginator.get_page(page_number)

    context = {
        'products':page_obj,
        'page_obj':page_obj,
        'current_category':category,
        'page_title':page_title,
        'shop':category.shop,
        'cart':cartData(request)
    }
    return render(request,'shops/shop.html',context)

def products_by_sub_category(request,category_name,sub_category_name):
    name = urllib.parse.unquote_plus(sub_category_name)
    sub_category = ProductSubCategory.objects.get(subcategory_name = name)
    products = sub_category.products.all()
    page_title = sub_category.subcategory_name

    paginator = Paginator(products, 12)
    try:
        page_number = request.GET.get('page')
    except:
        page_number = 1

    page_obj = paginator.get_page(page_number)

    context = {
        'products':page_obj,
        'page_obj':page_obj,
        'current_category':sub_category.category,
        'page_title':page_title,
        'shop':sub_category.category.shop,
        'cart':cartData(request)
    }
    return render(request,'shops/shop.html',context)

def product_search(request):
    filled_form = ProductSearchForm(request.POST)
    if filled_form.is_valid():
        category_name = filled_form.cleaned_data['category_name']
        product_name = filled_form.cleaned_data['product_name']

        if category_name == 'all':
            products = Product.objects.filter(product_name__icontains = product_name)
        
        else:
            products = Product.objects.filter(product_category__category__category_name = category_name).filter(product_name__icontains = product_name)

        if products.count() > 0:
            current_category = ''
            page_title = 'product search results'
            context = {
                'products':products,
                'current_category':current_category,
                'page_title':page_title,
                'shop':Shop.objects.all()[0],
                'cart':cartData(request)
            }
            return render(request,'shops/shop.html',context)
        else:
            messages.info(request,f"No product matched searched name")
            return redirect('shop')
    else:
        messages.error(request,f"Error occured during search {filled_form.errors.as_text()}")
        return redirect('shop')

def cart(request):
    cart = cartData(request)
    shop = Shop.objects.all()[0]
    current_category = ''
    page_title = "shopping cart"

    if request.method=="POST":
        filled_form = CheckOutForm(request.POST)

        if filled_form.is_valid():

            order = Order.objects.create(shop = shop)
            checkout_info = filled_form.save()
            checkout_info.order = order
            checkout_info.save()
            try:
                for item in cart['items']:
                    product = Product.objects.get(id=item['id'])
                    OrderItem.objects.create(
                        product=product,
                        order=order,
                        quantity=item['quantity'],
                    )

                messages.success(request,f'Order was placed successfuly. We shall get back to you soon. Thank you for shopping with us')
                url = reverse('cart')
                response = HttpResponseRedirect(url)
                response.delete_cookie('cart')

                # try:
                #     send_order_notification(order)
                # except Exception as err:
                #     # raise err
                #     print(f'ERROR:{type(err).__name__} {str(err)}')

                return response

            except Exception as err:
                context={
                    'form':filled_form,
                    'cart':cart,
                    'current_category':current_category,
                    'page_title':page_title,
                    'shop':shop,
                    'cart':cartData(request)
                }
                messages.error(request,'Order was not placed. Error occured please try again ')
                return render(request,'app/cart.html',context)
        else:
            context={
                'form':filled_form,
                'cart':cart,
                'current_category':current_category,
                'page_title':page_title,
                'shop':shop,
                'cart':cartData(request)
            }
            messages.error(request,'Order was not placed. Error occured please try again')
            return render(request,'app/cart.html',context)

    elif request.method == "GET":
        initial_data = {
            'phone_number': '254'
        }
        form = CheckOutForm(initial=initial_data)
        context={
            'form':form,
            'cart':cart,
            'current_category':current_category,
            'page_title':page_title,
            'shop':shop,
            'cart':cartData(request)
        }
        return render(request,'shops/cart.html',context)