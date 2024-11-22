from django.shortcuts import render, redirect
from django.contrib.auth.models import User
#from django.http import HttpResponse, HttpResponseRedirect
#from django.urls import reverse
from django.template import loader
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from .models import *
import openai, os, requests
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("OPENAPI_KEY")
openai.api_key = api_key

#Function that defines a home page where all recipe lists are displayed
@login_required(login_url='/')
def recipelist_page(request):
    """queryset = Recipe.objects.all().values()
    template = loader.get_template("homepage.html")
    context = {'recipe': queryset}"""
    # Render the home page template (GET request)
    return render(request, 'homepage.html')

"""@login_required(login_url='/')
def add(request):
    template = loader.get_template('add_recipe.html')
    return HttpResponse(template.render({}, request))

@login_required(login_url='/')
def add_recipe(request):
    new_name = request.POST['name']
    new_ingredients = request.POST['ingredients']
    new_description = request.POST['description']
    recipe = Recipe(
        recipe_name=new_name,
        recipe_ingredients=new_ingredients,
        recipe_description=new_description,
    )
    recipe.save()
    return HttpResponseRedirect(reverse('recipelists'))"""

# create recipes page
@login_required(login_url='/')
def add_recipe(request):
    if request.method == 'POST':
        data = request.POST
        recipe_name = data.get('name')
        recipe_ingredients = data.get('ingredients')
        recipe_description = data.get('description')
        recipe_cooktime = data.get('cooktime')
        recipe = Recipe.objects.create(
            name=recipe_name,
            ingredients=recipe_ingredients,
            description=recipe_description,
            cooktime = recipe_cooktime,
        )
        recipe.save()
        return redirect('home/')

    queryset = Recipe.objects.all().values()
    """if request.GET.get('search'):
        queryset = queryset.filter(
            name__icontains=request.GET.get('search'))"""

    context = {'recipe': queryset}
    return render(request, 'add_recipe.html', context)

#Update the recipes data
@login_required(login_url='/')
def update_recipe(request, id):
    queryset = Recipe.objects.get(id=id)

    if request.method == 'POST':
        data = request.POST
        new_name = data.get('name')
        new_ingredients = data.get('ingredients')
        new_description = data.get('description')
        new_cooktime = data.get('cooktime')

        queryset.name = new_name
        queryset.ingredients = new_ingredients
        queryset.description = new_description
        queryset.cooktime = new_cooktime
        queryset.save()
        return redirect('/home/')

    context = {'recipe': queryset}
    return render(request, 'update_recipe.html', context)

#Function that defines a login page
def login_page(request):
    #Check if the HTTP request method is POST (form submission)
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        #Check if a user with the provided username exists
        if not User.objects.filter(username=username).exists():
            #Error message if username does not exist
            messages.error(request, 'Invalid Username')
            return redirect('/')

        #Authenticate the user with the provided username and password
        user = authenticate(username=username, password=password)
        if user is None:
            #Error message if authentication fails
            messages.error(request, "Invalid Username and/or Password!")
            return redirect('/')
        else:
            #Login was successful for user
            login(request, user)
            #Redirect to home page
            return redirect('/home/')

    #Render the login page template (GET request)
    return render(request, 'login.html')

#Function that defines a registration page
def register_page(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        #confirm_email = request.POST.get('confirm_email')
        password = request.POST.get('password')
        #confirm_password = request.POST.get('confirm_password')

        # Check if there already exists a user with the provided
        # username, password, and email
        user = User.objects.filter(username=username)
        if user.exists():
            #Show that the username is already taken
            messages.info(request, "Username is already taken!")
            return redirect('/register/')
        user = User.objects.filter(password=password)
        if user.exists():
            #Show that the password is already taken
            messages.info(request, "Password is already taken!")
            return redirect('/register/')
        user = User.objects.filter(email=email)
        if user.exists():
            #Show that the email is no longer available
            messages.info(request, "Email has already been utilized!")
            return redirect('/register/')
        """
        if email != confirm_email:
            #Show that both emails inputted are different
            messages.info(request, "Emails do not match!")
            return redirect('/register/')
        if password != confirm_password:
            #Show that both passwords inputted are different
            messages.info(request, "Passwords do not match!")
            return redirect('/register/')
        """

        #Create a new User object with the provided information
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email
        )

        #Set the user's password and save the user object
        user.set_password(password)
        user.save()

        #Show that an account has successfully been created
        messages.info(request, "Account created Successfully!")
        return redirect('/home/')

    #Render the registration page template (GET request)
    return render(request, 'register.html')

@login_required(login_url='/')
def questions_chatbot(request):
    chatbot_response = None
    if api_key is not None and request.method == 'POST':
        user_input = request.POST.get('user_input')
        #ensure that only questions pertaining to recipes are asked
        #prompt = f"if the question is related to recipes - answer it: {user_input}, else say: Sorry I can't answer this"
        prompt = user_input
        response = openai.Completion.create(
            engine = 'text-davinci-003',
            prompt = prompt,
            max_tokens = 100, #maximum of 100 characters for search bar
            temperature = 0.5
        )
        print(response)
    return render(request, 'mainChat.html', {})

def generate_image_from_txt(request):
    if api_key is not None and request.method == "POST":
        user_input = request.POST.get('user_input')
        #prompt = f"if the text is related to food - answer it: {user_input}, else say: Sorry I can't show this"

        response = openai.Image.create(
            prompt = user_input,
            size = '256x256'
        )
        img_url = response["data"][0]["url"]

        response = requests.get(img_url)
        img_file = ContentFile(response.content)

        count = Image.objects.count() + 1
        fname = f"image-{count}.jpg"

        obj = Image(phrase=user_input)
        obj.ai_image.save(fname, img_file)
        obj.save()

        print(obj)

    return render(request, "mainImage.html", {})