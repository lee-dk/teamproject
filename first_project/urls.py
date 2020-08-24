from django.urls import path
from . import views

urlpatterns = [
    path("main/", views.main, name="main"),
    path('newLogin_1/', views.newLogin_1, name="newLogin_1"),
    # path('register/', views.register, name="register"),
]