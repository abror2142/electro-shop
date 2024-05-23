from django.urls import path
from .views import (index_view, detail_view, category_filter_view,
                    store_view, sort_by_price, brand_filter_view, cart_view,
                    to_cart, create_checkout_session, success_payment, subscription_view, to_wishlist, wishlist_view)


urlpatterns = [
    path('', index_view, name='index'),
    path('product/<slug:slug>/', detail_view, name='detail'),
    path('store/', store_view, name='store'),
    path('store/<slug:slug>/', category_filter_view, name='category_filter'),
    path('brand/<slug:slug>/', brand_filter_view, name='brand_filter'),
    path('order/<str:order>/', sort_by_price, name='sort_by_price'),
    path('cart/', cart_view, name='cart'),
    path('cart/<int:product_id>/<str:action>/', to_cart, name='to_cart'),
    path('checkout/', create_checkout_session, name='checkout'),
    path('success/', success_payment, name='success_payment'),
    path('subscribe/', subscription_view, name='subscribe'),
    path('wishlist/', wishlist_view, name='wishlist'),
    path('wishlist/<slug:slug>/<str:action>/', to_wishlist, name='to_wishlist')
]