from django.urls import path
from .views import render_resume

urlpatterns = [
    path('', render_resume),
]
