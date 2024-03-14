from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('login/', views.login_, name='login'),
    path('logout', views.logout_, name='logout'),
    path('verify/<str:uidb64>/<str:token>/', views.activate, name='activate'),
    path('seller', views.create_seller, name='seller'),
    path('medic_tools', views.medic_tools, name='medic_tools'),
    path('chatbot', views.chatbot, name='chatbot'),
    path('predict', views.predict, name='predict'),
    path('success', views.success, name='success'),
    path('cancel', views.cancel, name='cancel'),
]