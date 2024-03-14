from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home, name='home'),
    path('user_profile', views.user_profile, name='user_profile'),
    path('product/<str:id>', views.single_product, name='single_product'),
    path('collection', views.collection, name='collection'),
    path('add_to_collection/<str:id>', views.add_to_collection, name='add_to_collection'),
    path('remove_from_collection/<str:id>', views.remove_from_collection, name='remove_from_collection'),
    path('checkout', views.start_checkout, name='checkout')
]