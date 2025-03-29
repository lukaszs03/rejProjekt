from django.contrib import admin
from django import forms
from django.shortcuts import render
from django.urls import path
from django.http import HttpResponseRedirect
from django.contrib import messages
import pandas as pd
from .models import Realizacja, Rejestrator

class ImportExcelForm(forms.Form):
    excel_file = forms.FileField()

@admin.register(Rejestrator)
class RejestratorAdmin(admin.ModelAdmin):
    list_display = ('numer_rejestracyjny', 'rejestrator', 'osoba_kontaktowa', 'email', 'telefon')
    change_list_template = 'admin/rej_app/rejestrator/change_list.html'
    
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-excel/', self.import_excel),
        ]
        return my_urls + urls
    
    def import_excel(self, request):
        if request.method == 'POST':
            form = ImportExcelForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    df = pd.read_excel(request.FILES['excel_file'])
                    for index, row in df.iterrows():
                        Rejestrator.objects.update_or_create(
                            numer_rejestracyjny=row['Numer Rejestracyjny'],
                            defaults={
                                'rejestrator': row['Rejestrator'],
                                'osoba_kontaktowa': row['Osoba do kontaktu'],
                                'email': row['email'],
                                'telefon': row['telefon'],
                                'adres': row['adres'],
                            }
                        )
                    self.message_user(request, "Dane zostały zaimportowane pomyślnie")
                    return HttpResponseRedirect('..')
                except Exception as e:
                    self.message_user(request, f"Błąd podczas importu: {str(e)}", level=messages.ERROR)
        else:
            form = ImportExcelForm()
        
        context = {
            'form': form,
            'opts': self.model._meta,
        }
        return render(request, 'admin/import_excel.html', context)

@admin.register(Realizacja)
class RealizacjaAdmin(admin.ModelAdmin):
    list_display = ('numer_rejestracyjny', 'rejestrator', 'numer_umowy', 'rodzaj_sprawy', 'grupa_spraw')
    change_list_template = 'admin/rej_app/realizacja/change_list.html'
    
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-excel/', self.import_excel),
        ]
        return my_urls + urls
    
    def import_excel(self, request):
        if request.method == 'POST':
            form = ImportExcelForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    df = pd.read_excel(request.FILES['excel_file'])
                    for index, row in df.iterrows():
                        rejestrator = Rejestrator.objects.filter(
                            numer_rejestracyjny=row['Rejestrator']
                        ).first()
                        
                        Realizacja.objects.update_or_create(
                            numer_rejestracyjny=row['Numer Rejestracyjny'],
                            defaults={
                                'rejestrator': rejestrator,
                                'numer_umowy': row['numer umowy'],
                                'rodzaj_sprawy': row['rodzaj sprawy'],
                                'grupa_spraw': row['grupy spraw'],
                            }
                        )
                    self.message_user(request, "Dane zostały zaimportowane pomyślnie")
                    return HttpResponseRedirect('..')
                except Exception as e:
                    self.message_user(request, f"Błąd podczas importu: {str(e)}", level=messages.ERROR)
        else:
            form = ImportExcelForm()
        
        context = {
            'form': form,
            'opts': self.model._meta,
        }
        return render(request, 'admin/import_excel.html', context)