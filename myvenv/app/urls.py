from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search-pdf/', views.search_pdf, name='search-pdf'),
]

