from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required

urlpatterns = [
path('', views.index, name='index'),
path('login/', views.login, name="login"),
path('signup/', views.signup, name="signup"),
path('shipping', views.shipping, name="shipping"),
path('admin_homepage/', views.admin_homepage, name="admin_homepage"),
path('special_offer/', views.special_offer, name='special_offer'),
path('add_to_cart/<str:product_id>/', views.add_to_cart, name='add_to_cart'),
]






