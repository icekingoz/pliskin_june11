import playwright
from playwright.async_api import APIRequestContext, Playwright
import pytest

# Ping
# Ping - HealthCheck
# A simple health check endpoint to confirm whether the API is up and running.

# get
# https://restful-booker.herokuapp.com/ping
# Ping server:
# curl -i https://restful-booker.herokuapp.com/ping
# Success 200
# Field	Type	Description
# OK	String	
# Default HTTP 201 response

# Response:
# HTTP/1.1 201 Created

@pytest.fixture(scope="session")
def api_context(playwright: Playwright):
    ctx = playwright.request.new_context(base_url="https://restful-booker.herokuapp.com")
    yield ctx
    ctx.dispose()

def test_ping(api_context: APIRequestContext):
    response = api_context.get("/ping")    
    
    assert response.status == 201