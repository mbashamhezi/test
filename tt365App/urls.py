from django.urls import path
from . import views

urlpatterns = [
path('', views.index, name='index'),
path('login/', views.login, name="login"),
path('signup/', views.signup, name="signup"),
path('cart/', views.cart, name="cart"),
path('shipping', views.shipping, name="shipping"),
path('admin_homepage/', views.admin_homepage, name="admin_homepage"),
]


