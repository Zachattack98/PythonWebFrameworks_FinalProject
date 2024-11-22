from django.test import TestCase
from .models import Recipe


# Test model
class RecipeModelTest(TestCase):
    def setUpTestData(self):
        Recipe.objects.create(
            name='Pumpkin Bars',
            ingredients='Pumpkin Mix, 2 Cup Milk, 4 Eggs, Sugar, Flour, Baking Soda, and Vanilla.',
            description='Beat everything into a bowl, pour into a pan, and bake in oven at 350 degrees.',
            cooktime = 85
        )

    # test to see if the recipe's name is initialized as expected
    def test_recipe_name(self):
        recipe = Recipe.objects.get(id=1)
        field_label = recipe._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    # test to see if the length of the name field is a maximum of 100 characters
    def test_recipe_name_max_length(self):
        recipe = Recipe.objects.get(id=1)
        max_length = recipe._meta.get_field('name').max_length
        self.assertEqual(max_length, 50, 'name has over 50 characters')

    # test to see if the length of the name field is a maximum of 100 characters
    def test_recipe_ingredients_max_length(self):
        recipe = Recipe.objects.get(id=1)
        max_length = recipe._meta.get_field('name').max_length
        self.assertEqual(max_length, 250, 'ingredients has over 250 characters')

    # test to see if the length of the name field is a maximum of 100 characters
    def test_recipe_descip_max_length(self):
        recipe = Recipe.objects.get(id=1)
        max_length = recipe._meta.get_field('name').max_length
        self.assertEqual(max_length, 500, 'name has over 500 characters')

    # test to see if the cooking_time field is an integer
    def test_cooking_time_is_integer(self):
        recipe = Recipe.objects.get(id=1)
        cooking_time = recipe.cooktime
        self.assertIs(type(cooking_time), int, 'cooking_time is not a number')