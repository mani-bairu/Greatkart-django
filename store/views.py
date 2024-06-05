from django.shortcuts import render
from .models import Product 
from category.models import Category
from django.http import Http404
from cart.models import Cart_items
from cart.views import _cart_id
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.db.models import Q
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='signin')
def Store(request,category_slug=None):
  

    if category_slug != None:
        category=Category.objects.get(slug=category_slug)
        products= Product.objects.filter(category=category)
        paginator=Paginator(products,1)
        page=request.GET.get('page')
        paged_products=paginator.get_page(page)

        product_count=products.count()
    else:

        products= Product.objects.all().filter(is_avalible=True).order_by('id')
        paginator=Paginator(products,6)
        page=request.GET.get('page')
        paged_products=paginator.get_page(page)
        product_count=products.count()
    context={
        'products' :paged_products,
        'product_count':product_count

    }
    return render(request,'store/store.html',context)

@login_required(login_url='signin')
def product_detail(request,category_slug,product_slug):
    product=None
    try:
        product=Product.objects.get(slug=product_slug,category__slug=category_slug,)
        in_cart=Cart_items.objects.filter(cart__cart_id=_cart_id(request),product=product).exists()

    except Product.DoesNotExist:
        raise Http404("Product not found")
    context={
        'product':product,
        'in_cart':in_cart
    }
    return render(request,'store/product_detail.html',context)

@login_required(login_url='signin')
def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET.get('keyword')
        if keyword:
            products=Product.objects.filter(Q(product_name__icontains=keyword) | Q(discription__icontains=keyword)).order_by('id')
        else:
            pass
        product_count=products.count()
        context={
            'products':products,
            'product_count':product_count
        }
        return render(request,'store/store.html',context)


