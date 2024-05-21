from django.contrib import admin
from .models import UserInfo, Like, WishList, Rating


@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name']
    list_display_links = ['first_name', 'last_name']


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'user']
    list_display_links = ['product']


@admin.register(WishList)
class WishListAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'user']
    list_display_links = ['product']


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'user']
    list_display_links = ['product']

