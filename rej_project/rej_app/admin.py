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
                            rejestrator=row['Rejestrator'],
                            defaults={
                                'osoba_kontaktowa': row['Osoba do kontaktu'],
                                'email': row['email'],
                                'telefon': row['telefon'],
                                'adres': row['adres'],
                            }
                        )
                    self.message_user(request, "Dane zaimportowane pomyślnie!")
                    return HttpResponseRedirect('..')
                except Exception as e:
                    self.message_user(request, f"Błąd: {str(e)}", level=messages.ERROR)
        else:
            form = ImportExcelForm()
        
        context = {
            'form': form,
            'opts': self.model._meta,
        }
        return render(request, 'admin/import_excel.html', context)

@admin.register(Realizacja)
class RealizacjaAdmin(admin.ModelAdmin):
    list_display = ('numer_rejestracyjny', 'get_rejestrator', 'numer_umowy', 'rodzaj_sprawy', 'grupa_spraw', 'data_dodania')
    change_list_template = 'admin/rej_app/realizacja/change_list.html'

    def get_rejestrator(self, obj):
        return obj.rejestrator.rejestrator if obj.rejestrator else "-"
    get_rejestrator.short_description = 'Rejestrator'
    get_rejestrator.admin_order_field = 'rejestrator__rejestrator'
    
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
                        numer_rej = row['Numer Rejestracyjny']
                        nazwa_rejestratora = row['Rejestrator']

                        prefix_rej = ''.join(filter(str.isalpha, str(numer_rej))).upper()

                        try:
                            rejestrator = Rejestrator.objects.get(
                                numer_rejestracyjny=prefix_rej,
                                rejestrator=nazwa_rejestratora
                            )

                            if not rejestrator.osoba_kontaktowa or rejestrator.osoba_kontaktowa == 'Do uzupełnienia':
                                rejestrator.osoba_kontaktowa = row.get('Osoba do kontaktu', 'Do uzupełnienia')
                            if not rejestrator.email or rejestrator.email == 'brak@example.com':
                                rejestrator.email = row.get('email', 'brak@example.com')
                            if not rejestrator.telefon or rejestrator.telefon == '000000000':
                                rejestrator.telefon = row.get('telefon', '000000000')
                            if not rejestrator.adres or rejestrator.adres == 'Do uzupełnienia':
                                rejestrator.adres = row.get('adres', 'Do uzupełnienia')
                            rejestrator.save()
                            
                        except Rejestrator.DoesNotExist:
                            rejestrator = Rejestrator.objects.create(
                                numer_rejestracyjny=prefix_rej,
                                rejestrator=nazwa_rejestratora,
                                osoba_kontaktowa=row.get('Osoba do kontaktu', 'Do uzupełnienia'),
                                email=row.get('email', 'brak@example.com'),
                                telefon=row.get('telefon', '000000000'),
                                adres=row.get('adres', 'Do uzupełnienia'),
                            )
                            self.message_user(
                                request, 
                                f"Utworzono nowego rejestratora: {prefix_rej} {rejestrator.rejestrator}", 
                                level=messages.INFO
                            )

                        Realizacja.objects.update_or_create(
                            numer_rejestracyjny=numer_rej,
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