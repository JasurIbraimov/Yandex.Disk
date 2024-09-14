from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import requests

def home_page(request: HttpRequest) -> HttpResponse:
	token = request.GET.get("token");
	context = {}
	if token :
		print(token)
		url='https://cloud-api.yandex.net/v1/disk'
		headers={'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'OAuth {token}'}
		response = requests.get(url, headers=headers)
		data = response.json()
		context["data"] = data 
	return render(request, "api/index.html", context)


def token_page(request: HttpRequest) -> HttpResponse:
	return render(request, "api/token.html", {})