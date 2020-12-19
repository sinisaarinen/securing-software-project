from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views

urlpatterns = [
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', views.RegisterPage.as_view(), name='signup'),
    path('accounts/login/', views.LoginPage.as_view(), name='login'),
    path('', views.index, name='index'),
    path('post/', views.postMessage, name='post'),
    path('findById/', views.findById, name='findById'),
]

