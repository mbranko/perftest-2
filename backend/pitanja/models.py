from datetime import timedelta
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.db import models


def sada():
    return now()


def sutra():
    return now() + timedelta(days=1)


class Skola(models.Model):
    naziv = models.CharField(max_length=100)
    adresa = models.CharField(max_length=100)
    mesto = models.CharField(max_length=100)

    def __str__(self):
        return self.naziv + ' ' + self.mesto

    class Meta:
        verbose_name = 'škola'
        verbose_name_plural = 'škole'


class Ucenik(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    skola = models.ForeignKey(Skola, on_delete=models.CASCADE)

    def name(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def __str__(self):
        return self.name()

    class Meta:
        verbose_name = 'učenik'
        verbose_name_plural = 'učenici'


class Test(models.Model):
    naziv = models.CharField(max_length=100)
    datum_formiranja = models.DateField(default=sada)
    datum_vazenja = models.DateField(default=sutra)

    def __str__(self):
        return self.naziv + ' ' + self.datum_vazenja.strftime('%Y-%m-%d')

    class Meta:
        verbose_name = 'test'
        verbose_name_plural = 'testovi'


class Pitanje(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    redni_broj = models.PositiveSmallIntegerField()
    tip = models.CharField(max_length=1, choices=[('1', 'Jedan tačan odgovor'), ('2', 'Više tačnih odgovora')])
    tekst = models.TextField()

    def __str__(self):
        return self.test.naziv + ' ' + str(self.redni_broj)

    class Meta:
        verbose_name = 'pitanje'
        verbose_name_plural = 'pitanja'


class Odgovor(models.Model):
    pitanje = models.ForeignKey(Pitanje, on_delete=models.CASCADE)
    redni_broj = models.PositiveSmallIntegerField()
    tekst = models.TextField()
    tacan = models.BooleanField()

    def __str__(self):
        return str(self.pitanje) + ' ' + str(self.redni_broj)

    class Meta:
        verbose_name = 'odgovor'
        verbose_name_plural = 'odgovori'


class TestUcenika(models.Model):
    ucenik = models.ForeignKey(Ucenik, verbose_name='učenik', on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    pocetak_rada = models.DateTimeField(default=sada)
    kraj_rada = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.ucenik) + ' ' + str(self.test) + ' ' + self.pocetak_rada.strftime('%Y-%m-%d')

    class Meta:
        verbose_name = 'test učenika'
        verbose_name_plural = 'testovi učenika'


class OdgovorUcenika(models.Model):
    test_ucenika = models.ForeignKey(TestUcenika, verbose_name='test učenika', on_delete=models.CASCADE)
    pitanje = models.ForeignKey(Pitanje, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=sada)
    odgovor = models.CharField(max_length=100)

    def __str__(self):
        return str(self.test_ucenika) + ' ' + str(self.pitanje.redni_broj)

    class Meta:
        verbose_name = 'odgovor učenika'
        verbose_name_plural = 'odgovori učenika'
