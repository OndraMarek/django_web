from django.db import models

from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse

# Create your models here.

def plakat_path(instance, filename):
    return "film/" + str(instance.id) + "/plakat/" + filename

class Zanr(models.Model):
    zanr = models.CharField(max_length=50, unique=True, verbose_name="Nazev zanru", help_text='Zadej zanr filmu')
    class Meta:
        ordering = ["zanr"]
    def __str__(self):
        return self.zanr

class Film(models.Model):
    nazev = models.CharField(max_length=200, verbose_name="Nazev")
    reziser = models.CharField(max_length=100, verbose_name="Reziser")
    popis = models.TextField(blank=True, null=True, verbose_name="Popis filmu")
    delka = models.IntegerField(blank=True, null=True, help_text="Zadejte celočíselnou hodnotu", verbose_name="Delka filmu")
    pristupnost = models.CharField(max_length=20, verbose_name="Pristupnost")
    plakat = models.ImageField(upload_to=plakat_path, blank=True, null=True, verbose_name="Plakat")
    zanry = models.ManyToManyField(Zanr, help_text='Vyber zanr pro tento film')
    class Meta:
        ordering = ["nazev"]
    def __str__(self):
        return f"{self.nazev}, reziser: {str(self.reziser)}, pristupnost: {str(self.pristupnost)}"
    def get_absolute_url(self):
        return reverse('film-detail', args=[str(self.id)])
    
    # pristupnost = models.EnumField(choices=['Bez omezeni', 'P', '12', '15'])


