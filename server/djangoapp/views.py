# Uncomment the required imports before adding the code
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import CarMake, CarModel
from .populate import initiate
import logging
import json

# from django.http import HttpResponseRedirect, HttpResponse
# from django.contrib import messages
# from datetime import datetime




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

def get_cars(request):
    count = CarMake.objects.filter().count()
    print(count)
    if(count == 0):
        initiate()
    car_models = CarModel.objects.select_related('car_make')
    cars = []
    for car_model in car_models:
        cars.append({"CarModel": car_model.name, "CarMake": car_model.car_make.name})
    return JsonResponse({"CarModels":cars})
# Create a `get_dealer_reviews` view to render the reviews of a dealer
# def get_dealer_reviews(request,dealer_id):
# ...

# Create a `get_dealer_details` view to render the dealer details
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request):
# ...
