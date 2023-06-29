from django.urls import path , include
from . import views
from .views import *

urlpatterns = [
    path('', views.index, name='index'),
    path('market/', views.market, name='market'),
    path('create_listing/', views.create_listing, name='create_listing'),
    path('listings/', views.listing_list, name='listing_list'),
    path('delete_listing/', views.delete_all_listings, name='delete_listing'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('edit_user/', views.edit_user, name='edit_user'),
    path('i18n/', include('django.conf.urls.i18n')),  # Django's i18n URLs
    path('listing/<int:id>/', views.listing_detail, name='listing_detail'),
    path('bookmark/', views.bookmark, name='bookmark'),
    path('delete/<int:listing_id>/', delete_listing, name='delete_listing'),
]