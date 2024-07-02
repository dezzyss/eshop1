from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
import json
import datetime
from .models import *
from .utils import cookieCart




def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all() 
        cartItems = order.get_cart_items
    else:
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
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
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

    # Debugging prints
    print("Items in cart view:", items)
    print("Order in cart view:", order)
    print("Cart Items in cart view:", cartItems)

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all() 
        cartItems = order.get_cart_items
    else:
        # Vytvoří prázdnou objednávku pro nepřihlášeného uživatele
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping':False}
        items = []
        cartItems = order['get_cart_items']
        

    context = {'items': items, 'order': order, 'cartItems': cartItems}
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

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_cart_items
    else:
        cartItems = 0

    context = {
        'product': product,
        'cartItems': cartItems
    }

    return render(request, 'store/product_detail.html', context)

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

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, created = Customer.objects.get_or_create(
            email=data['form']['email'],
        )
        customer.name = data['form']['name']
        customer.save()
        
        order = Order.objects.create(
            customer=customer, complete=False,
        )
    
    total = float(data['form']['total']) 
    order.transaction_id = transaction_id
    
    if total == order.get_cart_total:
        order.complete = True
        order.save()

        if order.shipping:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )
        
        # Redirect to order summary page after successfully completing the order
        return JsonResponse({'order_id': order.id}, safe=False)
    else:
        return JsonResponse('Failed to complete payment.', safe=False)

def order_summary(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user.customer, complete=True)
    order_items = OrderItem.objects.filter(order=order)
    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'store/order_summary.html', context)






# Create your views here.
