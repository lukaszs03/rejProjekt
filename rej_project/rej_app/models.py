from django.db import models

class Rejestrator(models.Model):
    numer_rejestracyjny = models.CharField(max_length=10)
    nazwa_firmy = models.CharField(max_length=100)
    imie_nazwisko = models.CharField(max_length=100)
    email = models.EmailField()
    telefon = models.CharField(max_length=20)
    adres = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.nazwa_firmy} - {self.imie_nazwisko}"

class Realizacja(models.Model):
    firma = models.ForeignKey(Rejestrator, on_delete=models.CASCADE) 
    numer_rejestracyjny = models.CharField(max_length=20)
    czynnosc = models.TextField()
    data_dodania = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.firma.nazwa_firmy} - {self.numer_rejestracyjny}"
