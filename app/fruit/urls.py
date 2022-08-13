
from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('mystore', views.mystore, name='mystore'),
    path('profile', views.profile, name='profile'),
    path('products/create', views.create_product, name='product_create'),
    path('products/<pk>/sku/create', views.create_sku, name='create_sku'),
    path('sku/<pk>', views.edit_sku, name='edit_sku'),
    path('products/', views.product_index, name='product_index'),
    path('products/<pk>', views.product_edit, name='product_edit'),
    path('sales/', views.sale_index, name='sale_index'),
    path('sales/<pk>', views.sale_edit, name='sale_edit'),
    path('inbox/', views.inbox_index, name='inbox_index'),
    path('inbox/<pk>', views.inbox_edit, name='inbox_edit'),
    path('vendor/', views.vendor_index, name='vendor_index'),
    path('vendor/create', views.vendor_create, name='vendor_create'),
    path('vendor/<pk>', views.vendor_edit, name='vendor_edit'),
    path('vendor/<pk>/product/create', views.vendorproduct_create, name='vendorproduct_create'),
    path('vendorproduct/<pk>', views.vendorproduct_edit, name='vendorproduct_edit'),
    path('vendororder/', views.vendororder_index, name='vendororder_index'),
    path('vendororder/create', views.vendororder_create, name='vendororder_create'),
    path('vendororder/<pk>', views.vendororder_edit, name='vendororder_edit'),
    path('signup', views.signup, name='signup'),
    path('account_activation_sent', views.account_activation_sent, name='account_activation_sent'),
    path(r'activate/<uidb64>/<token>/',
        views.activate, name='activate'),

]

app_name = 'fruit'
