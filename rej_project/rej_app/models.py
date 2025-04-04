from django.db import models

class Rejestrator(models.Model):
    numer_rejestracyjny = models.CharField(max_length=20)
    rejestrator = models.CharField(max_length=100)
    osoba_kontaktowa = models.CharField(max_length=100)
    email = models.EmailField()
    telefon = models.CharField(max_length=100)
    adres = models.CharField(max_length=300)

    def __str__(self):
        return self.rejestrator

class Meta:
    unique_together = ['numer_rejestracyjny', 'rejestrator']


class Realizacja(models.Model):
    rejestrator = models.ForeignKey(Rejestrator, on_delete=models.CASCADE, null=True)
    numer_rejestracyjny = models.CharField(max_length=20)
    numer_umowy = models.CharField(max_length=50)
    rodzaj_sprawy = models.CharField(max_length=100)
    grupa_spraw = models.CharField(max_length=10)
    data_dodania = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.numer_rejestracyjny