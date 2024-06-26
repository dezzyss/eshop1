from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import *




def store(request):
    category_id = request.GET.get('category', None)
    
    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()
        
    categories = Category.objects.all()
    context = {
        'products': products,
        'categories': categories,
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
    return JsonResponse('Item was added', safe=False)




# Create your views here.
