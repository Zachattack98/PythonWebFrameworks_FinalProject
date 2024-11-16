from django.contrib import admin
from django.urls import path
from recipeapp import views

urlpatterns = [
    path('home/', views.recipelist_page, name="recipes"),
    path('', views.login_page, name="login"),
    path('register/', views.register_page, name="register"),
    path('admin/', admin.site.urls),
]