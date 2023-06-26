from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.index, name='index'),
    path('market/', views.market, name='market'),
    path('upload/', image_upload_view, name='image_upload'),
]