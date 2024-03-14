from django.urls import path
from . import views

urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path('manage_products', views.manage_products, name='manage_products'),
    path('add_product', views.add_product, name='add_product'),
    path('manage/<str:id>', views.manage, name='manage'),
    path('delete_product/<str:id>', views.delete_product, name='delete_product'),
    path('profile', views.profile, name='profile'),
]