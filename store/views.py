from django.shortcuts import render , get_object_or_404
from django.http import HttpResponse
from . models import Product, Category
from carts.models import CartItem
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q

# Create your views here.

def store(request,category_slug=None):
    categories = None
    products = None
    category_name = Category.objects.all()

    if category_slug != None:
        categories = get_object_or_404(Category,slug=category_slug)
        products = Product.objects.filter(category=categories,is_available=True)
        paginator = Paginator(products,3)
        page = request.GET.get('page')
        paged_product = paginator.get_page(page)
        product_count = products.count()
        
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products,6)
        page = request.GET.get('page')
        paged_product = paginator.get_page(page)
        product_count = products.count()
    print(paged_product) 
    context = {"products":paged_product, "category_name":category_name,"product_count":product_count}
    return render(request, "store/store.html" , context)

def product_detail(request, category_slug, product_slug):
    try:
        product = Product.objects.get(category__slug=category_slug,slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id = _cart_id(request),product=product).exists
    except Exception as e:
        raise e
    
    context = {"product":product, "in_cart": in_cart}
    return render(request,"store/product_detail.html", context)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword)| Q(product_name__icontains=keyword))
    context = {"products": products}
    print(products)
    return render(request,"store/store.html",context)