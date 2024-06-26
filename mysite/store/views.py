from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
import json
from .models import *




def store(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all() 
        cartItems = order.get_cart_items
    
    else:
        # Vytvoří prázdnou objednávku pro nepřihlášeného uživatele
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        items = []
        cartItems = order['get_cart_items']

    category_id = request.GET.get('category', None)
    
    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()
        
    categories = Category.objects.all()
    context = {
        'products': products,
        'categories': categories,
        'cartItems': cartItems,
    }
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

def search_view(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(name__icontains=query)
    context = {
        'products': products,
        'query': query,
    }
    return render(request, 'store/search_results.html', context)

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'store/product_detail.html', {'product': product})

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('productId:', productId)
    
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()


    return JsonResponse('Item was added', safe=False)






# Create your views here.
