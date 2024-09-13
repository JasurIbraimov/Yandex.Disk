from django.urls import path
from .views import *

urlpatterns = [
    path('', home_page, name="home"),
    path('token/', token_page, name="token"),
	
]
