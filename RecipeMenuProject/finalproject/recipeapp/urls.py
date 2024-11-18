from django.contrib import admin
from django.urls import path
from recipeapp import views
from chatquestions import views as qviews
from images import views as iviews

urlpatterns = [
    path('home/', views.recipelist_page, name="recipes"),
    path('', views.login_page, name="login"),
    path('register/', views.register_page, name="register"),
    path('add_recipe/', views.add_recipe, name='add_recipe'),
    path('update_recipe/<id>', views.update_recipe, name='update_recipe'),
    path('chatbot/', qviews.questions_chatbot, name='chatbot'),
    path('images/', iviews.generate_image_from_txt, name='images'),
    path('admin/', admin.site.urls),
]