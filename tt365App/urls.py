from django.urls import path
from . import views

urlpatterns = [
path('', views.index, name='index'),
path('login/', views.login, name="login"),
path('signup/', views.signup, name="signup"),
path('men_fashion/', views.men_fashion, name="men_fashion"),
path('women_fashion/', views.women_fashion, name="women_fashion"),
path('kids_fashion/', views.kids_fashion, name="kids_fashion"),
path('cart/', views.cart, name="cart"),
path('shipping', views.shipping, name="shipping"),
path('admin_homepage/', views.admin_homepage, name="admin_homepage"),
]



