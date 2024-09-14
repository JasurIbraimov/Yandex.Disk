from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseServerError
import requests
from django.template import RequestContext
from io import BytesIO
from zipfile import ZipFile
import logging


def handler500(request):
    return render(request, "api/500.html", status=500)


def home_page(request: HttpRequest) -> HttpResponse:
    try:
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
            disk_data_response.raise_for_status()
            disk_data = disk_data_response.json()

            disk_items_response = requests.get(disk_items_url, headers=headers)
            disk_items_response.raise_for_status()
            disk_items_data = disk_items_response.json()

            context["disk"] = disk_data
            context["items_data"] = disk_items_data
        return render(request, "api/index.html", context)
    except requests.RequestException as e:
        logging.error(f"Request error: {e}")
        return HttpResponseServerError("Ошибка при запросе к Yandex Disk API.")
    except ValueError as e:
        logging.error(f"JSON decode error: {e}")
        return HttpResponseServerError("Ошибка при обработке ответа.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return HttpResponseServerError("Что-то пошло не так...")


def token_page(request: HttpRequest) -> HttpResponse:
    return render(request, "api/token.html", {})


def download_view(request: HttpRequest) -> HttpResponse:
    try:
        token = request.GET.get("token")
        path = request.GET.get("path")
        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json', 'Authorization': f'OAuth {token}'}
        download_url = f"https://cloud-api.yandex.net/v1/disk/resources/download?path={path}"
        response = requests.get(download_url, headers=headers)
        response.raise_for_status()
        data = response.json()

        return redirect(data.get("href"))
    except requests.RequestException as e:
        logging.error(f"Request error: {e}")
        return HttpResponseServerError("Ошибка при запросе к Yandex Disk API.")
    except ValueError as e:
        logging.error(f"JSON decode error: {e}")
        return HttpResponseServerError("Ошибка при обработке ответа.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return HttpResponseServerError("Что-то пошло не так...")


def download_all_view(request: HttpRequest) -> HttpResponse:
    try:
        token = request.GET.get("token")
        pathes = request.GET.get("pathes").split(",")
        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json', 'Authorization': f'OAuth {token}'}

        download_links = []
        for path in pathes:
            download_url = f"https://cloud-api.yandex.net/v1/disk/resources/download?path={path}"
            response = requests.get(download_url, headers=headers)
            response.raise_for_status()
            data = response.json()
            download_links.append(data.get("href"))

        zip_buffer = BytesIO()

        with ZipFile(zip_buffer, 'w') as zip_file:
            for idx, link in enumerate(download_links):
                response = requests.get(link)
                response.raise_for_status()

                file_name = pathes[idx].split('/')[-1]
                zip_file.writestr(file_name, response.content)

        zip_buffer.seek(0)

        response = HttpResponse(zip_buffer, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=files.zip'
        return response
    except requests.RequestException as e:
        logging.error(f"Request error: {e}")
        return HttpResponseServerError("Ошибка при запросе к Yandex Disk API.")
    except ValueError as e:
        logging.error(f"JSON decode error: {e}")
        return HttpResponseServerError("Ошибка при обработке ответа.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return HttpResponseServerError("Что-то пошло не так...")
