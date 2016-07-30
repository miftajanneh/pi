from django.db import models
from django.contrib.auth.models import User


class Obat(models.Model):
    jenis = models.CharField(max_length=30)
    nama = models.CharField(max_length=30)
    harga = models.IntegerField()

    class Meta:
        verbose_name_plural = 'Obat'

    def __str__(self):
        return self.nama


class Kunjungan(models.Model):
    tanggal = models.DateField()
    pasien = models.ForeignKey(User, related_name='kunjungan_pasien')
    biaya = models.IntegerField()
    obat = models.ManyToManyField(Obat)

    class Meta:
        verbose_name_plural = 'Kunjungan'

    def __str__(self):
        return str(self.tanggal) + ' ' + self.pasien.username

class AlatKB(models.Model):
    nama = models.CharField(max_length=30)
    periode_pemakaian = models.IntegerField(help_text='dalam hari')

    class Meta:
        verbose_name_plural = 'Alat KB'

    def __str__(self):
        return self.nama

class KB(models.Model):
    pasien = models.ForeignKey(User)
    alat_kb = models.ForeignKey(AlatKB)
    tanggal_mulai_pemakaian = models.DateField()
    tanggal_kontrol = models.DateField()

    class Meta:
        verbose_name_plural = 'KB'

    def __str__(self):
        return self.pasien.username + ' - ' + self.alat_kb.nama
