from django.urls import path
from .views import index_view, detail_view, category_filter_view, store_view, sort_by_price, brand_filter_view


urlpatterns = [
    path('', index_view, name='index'),
    path('product/<slug:slug>/', detail_view, name='detail'),
    path('store/', store_view, name='store'),
    path('store/<slug:slug>/', category_filter_view, name='category_filter'),
    path('brand/<slug:slug>/', brand_filter_view, name='brand_filter'),
    path('order/<str:order>/', sort_by_price, name='sort_by_price'),
]