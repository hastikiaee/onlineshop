from ...models import Cart 

def get_or_create_cart(request):
    #get or create cart for user
    user=request.user if request.user.is_authenticated else None
    session_key=request.session.session_key
    if not session_key:
        request.session.create()
        session = request.session.session_key
    
    #create or get cart with session or user and total price
    if user:
        cart,_=Cart.objects.get_or_create(user=user)
        return cart
    else:
        cart,_=Cart.objects.get_or_create(session=session)
        return cart