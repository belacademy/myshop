from django.contrib import admin
from .models import Category, Product, Token, Notification


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price',
                    'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ['id', 'token']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['text', 'date', 'seen']
