from django.urls import path
from . import views

app_name = 'marketra'

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('collection/toggle/<int:pk>/', views.toggle_collection, name='toggle_collection'),
    path('collection/remove/<int:pk>/', views.remove_from_collection, name='remove_from_collection'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('featured/', views.featured_view, name='featured'),
    path('search/', views.search_view, name='search'),
    path('collection/', views.collection_view, name='collection'),
    path('recommendations/', views.recommendations, name='recommendations'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/profile/', views.profile_view, name='profile'),
    path('dashboard/orders/', views.orders_view, name='orders'),
    path('dashboard/wishlist/', views.wishlist_view, name='wishlist'),
    path('dashboard/wishlist/toggle/<int:pk>/', views.toggle_wishlist, name='toggle_wishlist'),
    path('dashboard/wishlist/remove/<int:pk>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('dashboard/style-profile/', views.style_profile_view, name='style_profile'),
]
