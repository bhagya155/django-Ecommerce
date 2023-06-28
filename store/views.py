from django.shortcuts import render , get_object_or_404
from django.http import HttpResponse
from . models import Product, Category

# Create your views here.

def store(request,category_slug=None):
    categories = None
    products = None
    category_name = Category.objects.all()

    if category_slug != None:
        categories = get_object_or_404(Category,slug=category_slug)
        products = Product.objects.filter(category=categories,is_available=True)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True)
        product_count = products.count()
    
    context = {"products":products, "category_name":category_name,"product_count":product_count}
    return render(request, "store/store.html" , context)

def product_detail(request, category_slug, product_slug):
    try:
        product = Product.objects.get(category__slug=category_slug,slug=product_slug)
    except Exception as e:
        raise e
    
    context = {"product":product}
    return render(request,"store/product_detail.html", context)