from django.urls import path
from . import views

urlpatterns = [
    # Home and product browsing
    path('', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    
    # Shopping cart
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    
    # Checkout
    path('checkout/', views.checkout, name='checkout'),
    path('order/place/', views.place_order, name='place_order'),
    
    # Order management
    path('orders/', views.orders_list, name='orders_list'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
]