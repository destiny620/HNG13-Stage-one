from django.urls import path
from . import views

urlpatterns = [
    path('strings', views.create_string_analysis),
    path('strings/<str:string_value>', views.get_string_analysis),
    path('strings/', views.get_string_analysis),
    path('strings/<str:string_value>/delete', views.delete_string_analysis),
]