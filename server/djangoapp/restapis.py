# Uncomment the imports below before you add the function code
import requests
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Retrieve URLs from environment variables, with default fallbacks
backend_url = os.getenv('backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv('sentiment_analyzer_url', default="http://localhost:5050/")

def get_request(endpoint, **kwargs):
    """
    Sends a GET request to the backend URL with optional query parameters.

    Args:
        endpoint (str): The API endpoint to be appended to the backend URL.
        **kwargs: Optional query parameters to be included in the request.

    Returns:
        dict: JSON response from the server.
    """
    # Construct query parameters from kwargs
    params = "&".join(f"{key}={value}" for key, value in kwargs.items())
    request_url = f"{backend_url}{endpoint}?{params}" if params else f"{backend_url}{endpoint}"

    print(f"GET from {request_url}")
    try:
        # Call GET method of requests library
        response = requests.get(request_url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx, 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Network exception occurred: {e}")
        return {"error": "Network exception occurred"}

def analyze_review_sentiments(text):
    try:
        if text:
            url = os.getenv(
                'SENTIMENT_ANALYZER_URL', 
                'https://sentianalyzer.1r729rxqpt17.us-south.codeengine.appdomain.cloud/'
            )
            response = requests.get(
                f"{url}analyze/{text}", 
                headers={'Content-Type': 'application/json'}
            )
            
            # Handle different response formats
            if response.status_code == 200:
                result = response.json()
                return {
                    'sentiment': result.get('sentiment', 'neutral'),
                    'confidence': result.get('confidence', 0)
                }
            return {'sentiment': 'neutral', 'confidence': 0}
        return {'sentiment': 'neutral', 'confidence': 0}
    except Exception as e:
        print(f"Sentiment Analysis Error: {str(e)}")
        return {'sentiment': 'neutral', 'confidence': 0}

def post_review(data_dict):
    """
    Sends a POST request to insert a new review.

    Args:
        data_dict (dict): The data to be sent in the POST request.

    Returns:
        dict: JSON response from the server.
    """
    request_url = f"{backend_url}/insert_review"
    
    print(f"POST to {request_url} with data: {data_dict}")
    try:
        # Call POST method of requests library
        response = requests.post(request_url, json=data_dict)
        response.raise_for_status()  # Raise HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Network exception occurred: {e}")
        return {"error": "Network exception occurred"}