from django.db.models import Max, Min
from django.shortcuts import render
from .models import Category, Product, ProductImage, Brand
from math import inf


def index_view(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    product_images = ProductImage.objects.all()
    context = {
        'categories': categories,
        'products': products,
        'product_images': product_images
    }
    return render(request, 'index.html', context)


def detail_view(request, slug):
    product = Product.objects.get(slug=slug)
    product_images = ProductImage.objects.filter(product=product)
    related_products = Product.objects.filter(category=product.category).exclude(slug=slug)[:4]
    context = {
        'categories': Category.objects.all(),
        'product': product,
        'product_images': product_images,
        'related_products': related_products
    }
    print(product.get_discount_price)
    return render(request, 'product.html', context)


def store_view(request):
    max_product_price = Product.objects.aggregate(Max('price'))['price__max']
    min_product_price = Product.objects.aggregate(Min('price'))['price__min']
    products = Product.objects.all()
    categories = Category.objects.all()
    brands = Brand.objects.all()
    context = {
        'products': products,
        'categories': categories,
        'brands': brands,
        'max_product_price': float(max_product_price),
        'min_product_price': float(min_product_price)
    }
    print(type(context['min_product_price']))
    return render(request, 'store.html', context)


def category_filter_view(request, slug):
    category = Category.objects.get(slug=slug)
    products = Product.objects.filter(category=category)
    brands = Brand.objects.all()
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'products': products,
        'brands': brands
    }
    return render(request, 'store.html', context)


def brand_filter_view(request, slug):
    brand = Brand.objects.get(slug=slug)
    products = Product.objects.filter(brand=brand)
    brands = Brand.objects.all()
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'products': products,
        'brands': brands
    }
    return render(request, 'store.html', context)


def sort_by_price(request, order):
    if order == 'asc':
        products = Product.objects.all().order_by('-price')
    elif order == 'desc':
        products = Product.objects.all().order_by('price')
    elif order == 'none':
        products = Product.objects.all()
    categories = Category.objects.all()
    brands = Brand.objects.all()
    context = {
        'products': products,
        'categories': categories,
        'brands': brands,
    }
    return render(request, 'store.html', context)

