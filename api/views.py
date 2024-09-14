from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
import requests
import json


def home_page(request: HttpRequest) -> HttpResponse:
	token = request.GET.get("token")
	context = {
		"token": token
	}
	if token:
		headers = {'Content-Type': 'application/json',
				   'Accept': 'application/json', 'Authorization': f'OAuth {token}'}
		disk_data_url = "https://cloud-api.yandex.net/v1/disk"
		disk_items_url = "https://cloud-api.yandex.net/v1/disk/resources/files"

		disk_data_response = requests.get(disk_data_url, headers=headers)
		disk_data = disk_data_response.json()

		disk_items_response = requests.get(disk_items_url, headers=headers)
		disk_items_data = disk_items_response.json()

		context["disk"] = disk_data
		context["items_data"] = disk_items_data

	return render(request, "api/index.html", context)


def token_page(request: HttpRequest) -> HttpResponse:
	return render(request, "api/token.html", {})


def download_view(request: HttpRequest) -> HttpResponse:
	token = request.GET.get("token")
	path=request.GET.get("path")
	headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'OAuth {token}'}
	download_url = f"https://cloud-api.yandex.net/v1/disk/resources/download?path={path}"
	response = requests.get(download_url,headers=headers)
	data = response.json()
	return redirect(data["href"])     