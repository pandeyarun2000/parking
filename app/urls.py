from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search-pdf/', views.search_pdf, name='search-pdf'),
    path('download-csv/', views.download_csv, name='download_csv'),
    path('results/', views.results, name='results'),
]

