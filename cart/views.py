from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from inventory.models import Product
from cart.cart import Cart
from cart.form import AddProductToCartForm
 

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = AddProductToCartForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            product=product,
            quantity=cd['quantity'],  # form.py properties
            override=cd['override'],  # form.py properties
        )
    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = AddProductToCartForm(
            initial={
                'quantity': item['quantity'],
                'override': True,
            },
        )
    return render(
        request,
        'cart/cart_details.html',
        {'cart': cart},
    )
