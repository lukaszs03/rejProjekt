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
    list_display = ('numer_rejestracyjny', 'rejestrator', 'miasto', 'email', 'telefon')
    change_list_template = 'admin/rej_app/rejestrator/change_list.html'  # Ważne!
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-excel/', self.import_excel, name='import_excel'),
        ]
        return custom_urls + urls
    
    def import_excel(self, request):
        if request.method == 'POST':
            form = ImportExcelForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    df = pd.read_excel(request.FILES['excel_file'])
                    for index, row in df.iterrows():
                        nazwa_rejestratora = row['Rejestrator']
                        numery_rej = str(row['Numer Rejestracyjny']).strip()
                        
                        for numer in [p.strip().upper() for p in numery_rej.split(',') if p.strip()]:
                            prefix = ''.join([c for c in numer if c.isalpha()])[:3]
                            prefix = prefix or 'UNK'
                            
                            Rejestrator.objects.update_or_create(
                                numer_rejestracyjny=prefix,
                                rejestrator=nazwa_rejestratora,
                                defaults={
                                    'miasto': row.get('Miasto', ''),
                                    'email': row.get('email', ''),
                                    'telefon': row.get('telefon', ''),
                                    'adres': row.get('adres', '')
                                }
                            )
                    
                    self.message_user(request, "Dane zaimportowane pomyślnie!")
                    return HttpResponseRedirect("../")
                except Exception as e:
                    self.message_user(request, f"Błąd: {str(e)}", level=messages.ERROR)
        else:
            form = ImportExcelForm()
        
        return render(request, 'admin/import_excel.html', {'form': form})

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
        def extract_prefix(numer_rej):
            numer_str = str(numer_rej).upper().strip()
            prefix = []
            for char in numer_str:
                if char.isalpha():
                    prefix.append(char)
                else:
                    break
            return ''.join(prefix) or 'UNK'

        if request.method == 'POST':
            form = ImportExcelForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    df = pd.read_excel(request.FILES['excel_file'])
                    new_records = 0
                    updated_records = 0
                    
                    for index, row in df.iterrows():
                        numer_rej = str(row['Numer Rejestracyjny']).strip()
                        prefix = extract_prefix(numer_rej)
                        rodzaj_sprawy = row.get('rodzaj sprawy', '') 
                        
                        rejestrator, created = Rejestrator.objects.get_or_create(
                            numer_rejestracyjny=prefix,
                            rejestrator=row['Rejestrator'],
                            defaults={
                                'miasto': row.get('miasto', ''),
                                'email': row.get('email', ''),
                                'telefon': row.get('telefon', ''),
                                'adres': row.get('adres', '')
                            }
                        )

                        if not Realizacja.objects.filter(
                            numer_rejestracyjny=numer_rej,
                            rejestrator=rejestrator,
                            rodzaj_sprawy=row.get('rodzaj sprawy', '')
                        ).exists():
                            
                            Realizacja.objects.create(
                                numer_rejestracyjny=numer_rej,
                                rejestrator=rejestrator,
                                numer_umowy=row.get('numer umowy', ''),
                                rodzaj_sprawy=row.get('rodzaj sprawy', ''),
                                grupa_spraw=row.get('grupy spraw', ''),
                            )
                            new_records += 1
                        else:
                            updated_records += 1
                    
                    self.message_user(
                        request,
                        f"Zakończono import: {new_records} nowych wpisów, {updated_records} pominiętych duplikatów",
                        level=messages.SUCCESS
                    )
                    return HttpResponseRedirect('..')
                    
                except Exception as e:
                    self.message_user(request, f"Błąd: {str(e)}", level=messages.ERROR)
        else:
            form = ImportExcelForm()
        
        context = {'form': form, 'opts': self.model._meta}
        return render(request, 'admin/import_excel.html', context)