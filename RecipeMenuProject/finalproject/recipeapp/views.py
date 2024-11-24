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
    #Maily for clearing out all recipe data; uncomment to delete all
    #Recipe.objects.all().delete()
    queryset = Recipe.objects.all()
    # Render the home page template (GET request)
    return render(request, 'homepage.html', {'recipes': queryset})

# create recipes page
@login_required(login_url='/')
def add_recipe(request):
    if request.method == 'POST':
        data = request.POST
        new_recipe_name = data.get('name')
        new_recipe_ingredients = data.get('ingredients')
        new_recipe_description = data.get('description')
        new_recipe_cooktime = data.get('cooktime')

        Recipe.objects.create(
            name=new_recipe_name,
            ingredients=new_recipe_ingredients,
            description=new_recipe_description,
            cooktime = new_recipe_cooktime,
        )
        return redirect('/home/')

    queryset = Recipe.objects.all()
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
        chatbot_response = response["choices"][0]["text"]

    return render(request, 'chatbot_questions/mainChat.html', {"response": chatbot_response})

@login_required(login_url='/')
def generate_image_from_txt(request):
    chatbot_response = None
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

        chatbot_response = Image(phrase=user_input)
        chatbot_response.ai_image.save(fname, img_file)
        chatbot_response.save()

    return render(request, "chatbot_images/mainImage.html", {"object:": chatbot_response})