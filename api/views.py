from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


def home_page(request: HttpRequest) -> HttpResponse:
	URL='https://cloud-api.yandex.net/v1/disk/resources'
	HEADERS={'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': 'OAuth '}
	
	return render(request, "api/index.html", {})


def token_page(request: HttpRequest) -> HttpResponse:
	return render(request, "api/token.html", {})