import json
from . models import *
def cookieCart(request):
    try:
        cart=json.loads(request.COOKIES['cart'])
    except:
        cart={}
    
    print("cart: ",cart)
    items=[]
    order={'getCartItems':0,'shipping':False}
    cartItems=order['getCartItems']
    
    for i in cart:
        try:
            
            cartItems+=cart[i]["quantity"]
            product=Product.objects.get(id=i)
            #total=(product)
            order['getCartItems']+=cart[i]["quantity"]
            item={
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'imageURL':product.imageURL,
                },
                'quantity':cart[i]["quantity"],

            }
            items.append(item)

            order['shipping']=True


        except:
            pass 
    return {'cartItems':cartItems,'order':order,'items':items}

def cartData(request):
    if request.user.is_authenticated:
        
        receiver=request.user.receiver
        order,created=Order.objects.get_or_create(receiver=receiver,complete=False)
        
        items=order.orderitem_set.all()
        cartItems=order.getCartItems
        


    else:
        #items=[]
        #order={'getCartItems':0,'shipping':False}
        #cartItems=order['getCartItems']
        cookieData = cookieCart(request)
        cartItems=cookieData['cartItems']
        order=cookieData['order']
        items=cookieData['items']
    return {'cartItems':cartItems,'order':order,'items':items}


