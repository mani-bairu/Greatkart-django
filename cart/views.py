from django.shortcuts import render,redirect
from store.models import Product,variations
from .models import Cart , Cart_items
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart= request.session.create()
    return cart





def add_cart(request,product_id):

    if request.user.is_authenticated:
        print('enter in is_authenticated')
        current_user=request.user
        print(current_user)
        product= Product.objects.get(id=product_id)
        product_variations=[]
        if request.method=='POST':
            for item in request.POST:
                key=item
                value=request.POST[key]
                print(key,value)
                try:
                    variation= variations.objects.get(product=product,variation_category__iexact=key,variation_value__iexact=value)
                    product_variations.append(variation)
                    print('got variations')
                
                except:
                    pass
            
        is_cart_item_exist=Cart_items.objects.filter(product=product,user=current_user).exists()
        print(is_cart_item_exist)
        if is_cart_item_exist:
            try:
                cart_items= Cart_items.objects.get(product=product,user=current_user,variation=variation)
                cart_items.quantity += 1
                cart_items.save()
            except Cart_items.DoesNotExist:
                cart_items= Cart_items.objects.create(product=product,user=current_user,quantity=1)
                cart_items.variation.clear()
                for items in product_variations:
                    cart_items.variation.add(items)
                cart_items.save()
        else:
            print('enter in else block')
            cart_items= Cart_items.objects.create(user=current_user,product=product,quantity=1)
            print('enter in else block line 2')
            cart_items.variation.clear()
            for items in product_variations:
                print('enter in else block line ',items)
                
                cart_items.variation.add(items)
            print('enter in else block after the for loop ')
            

            cart_items.save()

        return redirect( 'cart')

    #if user is not Authenticated 
    else:
        product= Product.objects.get(id=product_id)
        product_variations=[]
        if request.method=='POST':
            for item in request.POST:
                key=item
                value=request.POST[key]
                print(key,value)
                try:
                    variation= variations.objects.get(product=product,variation_category__iexact=key,variation_value__iexact=value)
                    product_variations.append(variation)
                
                except:
                    pass
            
        try:
        
            cart=Cart.objects.filter(cart_id=_cart_id(request)).exists()
        
            if cart:
                cart=Cart.objects.get(cart_id=_cart_id(request))
            else:
                cart=Cart.objects.create(cart_id=_cart_id(request))
            
                print(cart)
                cart.save()


        except Exception as e:
            print(e)
        

        is_cart_item_exist=Cart_items.objects.filter(product=product,cart=cart).exists()
        if is_cart_item_exist:
            try:
                cart_items= Cart_items.objects.get(product=product,cart=cart,variation=variation)
                cart_items.quantity += 1
                cart_items.save()
            except Cart_items.DoesNotExist:
                cart_items= Cart_items.objects.create(product=product,cart=cart,quantity=1)
                cart_items.variation.clear()
                for items in product_variations:
                    cart_items.variation.add(items)
                cart_items.save()
        else:
            
            cart_items= Cart_items.objects.create(product=product,cart=cart,quantity=1)
            cart_items.variation.clear()
            for items in product_variations:
                cart_items.variation.add(items)

            cart_items.save()

        return redirect( 'cart')


def remove_cart(request,product_id,cart_item_id):
    product= Product.objects.get(id=product_id)
    if request.user.is_authenticated:
        cart_item=Cart_items.objects.get(product=product,user=request.user,id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()

        else:
            cart_item.delete()
    else:

        cart=Cart.objects.get(cart_id=_cart_id(request))
    
        cart_item=Cart_items.objects.get(product=product,cart=cart,id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()

        else:
            cart_item.delete()

    return redirect('cart')


def add_cart_quantity(request,product_id,cart_item_id):
    product= Product.objects.get(id=product_id)
    if request.user.is_authenticated:
         cart_item=Cart_items.objects.get(product=product,user=request.user,id=cart_item_id)
         cart_item.quantity += 1
         cart_item.save()
    else:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_item=Cart_items.objects.get(product=product,cart=cart,id=cart_item_id)
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')
   


def delete_cart_item(request,product_id,cart_item_id):
    product= Product.objects.get(id=product_id,)
    if request.user.is_authenticated:
        cart_item=Cart_items.objects.get(product=product,user=request.user,id=cart_item_id)
        cart_item.delete()
        
    else:
        
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_item=Cart_items.objects.get(product=product,cart=cart,id=cart_item_id)
        cart_item.delete()
    return redirect('cart')





 

def cart(request):

    # cart=Cart.objects.get(cart_id=_cart_id(request))
    if request.user.is_authenticated:
        cart_items=Cart_items.objects.filter(user=request.user)
    else:
        cart_items=Cart_items.objects.filter(cart__cart_id=_cart_id(request))
    total=0
    quantiy=0
    for cart_item in cart_items:
        Total = (cart_item.product.price * cart_item.quantity)
        total += Total
        quantiy += cart_item.quantity

    tax= (2*total)/100
    grand_total=total+tax
    cart_items_count=cart_items.count()
       

    context={
        'cart_items':cart_items,
        'total':total,
        'grand_total':grand_total,
        'tax':tax,
        'quantiy':quantiy,
        'cart_items_count':cart_items_count

    }

    return render(request,'store/cart.html',context)

@login_required(login_url='signin')
def checkout(request):
    if request.user.is_authenticated:
        cart_items=Cart_items.objects.filter(user=request.user)
    else:
        cart_items=Cart_items.objects.filter(cart__cart_id=_cart_id(request))
    total=0
    quantiy=0
    for cart_item in cart_items:
        Total = (cart_item.product.price * cart_item.quantity)
        total += Total
        quantiy += cart_item.quantity

    tax= (2*total)/100
    grand_total=total+tax
    cart_items_count=cart_items.count()
       

    context={
        'cart_items':cart_items,
        'total':total,
        'grand_total':grand_total,
        'tax':tax,
        'quantiy':quantiy,
        'cart_items_count':cart_items_count

    }
    return render(request,'store/checkout.html',context)
