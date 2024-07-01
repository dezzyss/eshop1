
import json
from .models import *

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES.get('cart', '{}'))
    except json.JSONDecodeError:
        cart = {}

    print('Cart:', cart)
    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    cartItems = 0

    for i in cart:
        try:
            product = Product.objects.get(id=i)
            if cart[i]['quantity'] <= product.stock:  # Kontrola dostupného množství na skladě
                total = product.price * cart[i]['quantity']

                order['get_cart_total'] += total
                order['get_cart_items'] += cart[i]['quantity']

                item = {
                    'product': {
                        'id': product.id,
                        'name': product.name,
                        'price': product.price,
                        'imageURL': product.image.url,
                    },
                    'quantity': cart[i]['quantity'],
                    'get_total': total,
                }
                items.append(item)

                if not product.digital:
                    order['shipping'] = True
            else:
                # Pokud je počet kusů v košíku větší než dostupné množství na skladě, přidat jen maximální dostupné množství
                total = product.price * product.stock

                order['get_cart_total'] += total
                order['get_cart_items'] += product.stock

                item = {
                    'product': {
                        'id': product.id,
                        'name': product.name,
                        'price': product.price,
                        'imageURL': product.image.url,
                    },
                    'quantity': product.stock,
                    'get_total': total,
                }
                items.append(item)

                if not product.digital:
                    order['shipping'] = True

                # Aktualizovat množství v košíku na maximální dostupné množství
                cart[i]['quantity'] = product.stock

        except Product.DoesNotExist:
            print(f'Product with id {i} does not exist')
            pass

    cartItems = order['get_cart_items']
    print('Items:', items)
    print('Order:', order)
    print('Cart Items:', cartItems)

    return {'cartItems': cartItems, 'order': order, 'items': items}
