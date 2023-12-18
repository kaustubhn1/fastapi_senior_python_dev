from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2AuthorizationCodeBearer
import subprocess
from dotenv import load_dotenv
import os
import requests

app = FastAPI()

# Load environment variables from .env file
load_dotenv()
# Shopify API configuration
SHOPIFY_API_URL = os.getenv("SHOPIFY_API_URL")
SHOPIFY_ACCESS_TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN")

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    tokenUrl="token",
    authorizationUrl="authorize",
)

from typing import Callable

def get_shopify_orders(customer_id: int, http_request: Callable) -> str:
    """
    Fetch Shopify orders for a specific customer.

    Parameters:
    - customer_id (int): The ID of the customer for whom orders are to be retrieved.
    - http_request (Callable): A function to make an HTTP request.

    Returns:
    - str: The json response from the Shopify API containing the orders.

    Raises:
    - HTTPException: If the HTTP request fails, a 500 Internal Server Error is raised.
    """

    url = f"{SHOPIFY_API_URL}/customers/{customer_id}/orders.json"
    headers = {"X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN}

    try:
        response = http_request("GET", url, headers=headers)
        response.raise_for_status()  # Check if the request was successful
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch orders: {str(e)}")

def http_request(method: str, url: str, headers: dict):
    return requests.request(method, url, headers=headers)

@app.get("/orders/{customer_id}", response_model=dict)
async def read_orders(customer_id: int):
    """
    Retrieve Shopify orders for a specific customer.

    Parameters:
    - customer_id (int): The ID of the customer for whom orders are to be retrieved.

    Returns:
    - dict: A dictionary containing the retrieved orders.
    """
    
    orders_result = get_shopify_orders(customer_id, http_request)
    return {"orders": orders_result}
