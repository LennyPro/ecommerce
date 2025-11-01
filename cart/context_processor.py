from cart.cart import Cart


# provide the 'cart' data to all templates
def cart(request):
    cart_processor = Cart(request)
    return {'cart': cart_processor}


'''
To use it as a context processor, 
you would add it to the "context_processors" option in your Django "settings" file, 
typically found in the TEMPLATES setting.


settings.py:

TEMPLATES = [
    {
        'OPTIONS': {
            'context_processors': [
                'cart.context_processor.cart',
            ],
        },
    },
] 
'''
