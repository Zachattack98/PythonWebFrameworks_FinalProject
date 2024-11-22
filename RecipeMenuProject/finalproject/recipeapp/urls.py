from django.contrib import admin
from django.urls import path
from recipeapp import views

urlpatterns = [
    path('home/', views.recipelist_page, name="recipelists"),
    path('', views.login_page, name="login"),
    path('register/', views.register_page, name="register"),
    path('home/add_recipe/', views.add_recipe, name='add_recipe'),
    path('home/update_recipe/<id>', views.update_recipe, name='update_recipe'),
    path('chatbot/', views.questions_chatbot, name='chatbot'),
    path('images/', views.generate_image_from_txt, name='images'),
    path('admin/', admin.site.urls),
]