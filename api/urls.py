from django.urls import path
from .views import *



urlpatterns = [
    path('', home_page, name="home"),
    path("token/", token_page, name="token"),
	path("download/", download_view, name="download"),
	path("download-all/", download_all_view, name="download_all")
]
