from django.conf import settings
from django.db.models import Max, Min
from django.core.mail import send_mail
from django.shortcuts import render, redirect, reverse

import stripe
from .models import Category, Product, ProductImage, Brand, Comment
from utils import CartAuthenticatedUser, UserWishlistManager
from .forms import CommentForm
from accounts.forms import EmailForm


def base_view_data(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    if request.user.is_authenticated:
        cart_info = CartAuthenticatedUser(request).get_cart_info()
        wishlist = UserWishlistManager(request).get_wishlist_info()['wishlist_products']
        context['order_products'] = cart_info['order_products']
        context['total_cart_price'] = cart_info['total_cart_price']
        context['total_product_number'] = cart_info['total_product_number']
        context['wishlist_count'] = len(wishlist)
    return context


def send_subscription_email(email):
    subject = 'Welcome message'
    message = f'Hi, thank you for registering in our website.'
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from, [email])


def index_view(request):
    base_context = base_view_data(request)
    context = {
        **base_context,
        'top_discounts': Product.objects.all().order_by('-discount')[:4]
    }
    return render(request, 'index.html', context)


def detail_view(request, slug):
    product = Product.objects.get(slug=slug)
    if request.user.is_authenticated:
        if request.method == 'POST':
            comment = request.POST.get('comment')
            data = {
                'content': comment,
                'user': request.user,
                'product': product
            }
            form = CommentForm(data)
            if form.is_valid():
                form.save()
                return redirect('detail', slug)

    product_images = ProductImage.objects.filter(product=product)
    related_products = Product.objects.filter(category=product.category).exclude(slug=slug)[:4]
    comments = Comment.objects.filter(product=product)
    base_context = base_view_data(request)
    context = {
        **base_context,
        'product': product,
        'product_images': product_images,
        'related_products': related_products,
        'comments': comments
    }
    return render(request, 'product.html', context)


def store_view(request):
    products = Product.objects.all()
    brands = Brand.objects.all()
    top_discounts = Product.objects.all().order_by('-discount')[:4]
    base_context = base_view_data(request)
    context = {
        **base_context,
        'products': products,
        'brands': brands,
        'top_discounts': top_discounts
    }
    return render(request, 'store.html', context)


def category_filter_view(request, slug):
    category = Category.objects.get(slug=slug)
    products = Product.objects.filter(category=category)
    brands = Brand.objects.all()
    base_context = base_view_data(request)
    context = {
        **base_context,
        'products': products,
        'brands': brands
    }
    return render(request, 'store.html', context)


def brand_filter_view(request, slug):
    brand = Brand.objects.get(slug=slug)
    products = Product.objects.filter(brand=brand)
    brands = Brand.objects.all()
    base_context = base_view_data(request)
    context = {
        **base_context,
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
    base_context = base_view_data(request)
    brands = Brand.objects.all()
    context = {
        **base_context,
        'products': products,
        'brands': brands,
    }
    return render(request, 'store.html', context)


def cart_view(request):
    if request.user.is_authenticated:
        cart_info = CartAuthenticatedUser(request).get_cart_info()

        context = {
            'order': cart_info['order'],
            'order_products': cart_info['order_products'],
            'total_cart_price': cart_info['total_cart_price'],
            'total_product_number': cart_info['total_product_number'],
        }
        return render(request, 'cart.html', context)
    else:
        return redirect('login')


def to_cart(request, product_id, action):
    if request.user.is_authenticated:
        CartAuthenticatedUser(request, product_id, action)
        page = request.META.get('HTTP_REFERER')
        return redirect(page)
    else:
        return redirect('login')


def create_checkout_session(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    cart_info = CartAuthenticatedUser(request).get_cart_info()
    total_price = cart_info['total_cart_price']
    total_quantity = cart_info['total_cart_product']
    session = stripe.checkout.Session.create(
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': "Online Shop Product"
                },
                'unit_amount': int(total_price * 100),
            },
            'quantity': 1
        }],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('success_payment')),
        cancel_url=request.build_absolute_uri(reverse('cart'))
    )
    return redirect(session.url, 303)


def success_payment(request):
    return render(request, 'shop/success.html')


def subscription_view(request):
    page = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        data = {
            'email': request.POST.get('email')
        }
        email = EmailForm(data)
        if email.is_valid():
            email.save()
            send_subscription_email(email.cleaned_data.get('email'))
    return redirect(page)


def wishlist_view(request):
    if request.user.is_authenticated:
        wishlist_info = UserWishlistManager(request).get_wishlist_info()
        wishlist_products = wishlist_info['wishlist_products']
        base_context = base_view_data(request)
        context = {
            **base_context,
            'wishlist_products': wishlist_products
        }
        return render(request, 'wishlist.html', context)
    return redirect('login')


def to_wishlist(request, slug, action):
    if request.user.is_authenticated:
        UserWishlistManager(request, slug, action)
        page = request.META.get('HTTP_REFERER')
        return redirect(page)
    else:
        return redirect('login')

