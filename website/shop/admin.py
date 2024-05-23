from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Product, ProductImage, Brand, Country, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['get_image', 'id', 'name', 'created_at']
    list_display_links = ['name']
    search_fields = ['name']
    prepopulated_fields = {'slug': ['name']}

    def get_image(self, category):
        if category.image:
            return mark_safe(f'<img src="{category.image.url}" width="70px" style="border-radius: 15px;">')
        else:
            return 'Image not found'

    get_image.short_description = 'Rasmi'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['get_image', 'id', 'name', 'added_at']
    list_display_links = ['name']
    search_fields = ['name']
    sortable_by = ['added_at', 'name']

    prepopulated_fields = {'slug': ['name']}

    def get_image(self, product):
        if product.productimage_set.first:
            return mark_safe(f'<img src="{product.productimage_set.first().image.url}" width="70px" style="border-radius: 15px;">')
        else:
            return 'Image not found'

    get_image.short_description = 'Rasmi'


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'product']
    list_display_links = ['id']
    sortable_by = ['product']


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'company_name']
    list_display_links = ['name']
    search_fields = ['name']
    prepopulated_fields = {'slug': ['name']}
    sortable_by = ['name']


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['name']
    search_fields = ['name']
    sortable_by = ['name']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'content']
    list_display_links = ['id']
    search_fields = ['content']
    sortable_by = ['created_at']

