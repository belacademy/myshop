from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('invoices/', views.invoice_list, name='product_list'),
    path('transfers/', views.transfer_list, name='transfer_list'),
    path('notifications/', views.notification_list, name='notification_list'),
    path('notifications/retrive/', views.retrivenotifications, name='retrivenotifications'),
    path('notifications/unseencount/', views.unseencount, name='unseencount'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
]
