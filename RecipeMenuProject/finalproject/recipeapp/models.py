from django.db import models
from django.contrib.auth.models import User

#Model for information on recipes
class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    recipe_name = models.CharField(max_length=50, default='something')
    recipe_ingredients = models.CharField(max_length=250, default='something')
    recipe_description = models.CharField(max_length=500, default='something')