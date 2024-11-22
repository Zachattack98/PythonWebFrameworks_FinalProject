from django.db import models
from django.contrib.auth.models import User

#Model for information on recipes
class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=50, default='something')
    ingredients = models.CharField(max_length=250, default='something')
    description = models.CharField(max_length=500, default='something')
    cooktime = models.IntegerField(help_text='in min', default=0)

#Model for images of recipes found online
class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)