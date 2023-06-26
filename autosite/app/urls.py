from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.index, name='index'),
    path('market/', views.market, name='market'),
    path('create_listing/', views.create_listing, name='create_listing'),
    path('listings/', views.listing_list, name='listing_list'),
]