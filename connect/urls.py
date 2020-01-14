from django.urls import path
from .views import starter, notify, completed
urlpatterns = [
    path('',starter),
    path('notify',notify),
    path('completed',completed),
]