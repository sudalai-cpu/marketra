from django.urls import path
from . import views

app_name = 'marketra'

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
]
