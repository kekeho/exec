from django.urls import path
from . import views

urlpatterns = [
    path('script/', views.execute_string, name='execute_string'),
    path('front/', views.execute_front, name='execute_front')
]
