from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

def homePageView(request: HttpRequest) -> HttpResponse:
    """Respond to an HTTP request with a simple web page.

    Args:
        request (HttpRequest): request being sent (automatically created).
        Contains meta-data, headers, cookies, user information... etc.

    Returns:
        HttpResponse: render a response
    """
    return HttpResponse('Hello, peeps')