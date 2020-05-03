from django.contrib.auth.views import LoginView,LogoutView
from django.urls import path
from .views import SignUp

app_name = 'account'

urlpatterns = [
    path('login/',LoginView.as_view(template_name = 'account/login.html'),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('signup/',SignUp.as_view(),name='signup'),
]