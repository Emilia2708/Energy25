"""
URL configuration for project_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from app_energy25 import views

urlpatterns = [
    path('', views.home, name='home'),
    path("predkosc_wiatru/", views.predkosc_wiatru, name="predkosc_wiatru"),
    path("produkcja_wiatrowa/", views.produkcja_wiatrowa, name="produkcja_wiatrowa"),
    path("suma_wiatrowa/", views.suma_wiatrowa, name="suma_wiatrowa"),
    path("lokalizacje_wiatrowe/", views.lokalizacje_wiatrowe, name="lokalizacje_wiatrowe"),
    path("naslonecznienie/", views.naslonecznienie, name="naslonecznienie"),
    path("produkcja_pv/", views.produkcja_pv, name="produkcja_pv"),
    path("suma_pv/", views.suma_pv, name="suma_pv"),
    path("lokalizacje_pv/", views.lokalizacje_pv, name="lokalizacje_pv"),
    path("pobierz_dane_pv/", views.pobierz_dane_pv, name="pobierz_dane_pv"),
    path("pobierz_dane_wil/", views.pobierz_dane_wil, name="pobierz_dane_wil"),
]
