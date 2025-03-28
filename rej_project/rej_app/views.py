from django.shortcuts import render, redirect
from .models import Realizacja, Rejestrator
from django.db.models import Q
from django.core.paginator import Paginator

def sprawdz_formularz(request):
    query = request.GET.get("q", "").upper()
    rejestratorzy = Rejestrator.objects.all()

    if query:
        rejestratorzy = rejestratorzy.filter(numer_rejestracyjny__startswith=query)

    paginator = Paginator(rejestratorzy, 10)
    page_number = request.GET.get("page")
    rejestratorzy_page = paginator.get_page(page_number)

    if request.method == "POST":
        numer = request.POST.get("numer_rejestracyjny")
        return redirect("sprawdz_wynik", numer=numer)

    return render(
        request, "formularz.html",
        {"rejestratorzy": rejestratorzy_page, "query": query}
    )


def sprawdz_wynik(request, numer):
    realizacje = Realizacja.objects.filter(numer_rejestracyjny=numer)

    prefix = numer[:3]

    if len(prefix) == 3 and prefix[2].isdigit():
        clean_prefix = numer[:2]
    else:
        clean_prefix = prefix

    return render(request, "wynik.html", {
        "realizacje": realizacje,
        "numer": numer,
        "clean_prefix": clean_prefix  
    })


def realizacje_lista(request):
    filter_value = request.GET.get("filter", "").upper()
    
    realizacje = Realizacja.objects.all()
    if filter_value:
        realizacje = realizacje.filter(numer_rejestracyjny__startswith=filter_value)

    paginator = Paginator(realizacje, 10)
    page_number = request.GET.get("page")
    realizacje_page = paginator.get_page(page_number)

    return render(request, "realizacje.html", {"realizacje": realizacje_page, "filter_value": filter_value})