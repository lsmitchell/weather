from django.urls import path
from . import views

urlpatterns = [
         path('', views.view, name='index_view'),
         path('api/weather/', views.get_weather, name='api'),
]
