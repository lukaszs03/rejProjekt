from django.urls import path
from django.shortcuts import redirect
from .views import sprawdz_formularz, sprawdz_wynik, realizacje_lista

urlpatterns = [
    path('sprawdz/', sprawdz_formularz, name='sprawdz_formularz'),
    path('sprawdz/wynik/<str:numer>/', sprawdz_wynik, name='sprawdz_wynik'),
    path("realizacje/", realizacje_lista, name="realizacje_lista"),
    path('', lambda request: redirect('sprawdz_formularz', permanent=False)),

]
