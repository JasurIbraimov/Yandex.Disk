from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

def home_page(request: HttpRequest) -> HttpResponse:
	return render(request, "api/index.html", {})