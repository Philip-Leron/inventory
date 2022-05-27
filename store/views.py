#from pyexpat.errors import messages
from urllib import response
from django.dispatch import receiver
from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import *
from .forms import ProdutForm,BrandForm,CategoryForm
import json
from django.db.models import Q
from django.db import connection
from django.contrib import messages
from . utils import cookieCart,cartData
from django.db import connection
from django.core.paginator import Paginator
import urllib
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required(login_url='login')
def store(request):
    
    """      if request.user.is_authenticated:
            receiver=request.user.receiver
            order,created=Order.objects.get_or_create(receiver=receiver,complete=False)
            items=order.orderitem_set.all()
            cartItems=order.getCartItems
        else:
            #items=[]
            #order={'getCartItems':0,'shipping':False}
            #cartItems=order['getCartItems']
            cookieData = cookieCart(request)
            cartItems=cookieData['cartItems']"""
    if 's' in request.GET:
        s=request.GET['s']
        products=Product.objects.filter(serial__icontains=s)
        #multiple=Q(Q(serial__icontains=s) | Q(category__icontains=s) | Q(brand__icontains=s))
        #products=Product.objects.filter(multiple)
    else:
        products =Product.objects.all()
        page=Paginator(products,15)
        page_list=request.GET.get('page')
        page=page.get_page(page_list)

    

    
    data = cartData(request)
    #data['cartItems']=0
    cartItems=data['cartItems']
    
        
    
    context={'products':products,'cartItems':cartItems,'page':page}
    return render(request,'store/store.html',context)



@login_required(login_url='login')
def checkout(request):
   
    #items=[]
    #order={'getCartItems':0,'shipping':False}
    #cartItems=order['getCartItems']
    
    data = cartData(request)
    cartItems=data['cartItems']
    order=data['order']
    items=data['items']
    """
    cookieData=cookieCart(request)
    cartItems=cookieData['cartItems']
    order=cookieData['order']
    items=cookieData['items']
    """
    receivers =Receiver.objects.all()
    
    if request.method=='POST':
        issuer=request.POST.get('issuer','')
        emailIssuer=request.POST.get('emailIssuer','')
        r=request.POST.get('r','')
        division=request.POST.get('division','')
        dept=request.POST.get('dept','')
        location=request.POST.get('location','')
        purpose=request.POST.get('purpose','')
        #print(r)
        cursor.execute(f"INSERT INTO [inventory].[dbo].[order1](iName,iEmail,rName,rDivision,rDepartment,rLocation,rPurpose) VALUES('{issuer}','{emailIssuer}','{r}','{division}','{dept}','{location}','{purpose}')")
        
        trasactionID=cursor.execute("SELECT TOP 1 id FROM [inventory].[dbo].[order1] ORDER BY id DESC").fetchval()
        #cookieData=cookieCart(request)
        #itemi=cookieData['items']
        
        
        for item in items:
            #for i in itemi:
            productId=item.product.id
            #product=Product.objects.get(id=item['product']['id'])
            quantity=item.quantity
            #product=request.POST.get('prodID','')
            #print(trasactionID,product)
            #product=product
            #order=order
           #quantity=request.POST.get('quantity','')
            cursor.execute(f"""INSERT INTO [inventory].[dbo].[orderDetails] (orderID,productID,quantity) VALUES('{trasactionID}','{productId}','{quantity}')
            UPDATE [inventory].[dbo].[store_product] SET status=0,returned=0 WHERE id='{productId}'
            """)
            
            receiver=request.user.receiver
            product = Product.objects.get(id=productId)
            order, created = Order.objects.get_or_create(receiver=receiver, complete=False)
            orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
            

            orderItem.delete()
            cartItems=0
            orderItem.quantity = 0
            
            #orderItem.save()
         
        
    context={'items':items,'order':order,'cartItems':cartItems,'receivers':receivers}
    return render(request,'store/checkout.html',context)
@login_required(login_url='login')
def cart(request):
    data = cartData(request)

   




    cartItems=data['cartItems']
    order=data['order']
    items=data['items']

    context={'items':items,'order':order,'cartItems':cartItems}
    return render(request,'store/cart.html',context)
@login_required(login_url='login')
def main(request):
    context={}
    return render(request,'store/main.html',context)


@login_required(login_url='login')
def category(request):
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
        #order=cookieData['order']
        #items=cookieData['items']
    items =Category.objects.all()
    if request.method=='POST':
        form=CategoryForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            #messages.success(request,"Form submission successful")
            return redirect('category')
    else:
        form=CategoryForm()
    context={'items':items,'form':form,'cartItems':cartItems}
    
    return render(request,'store/category.html',context)
@login_required(login_url='login')
def product(request):
    if request.user.is_authenticated:
        receiver=request.user.receiver
        order,created=Order.objects.get_or_create(receiver=receiver,complete=False)
        items=order.orderitem_set.all()
        cartItems=order.getCartItems
    else:
        items=[]
        order={'getCartItems':0,'shipping':False}
        cartItems=order['getCartItems']
    #products =Product.objects.all()
    #context={'products':products,'cartItems':cartItems}
    items=Product.objects.all()
    if request.method=='POST':
        form=ProdutForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            #messages.success(request,"Form submission successful")
            return redirect('product')
    else:
        form=ProdutForm()
    context={'items':items,'form':form,'cartItems':cartItems}
    return render(request,'store/product.html',context)
@login_required(login_url='login')
def checkin(request):
    if request.user.is_authenticated:
        receiver=request.user.receiver
        order,created=Order.objects.get_or_create(receiver=receiver,complete=False)
        items=order.orderitem_set.all()
        cartItems=order.getCartItems
    else:
        items=[]
        order={'getCartItems':0,'shipping':False}
        cartItems=order['getCartItems']
    #products =Product.objects.all()
    #context={'products':products,'cartItems':cartItems}
    items=cursor.execute("SELECT * FROM order1 ORDER BY id DESC")
    """
    if request.method=='POST':
        form=ProdutForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            #messages.success(request,"Form submission successful")
            return redirect('product')
    else:
        form=ProdutForm()
    """
    context={'items':items,'cartItems':cartItems}
    return render(request,'store/checkin.html',context)
@login_required(login_url='login')
def detail(request,id):
    if request.user.is_authenticated:
        receiver=request.user.receiver
        order,created=Order.objects.get_or_create(receiver=receiver,complete=False)
        items=order.orderitem_set.all()
        cartItems=order.getCartItems
    else:
        items=[]
        order={'getCartItems':0,'shipping':False}
        cartItems=order['getCartItems']
    #products =Product.objects.all()
    #context={'products':products,'cartItems':cartItems}
    items=cursor.execute("{call getItemsId(%s) }"%id)
    #ordi=items=cursor.execute("{call getOrder(%s) }"%id)
    
    if request.method=='POST':
        
        res=request.POST.getlist('boxes')
        print(res)
        for productId in res:
            product=int(productId)
            print(product)
            
            cursor.execute(f"""SET NOCOUNT ON
            UPDATE [inventory].[dbo].[store_product] SET status=1,returned=NULL WHERE id='{product}'
            """)
        return redirect('checkin')
    context={'items':items,'cartItems':cartItems}
    return render(request,'store/detail.html',context)
    
@login_required(login_url='login')
def brand(request):
    if request.user.is_authenticated:
        receiver=request.user.receiver
        order,created=Order.objects.get_or_create(receiver=receiver,complete=False)
        items=order.orderitem_set.all()
        cartItems=order.getCartItems
    else:
        items=[]
        order={'getCartItems':0,'shipping':False}
        cartItems=order['getCartItems']
    items =Brand.objects.all()
    if request.method=='POST':
        form=BrandForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            #messages.success(request,"Form submission successful")
            return redirect('brand')
    else:
        form=BrandForm()
    context={'items':items,'form':form,'cartItems':cartItems}
    return render(request,'store/brand.html',context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)
    receiver=request.user.receiver
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(receiver=receiver, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    elif action == 'clear':
        orderItem.quantity = 0
        orderItem.delete()
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item was added', safe=False)

@login_required(login_url='login')
def brand_update(request,pk):
    item= Brand.objects.get(id=pk)
    data = cartData(request)
    cartItems=data['cartItems']
    context={'cartItems':cartItems}
    if request.method=='POST':
        form = BrandForm(request.POST,instance=item)
        if form.is_valid():
            form.save()
            messages.success(request,'Brand has been updated successfully')
    
            return redirect('brand')
    else:
        form= BrandForm(instance=item)
    context={
        'form':form,'cartItems':cartItems,


    }
    return render(request,'store/brandUpdate.html',context)
@login_required(login_url='login')
def category_update(request,pk):
    item= Category.objects.get(id=pk)
    data = cartData(request)
    cartItems=data['cartItems']
    context={'cartItems':cartItems}
    if request.method=='POST':
        form = CategoryForm(request.POST,instance=item)
        if form.is_valid():
            form.save()
            messages.success(request,'Category has been updated successfully')
    
            return redirect('category')
    else:
        form= CategoryForm(instance=item)
    context={
        'form':form,'cartItems':cartItems,


    }
    return render(request,'store/categoryUpdate.html',context)
@login_required(login_url='login')
def product_update(request,pk):
    item= Product.objects.get(id=pk)
    data = cartData(request)
    cartItems=data['cartItems']
    context={'cartItems':cartItems}
    if request.method=='POST':
        form = ProdutForm(request.POST,request.FILES,instance=item)
        if form.is_valid():
            form.save()
            #if request.POST.get('Update') =='Update':
            messages.success(request,'Product has been updated successfully')
    
            return redirect('product')
        
    else:
        form= ProdutForm(instance=item)
    context={
        'form':form,'cartItems':cartItems,


    }
    return render(request,'store/productUpdate.html',context)
@login_required(login_url='login')
def brand_delete(request,pk):
    item=Brand.objects.get(id=pk)
    data = cartData(request)
    cartItems=data['cartItems']
    context={'cartItems':cartItems}
    if request.method=='POST':
        item.delete()
        messages.error(request,'Brand has been deleted successfully')
        
        return redirect('brand')
    return render(request,'store/brandDelete.html',context)
@login_required(login_url='login')
def category_delete(request,pk):
    item=Category.objects.get(id=pk)
    data = cartData(request)
    cartItems=data['cartItems']
    context={'cartItems':cartItems}
    if request.method=='POST':
        item.delete()
        messages.error(request,'Category has been deleted successfully')
        
        return redirect('category')
    return render(request,'store/categoryDelete.html',context)
@login_required(login_url='login')
def product_delete(request,pk):
    item=Product.objects.get(id=pk)
    data = cartData(request)
    cartItems=data['cartItems']
    context={'cartItems':cartItems}
    if request.method=='POST':
        item.delete()
        messages.error(request,'Product has been deleted successfully')
    
        return redirect('product')
    return render(request,'store/productDelete.html',context)

cursor= connection.cursor()

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
@login_required(login_url='login')
def processOrder(request):
    transactionID=datetime.datetime.now().timestamp()
    data=json.loads(request.body)
    if request.user.is_authenticated:
        receiver=request.user.receiver
        transactionID=datetime.datetime.now().timestamp()
        cursor.execute(f"INSERT INTO store_order (dateOrdered,complete,transactionID,receiver_id) VALUES('GETDATE()','True','{transactionID}','{receiver}')")
           
        """
        order, created = Order.objects.get_or_create(receiver=receiver, complete=False)
        total = data['form']['total']
        order.transactionID = transactionID
        cursor.execute(f"INSERT INTO store_order (dateOrdered,complete,transactionID,receiver_id) VALUES('GETDATE()','True','{transactionID}','{receiver}')")
           
        if total == order.getCartItems:
            order.complete = True
            
        order.save()
        """
        """
        if order.shipping==True:
            
            ShippingAddress.objects.create(
                receiver=receiver,
                issuer=data['form']['issuer'],
                division=data['user']['division'],
                dept=data['user']['dept'],
                location=data['user']['location'],
                purpose=data['user']['purpose'],

            )
            """
    else:
        print('user is not logged in')
        print('cookies',request.COOKIES)
        name=data['form']['name']
        email=data['form']['email']
        
        cookieData=cookieCart(request)
        items=cookieData['items']
        issuer,created=Issuer.objects.get_or_create(
            email=email,
        )
        issuer.name=name
        issuer.save()
        order=Order.objects.create(
            issuer=issuer,
            complete=False,
        )
        for item in items:
            product=Product.objects.get(id=item['product']['id'])
            orderItem=OrderItem.objects.create(
                product=product,
                order=order,
                quantity=item['quantity']
            )


    
    #return JsonResponse('Order Complete',safe=False)
    return render(request,'checkout.html')