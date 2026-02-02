from django.urls import path
from . import views

app_name = 'marketra'

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('collection/add/<int:pk>/', views.add_to_collection, name='add_to_collection'),
    path('collection/remove/<int:pk>/', views.remove_from_collection, name='remove_from_collection'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('featured/', views.featured_view, name='featured'),
    path('search/', views.search_view, name='search'),
    path('collection/', views.collection_view, name='collection'),
    path('recommendations/', views.recommendations_view, name='recommendations'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/profile/', views.profile_view, name='profile'),
    path('dashboard/orders/', views.orders_view, name='orders'),
    path('dashboard/wishlist/', views.wishlist_view, name='wishlist'),
    path('dashboard/style-profile/', views.style_profile_view, name='style_profile'),
]
