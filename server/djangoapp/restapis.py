import requests
import json
# import related models here
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    dealers = get_request(url)
    if dealers:
        # Get the row list in JSON as dealers
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"], id=dealer["id"], lat=dealer["lat"], long=dealer["long"], short_name=dealer["short_name"], st=dealer["st"], zip=dealer["zip"])
            results.append(dealer_obj)

    print(results)
    return results

def get_dealer_reviews_from_cf(url, dealer_id, **kwargs):
    results = []
    # Call get_request with a URL parameter
    reviews = get_request(url, dealerId=dealer_id)
    print(reviews)
    if reviews:
        # Get the row list in JSON as reviews
        # For each review object
        for review in reviews:
            # Get its content in `doc` object
            keys = (
                "dealership",
                "name",
                "purchase",
                "car_model",
                "car_year",
                "id",
                "purchase_date",
                "review",
                "car_make"
                )
            new_review = dict()
            for k in keys:
                if(k in review): new_review[k] = review[k]
                else: new_review[k] = None
            review_obj = DealerReview(dealership=new_review["dealership"], name=new_review["name"], purchase=new_review["purchase"], car_model=new_review["car_model"], car_year=new_review["car_year"], id=new_review["id"], purchase_date=new_review["purchase_date"], sentiment=None, review=new_review["review"], car_make=new_review["car_make"])
            review_obj.sentiment = analyze_review_sentiments(text=review_obj.review, version="2022-04-07", features="sentiment")
            results.append(review_obj)
    return results
# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(**kwargs):
    api_key = "XiBXKLTNKEWfQOxQGEKZIZqnoomvnuCEFqjMdj3VltkD"
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/f7bcf578-80b5-4b79-917f-a3a80e26632f/v1/analyze"
    params = dict()
    params["text"] = kwargs["text"]
    params["version"] = kwargs["version"]
    params["features"] = kwargs["features"]
    response = requests.get(url, params=params, headers={'Content-Type': 'application/json'}, auth=HTTPBasicAuth('apikey', api_key))
    json_data = json.loads(response.text)
    if ("sentiment" in json_data):
        text = json_data["sentiment"]["document"]["label"]
        return text
    else: return "neutral"

def post_request(url, json_payload, **kwargs):
    try:
        response = requests.post(url, params=kwargs, json=json_payload)
        return response.text
    except:
        print("error")
