from django.urls import path
from profiles.views import register

urlpatterns = [
    path('register', register, name='register')
]
