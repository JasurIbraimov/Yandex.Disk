from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
import requests
from io import BytesIO
from zipfile import ZipFile
import logging

BASE_URL = "https://cloud-api.yandex.net/v1/disk"

def handler500(request: HttpRequest, exception: str) -> HttpResponse:
    """Обработка ошибки со статусом 500 (ошибки на сервере)."""
    return render(request, "api/500.html", {"exception": exception}, status=500)


def handle_exception(request: HttpRequest, e: Exception) -> HttpResponse:
    """Обработка и вывод возможных ошибок."""
    if isinstance(e, requests.RequestException):
        logging.error(f"Request error: {e}")
        return handler500(request, "Ошибка при запросе к Yandex Disk API.")
    elif isinstance(e, ValueError):
        logging.error(f"JSON decode error: {e}")
        return handler500(request, "Ошибка при обработке ответа.")
    else:
        logging.error(f"Unexpected error: {e}")
        return handler500(request, "Что-то пошло не так...")

def home_page(request: HttpRequest) -> HttpResponse:
    """Представление для главной страницы."""
    try:
        # Получение токена из запроса
        token = request.GET.get("token") 
        
        # Формирование контекста рендера
        context = {
            "token": token
        }

        if token: # Если токен представлен в запросе

            # Формирование заголовков для запроса 
            headers = {'Content-Type': 'application/json',
                       'Accept': 'application/json', 'Authorization': f'OAuth {token}'}
            
            # ссылка для получения информации о диске  
            disk_data_url =  BASE_URL
            
            # ссылка для получения файлов на диске
            disk_items_url = f"{BASE_URL}/resources/files" 

            # Получение данных о диске по ссылке 
            disk_data_response = requests.get(disk_data_url, headers=headers)
            # Выкинуть ошибку при появлении
            disk_data_response.raise_for_status()
            # Получение ответа в виде JSON
            disk_data = disk_data_response.json()

            # Получение данных о файлах диска по ссылке 
            disk_items_response = requests.get(disk_items_url, headers=headers)
            # Выкинуть ошибку при появлении
            disk_items_response.raise_for_status()
            # Получение ответа в виде JSON
            disk_items_data = disk_items_response.json()

            # Добавить информацию в контекст
            context["disk"] = disk_data 
            context["items_data"] = disk_items_data
        
        return render(request, "api/index.html", context)
    except Exception as e:
        # В случае ошибки запустить обработчик
        return handle_exception(request, e)

def token_page(request: HttpRequest) -> HttpResponse:
    """Представление для страницы получения токена"""
    return render(request, "api/token.html", {})


def download_view(request: HttpRequest) -> HttpResponse:
    """Представление для страницы скачивания одного файла"""
    try:
        # Получение токена из запроса
        token = request.GET.get("token")
        # Получение пути к файла из запроса
        path = request.GET.get("path")
    
        # Формирование заголовков для запроса 
        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json', 'Authorization': f'OAuth {token}'}
       
        # ссылка для получения конечной ссылки на скачивание файла
        download_url = f"{BASE_URL}/resources/download?path={path}"

        # Получение ссылки на скачивание
        response = requests.get(download_url, headers=headers)
        # Выкинуть ошибку при появлении
        response.raise_for_status()
        # Получение ответа в виде JSON
        data = response.json()

        return redirect(data.get("href"))
    except Exception as e:
        return handle_exception(request, e)


def download_all_view(request: HttpRequest) -> HttpResponse:
    try:
        # Получение токена из запроса
        token = request.GET.get("token")
        # Получение всех пути к файлам из запроса
        pathes = request.GET.get("pathes").split(",")

        # Формирование заголовков для запроса 
        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json', 'Authorization': f'OAuth {token}'}

        # список в котором будут все ссылки на скачивание
        download_links = []

        for path in pathes:
            # ссылка на получение ссылки на скачивание каждого отдельного файла
            download_url = f"{BASE_URL}/resources/download?path={path}"
            # Получение ссылки на скачивание
            response = requests.get(download_url, headers=headers)
            # Выкинуть ошибку при появлении
            response.raise_for_status()
            # Получение ответа в виде JSON
            data = response.json()
            # Добавить в список полученную ссылку
            download_links.append(data.get("href"))

        # объект для записи в zip-файл
        zip_buffer = BytesIO()

        with ZipFile(zip_buffer, 'w') as zip_file:
            for idx, link in enumerate(download_links):
                # Получение файла для скачивания
                response = requests.get(link)
                # Выкинуть ошибку при появлении
                response.raise_for_status()
                # Получение названия файла
                file_name = pathes[idx].split('/')[-1]

                # Запись в zip-файл
                zip_file.writestr(file_name, response.content)

        # Переместить указатель на первый байт
        zip_buffer.seek(0)
        # Формирование ответа с типом файла zip
        response = HttpResponse(zip_buffer, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=files.zip'
        return response
    except Exception as e:
        return handle_exception(request, e)