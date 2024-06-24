from django.shortcuts import render, get_object_or_404
from .models import *


def store(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'store.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
    context = {'items': items, 'order': order}
    return render(request, 'store/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all() 
    else:
        # Vytvoří prázdnou objednávku pro nepřihlášeného uživatele
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        items = []

    context = {'items': items, 'order': order}
    return render(request, 'store/checkout.html', context)

def product(request):
    product_id = request.GET.get('id')
    product = get_object_or_404(Product, id=product_id)
    context = {'product': product}
    return render(request, 'store/product.html', context)



# Create your views here.
