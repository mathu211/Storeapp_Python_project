from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from .models import Product, Customer, Order, Address
from decimal import Decimal

# ==================== PRODUCT BROWSING ====================

def home(request):
    """Display home page with all products"""
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def product_list(request):
    """Display all products in grid format"""
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def product_detail(request, product_id):
    """Display single product details with add to cart form"""
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

# ==================== SHOPPING CART ====================

@require_POST
def add_to_cart(request, product_id):
    """Add product to shopping cart (stored in session)"""
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    
    # Get quantity from form, default to 1
    quantity = int(request.POST.get('quantity', 1))
    product_id_str = str(product_id)
    
    # If product already in cart, increase quantity
    if product_id_str in cart:
        cart[product_id_str]['quantity'] += quantity
    else:
        # Add new product to cart
        cart[product_id_str] = {
            'name': product.name,
            'price': str(product.price),
            'quantity': quantity
        }
    
    request.session['cart'] = cart
    return redirect('product_list')

def view_cart(request):
    """Display shopping cart with totals"""
    cart = request.session.get('cart', {})
    total = Decimal('0')
    cart_items = []
    
    # Calculate totals for each item
    for product_id, item in cart.items():
        item_total = Decimal(item['price']) * item['quantity']
        total += item_total
        cart_items.append({
            'product_id': product_id,
            'name': item['name'],
            'price': item['price'],
            'quantity': item['quantity'],
            'total': item_total
        })
    
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })

# ==================== CHECKOUT & ORDERS ====================

def checkout(request):
    """Display checkout form for customer and address details"""
    cart = request.session.get('cart', {})
    
    # Cannot checkout without items in cart
    if not cart:
        return redirect('product_list')
    
    return render(request, 'checkout.html', {'cart': cart})

@require_POST
def place_order(request):
    """Create order with customer, address, and order records"""
    cart = request.session.get('cart', {})
    
    # Verify cart exists
    if not cart:
        return redirect('product_list')
    
    # Create Customer record from form data
    customer = Customer.objects.create(
        first_name=request.POST.get('first_name'),
        last_name=request.POST.get('last_name'),
        email=request.POST.get('email'),
        phone=request.POST.get('phone')
    )
    
    # Create Address record linked to Customer
    Address.objects.create(
        customer=customer,
        street=request.POST.get('street'),
        city=request.POST.get('city'),
        zip_code=request.POST.get('zip_code')
    )
    
    # Create Order record linked to Customer
    order = Order.objects.create(customer=customer, payment_status='p')
    
    # Clear cart from session (fresh start for next customer)
    del request.session['cart']
    
    return render(request, 'order_confirmation.html', {'order': order})

# ==================== ORDER MANAGEMENT ====================

def orders_list(request):
    """Display all orders placed"""
    orders = Order.objects.all().order_by('-placed_at')
    return render(request, 'orders_list.html', {'orders': orders})

def order_detail(request, order_id):
    """Display detailed order information with customer and address"""
    order = get_object_or_404(Order, id=order_id)
    customer = order.customer
    address = Address.objects.get(customer=customer)
    
    return render(request, 'order_detail.html', {
        'order': order,
        'customer': customer,
        'address': address
    })
