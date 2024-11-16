from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *

#Function that defines a home page
def recipelist_page(request):
    # Render the home page template (GET request)
    return render(request, 'homepage.html')

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