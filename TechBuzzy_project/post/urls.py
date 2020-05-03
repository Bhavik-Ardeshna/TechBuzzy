from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('',views.PostList.as_view(),name='all'),
    path('new/',views.PostCreateView.as_view(),name='create'),
    path('by/<username>/',views.UserPostList.as_view(),name='for_user'),
    path('by/<username>/<int:pk>/',views.PostDetailView.as_view(),name='single'),
    path('delete/<int:pk>/',views.PostDeleteView.as_view(),name='delete'),
]