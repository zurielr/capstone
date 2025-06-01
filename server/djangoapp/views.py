# Uncomment the required imports before adding the code
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import CarMake, CarModel, Dealer, Review
from .populate import initiate
from .forms import ReviewForm
import logging
import json
from .restapis import get_request, analyze_review_sentiments, post_review
# from django.http import HttpResponseRedirect, HttpResponse
# from django.contrib import messages
# from datetime import datetime


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

def home(request):
    return render(request, "Home.html")


def index(request):
    return render(request, 'index.html')

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
def get_dealerships(request):
    # Fetch dealerships from the API
    dealerships = get_request("/fetchDealerships")
    if dealerships:
        return JsonResponse(dealerships, safe=False)
    else:
        return JsonResponse({"error": "No dealerships found"}, status=404)

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
def get_dealer_reviews(request, dealer_id):
    # Fetch reviews for the dealer
    reviews = get_request(f"/fetchReviews/dealer/{dealer_id}")
    review_details = []
    if reviews:
        for review in reviews:
            sentiment = analyze_review_sentiments(review.get("review", ""))
            review_detail = {
                "id": review.get("id"),
                "name": review.get("name"),
                "dealership": review.get("dealership"),
                "review": review.get("review"),
                "purchase": review.get("purchase"),
                "purchase_date": review.get("purchase_date"),
                "car_make": review.get("car_make"),
                "car_model": review.get("car_model"),
                "car_year": review.get("car_year"),
                "sentiment": sentiment
            }
            review_details.append(review_detail)
    return JsonResponse(review_details, safe=False)

# Create a `get_dealer_details` view to render the dealer details
# def get_dealer_details(request, dealer_id):


def dealer_detail(request, dealer_id):
    dealer = get_object_or_404(Dealer, id=dealer_id)
    reviews = Review.objects.filter(dealer=dealer)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.dealer = dealer
            review.name = request.user.username  # Assuming a logged-in user
            review.save()
            return redirect("dealer_detail", dealer_id=dealer.id)
    else:
        form = ReviewForm()

    return render(request, "dealer_detail.html", {"dealer": dealer, "reviews": reviews, "form": form})

# Create a `add_review` view to submit a review
# def add_review(request):
def add_review(request):
    if(request.user.is_anonymous == False):
        data = json.loads(request.body)
        try:
            response = post_review(data)
            return JsonResponse({"status":200})
        except:
            return JsonResponse({"status":401,"message":"Error in posting review"})
    else:
        return JsonResponse({"status":403,"message":"Unauthorized"})



def post_review(request, dealer_id):
    dealer = get_object_or_404(Dealer, pk=dealer_id)
    # If you have a CarModel model, fetch car models for the dropdown
    car_models = []  # Replace with CarModel.objects.all() if available

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            # Save the review (implement your Review model accordingly)
            # Example:
            # Review.objects.create(
            #     name=request.user.get_full_name() or request.user.username,
            #     dealership=dealer,
            #     review=form.cleaned_data['review'],
            #     purchase=True,
            #     purchase_date=form.cleaned_data['purchase_date'],
            #     car_make=form.cleaned_data['car_make'],
            #     car_model=form.cleaned_data['car_model'],
            #     car_year=form.cleaned_data['car_year'],
            # )
            return redirect('djangoapp:dealer_detail', dealer_id=dealer.id)
    else:
        form = ReviewForm()

    return render(request, "post_review.html", {
        "dealer": dealer,
        "form": form,
        "car_models": car_models,
    })
