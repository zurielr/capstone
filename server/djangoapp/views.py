# Uncomment the required imports before adding the code
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
# from django.shortcuts import render
# from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
# from django.shortcuts import get_object_or_404, render, redirect
# from django.contrib.auth import logout
# from django.contrib import messages
# from datetime import datetime

from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

# from .populate import initiate


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

def home(request):
    return render(request, "Home.html")

# ...existing code...
# Create a `login_request` view to handle sign in request
def login_user(request):
    context = {}
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['password']
        # Try to check if provided credentials can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect('home')  # Redirect to home page after login
        else:
            context['error'] = "Invalid username or password."
            return render(request, 'login.html', context)
    else:
        return render(request, 'login.html', context)

@csrf_exempt
def login_user(request):
    context = {}
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                context['error'] = "Invalid username or password."
        else:
            context['error'] = "Please enter both username and password."
    return render(request, 'login.html', context)
# Create a `logout_request` view to handle sign out request
# def logout_request(request):
def logout_request(request):
    logout(request)
    return redirect('home')

# Create a `registration` view to handle sign up request
# @csrf_exempt

def register_user(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'register.html', context)
    elif request.method == 'POST':
        # Get user information from request.POST
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except User.DoesNotExist:
            logger.debug(f"{username} is a new user")
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                password=password
            )
            # Login the user and redirect to home page
            login(request, user)
            return redirect('home')
        else:
            context['error'] = "User already exists."
            return render(request, 'register.html', context)

# # Update the `get_dealerships` view to render the index page with
# a list of dealerships
# def get_dealerships(request):
# ...

# Create a `get_dealer_reviews` view to render the reviews of a dealer
# def get_dealer_reviews(request,dealer_id):
# ...

# Create a `get_dealer_details` view to render the dealer details
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request):
# ...
