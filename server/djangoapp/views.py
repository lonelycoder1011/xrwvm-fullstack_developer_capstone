from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.http import JsonResponse
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .populate import initiate
from .models import CarMake, CarModel
from .restapis import get_request, analyze_review_sentiments, post_review

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

@csrf_exempt
def login_user(request):
    """
    Handle sign-in requests.
    """
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    
    user = authenticate(username=username, password=password)
    response_data = {"userName": username}

    if user is not None:
        login(request, user)
        response_data["status"] = "Authenticated"
        
    return JsonResponse(response_data)


@csrf_exempt
def logout_request(request):
    """
    Handle sign-out requests.
    """
    if request.method == "GET":
        logout(request)
        request.session.flush()
        return JsonResponse({"status": True, "userName": ""})

    return JsonResponse({"status": False, "message": "Invalid request method."})


@csrf_exempt
def registration(request):
    """
    Handle user registration requests.
    """
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']
    username_exist = False

    try:
        User.objects.get(username=username)
        username_exist = True
    except Exception:
        logger.debug(f"{username} is a new user")

    if not username_exist:
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=email
        )
        login(request, user)
        return JsonResponse({"userName": username, "status": "Authenticated"})

    return JsonResponse({"userName": username, "error": "Already Registered"})


def get_cars(request):
    """
    Retrieve car models along with their associated car makes.
    If no car makes exist, populate the database.
    """
    if CarMake.objects.count() == 0:
        initiate()

    car_models = CarModel.objects.select_related('car_make')
    cars = [
        {
            "CarMake": car_model.car_make.name,
            "CarModel": car_model.name,
            "Year": car_model.year,
            "Type": car_model.get_type_display(),
        }
        for car_model in car_models
    ]
    return JsonResponse({"CarModels": cars})


def get_dealerships(request, state="All"):
    """
    Retrieve a list of dealerships.
    If a state is provided, filter dealerships by state.
    """
    endpoint = "/fetchDealers" if state == "All" else f"/fetchDealers/{state}"
    dealerships = get_request(endpoint)
    
    return JsonResponse({"status": 200, "dealers": dealerships})


def get_dealer_reviews(request, dealer_id):
    """
    Retrieve reviews for a given dealer.
    """
    if dealer_id:
        endpoint = f"/fetchReviews/dealer/{dealer_id}"
        reviews = get_request(endpoint)

        if isinstance(reviews, list):
            for review_detail in reviews:
                try:
                    sentiment_response = analyze_review_sentiments(
                        review_detail.get('review', '')
                    )
                    review_detail['sentiment'] = sentiment_response.get(
                        'sentiment', 'neutral'
                    ).lower()
                except KeyError as e:
                    review_detail['sentiment'] = 'neutral'
                    logger.error(f"KeyError in sentiment analysis: {str(e)}")

            return JsonResponse({"status": 200, "reviews": reviews})

        return JsonResponse({"status": 400, "message": "Invalid reviews format"})

    return JsonResponse({"status": 400, "message": "Bad Request"})


def get_dealer_details(request, dealer_id):
    """
    Retrieve details for a specific dealer.
    """
    if dealer_id:
        try:
            endpoint = f"/fetchDealer/{dealer_id}"
            dealership = get_request(endpoint)

            if not dealership:
                return JsonResponse(
                    {"status": 404, "message": "Dealer not found"}, status=404
                )

            return JsonResponse({"status": 200, "dealer": dealership}, status=200)

        except Exception as e:
            return JsonResponse(
                {"status": 500, "message": f"Internal Server Error: {str(e)}"},
                status=500
            )

    return JsonResponse(
        {"status": 400, "message": "Bad Request: Dealer ID is required"},
        status=400
    )


@csrf_exempt
def add_review(request, dealer_id):
    """
    Submit a review for a dealer.
    """
    if request.user.is_authenticated:
        try:
            data = json.loads(request.body)
            review = {
                "dealership": dealer_id,
                "name": request.user.username,
                "purchase": data.get("purchase", False),
                "review": data["review"],
                "purchase_date": data.get("purchase_date", ""),
                "car_make": data.get("car_make", ""),
                "car_model": data.get("car_model", ""),
                "car_year": data.get("car_year", ""),
            }
            post_review(review)
            return JsonResponse(
                {"status": 200, "message": "Review posted successfully"}
            )
        except Exception as e:
            logger.error(f"Error posting review: {str(e)}")
            return JsonResponse({"status": 500, "message": str(e)})

    return JsonResponse({"status": 403, "message": "Unauthorized"})
