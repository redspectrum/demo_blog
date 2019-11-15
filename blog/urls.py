from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', welcome, name='home'),
    path('posts/', posts, name='posts'),
    path('form/', image_form, name='image_form'),
    path('upload/', image_upload, name='image_upload'),


    path('create_posts/', post_create, name='post_create_url'),
    path('delete_picture/<str:url>', delete_picture, name='delete_picture'),
    path('create_collection/', create_collection, name='create_collection'),

    path('post/<str:slug>', post, name='post'),
    path('collection/<str:slug>', collection, name='collection'),
]
