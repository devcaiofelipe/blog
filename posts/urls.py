from django.urls import path
from .views import post_index, post_details, posts_filter, posts_search

urlpatterns = [
    path('', post_index, name='post_index'),
    path('post/<int:post_id>', post_details, name='post_details'),
    path('filter/<str:search>', posts_filter, name='post_filter'),
    path('search/', posts_search, name='post_search'),
]