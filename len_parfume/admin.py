from django import forms
from django.contrib import admin

from .models import *

# class SizeInline(admin.TabularInline):
#     verbose_name='Размеры'
#     model=Size

# class SizeAdmin(admin.ModelAdmin):
#     inlines = [
#         SizeInline,
#         ]

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':("name",)}
    list_display= ( 'id','name')
    list_display_links=('id','name')


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':("title",)}
    list_display= ( 'id','title', 'category', 'price', 'available')
    list_display_links=('id','title')
    list_editable=('available',)

    search_fields=('title',)
    readonly_fields = ('views',)


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':("title",)}
    list_display= ( 'id','title')
    list_display_links=('id','title')




admin.site.register(Category,CategoryAdmin)
admin.site.register(Size)
admin.site.register(Product,ProductAdmin)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(Order)
admin.site.register(Customer)
admin.site.register(Whishlist)
admin.site.register(Rewiews)
admin.site.register(Tag,TagAdmin)




admin.site.site_title="Администрация магазина"
admin.site.site_header="Магазин"