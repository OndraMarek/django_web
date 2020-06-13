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
    class Pristupnost(models.TextChoices):
        BEZ_OMEZENI = 'Bez omezeni'
        P = 'P'
        DVANACT = '12'
        PATNACT = '15'
    pristupnost = models.CharField(max_length=15, choices=Pristupnost.choices)
    plakat = models.ImageField(upload_to=plakat_path, blank=True, null=True, verbose_name="Plakat")
    zanry = models.ManyToManyField(Zanr, help_text='Vyber zanr pro tento film')
    class Meta:
        ordering = ["nazev"]
    def __str__(self):
        return f"{self.nazev}, reziser: {str(self.reziser)}, pristupnost: {str(self.pristupnost)}"
    def get_absolute_url(self):
        return reverse('film-detail', args=[str(self.id)])

class Sal(models.Model):
    pocet_sedadel = models.IntegerField(blank=True, null=True, help_text="Zadejte celočíselnou hodnotu", verbose_name="Pocet mist")
    class Meta:
        ordering = ["pocet_sedadel"]
    def __str__(self):
        return self.pocet_sedadel

class Projekce(models.Model):
    zacatek = models.DateField(blank=True, null=True, help_text="Format: <em>YYYY-MM-DD</em>", verbose_name="Zacatek projekce")
    class Typy(models.TextChoices):
        TRID = '3D'
        DVED = '2D'
    typ = models.CharField(max_length=10, choices=Typy.choices)
    class Dabing(models.TextChoices):
        TITULKY = 'titulky'
        CESKY = 'cesky'
    dabing = models.CharField(max_length=10, choices=Dabing.choices)
    filmy = models.ManyToManyField(Film, help_text='Vyber film')
    saly = models.ManyToManyField(Sal, help_text='Vyber pocet sedadel')
    class Meta:
        ordering = ["zacatek", "typ"]
    def __str__(self):
        return self.zacatek

class Uzivatel(models.Model):
    jmeno = models.CharField(max_length=20, verbose_name="Jmeno")
    prijmeni = models.CharField(max_length=20, verbose_name="Prijmeni")
    class Pohlavi(models.TextChoices):
        ZENA = 'zena'
        MUZ = 'muz'
        JINE = 'jine'
    pohlavi = models.CharField(max_length=10, choices=Pohlavi.choices)
    email = models.CharField(max_length=200, verbose_name="Email")
    class Meta:
        ordering = ["prijmeni", "jmeno"]
    def __str__(self):
        return self.prijmeni

class Rezervace(models.Model):
    pocet_mist = models.IntegerField(blank=True, null=True, help_text="Zadejte celočíselnou hodnotu", verbose_name="Pocet mist")
    uzivatel = models.ManyToManyField(Uzivatel, help_text='Uzivatel')
    projekce = models.ManyToManyField(Projekce, help_text='Projekce')
    class Meta:
        ordering = ["pocet_mist"]
    def __str__(self):
        return self.pocet_mist