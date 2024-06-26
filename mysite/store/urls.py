from django.urls import path

from . import views

urlpatterns = [
        #Leave as empty string for base url
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
    path('product/', views.product, name="product"),
    path('search/', views.search_view, name='search'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('update_item/', views.updateItem, name="update_item"),
    
    
	]