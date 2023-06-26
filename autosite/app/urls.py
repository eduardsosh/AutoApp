from django.urls import path
from . import views
from .views import image_upload_view

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', image_upload_view, name='image_upload'),
]