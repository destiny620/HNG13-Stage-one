from django.urls import path
from .views import StringAnalyzerView, NaturalLanguageFilterView

urlpatterns = [
    path('strings/', StringAnalyzerView.as_view(), name='string-list'),
    path('strings/<str:string_value>/', StringAnalyzerView.as_view(), name='string-detail'),
    path('strings/filter-by-natural-language', NaturalLanguageFilterView.as_view(), name='natural-language-filter'),
]