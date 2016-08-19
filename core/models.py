import datetime

from django.db import models
from django.core.exceptions import ValidationError
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
    nama = models.CharField(max_length=30, unique=True)
    periode_pemakaian = models.IntegerField(help_text='dalam hari')

    class Meta:
        verbose_name_plural = 'Alat KB'

    def __str__(self):
        return self.nama


class KB(models.Model):
    pasien = models.ForeignKey(User)
    alat_kb = models.ForeignKey(AlatKB)
    tanggal_mulai_pemakaian = models.DateField()
    tanggal_kontrol = models.DateField(blank=True)

    def save(self, *args, **kwargs):
        periode_pemakaian = self.alat_kb.periode_pemakaian
        self.tanggal_kontrol = \
            self.tanggal_mulai_pemakaian + datetime.timedelta(days=periode_pemakaian)
        super(KB, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'KB'

    def __str__(self):
        return self.pasien.username + ' - ' + self.alat_kb.nama


TUJUAN_CHOICES = (
    ('konsultasi kehamilan', 'konsultasi kehamilan'),
    ('USG', 'USG'),
    ('melahirkan', 'melahirkan'),
    ('KB', 'KB'),
    ('imunisasi', 'imunisasi'),
    ('konsultasi ibu dan anak', 'konsultasi ibu dan anak')
)

IBU_ATAU_ANAK_CHOICES = (
    ('ibu', 'ibu'),
    ('anak', 'anak')
)


class Pendaftaran(models.Model):
    pasien = models.ForeignKey(User)
    tanggal = models.DateField()
    tujuan_kunjungan = models.CharField(max_length=100, choices=TUJUAN_CHOICES)
    urutan_kunjungan = models.IntegerField()

    class Meta:
        verbose_name_plural = 'Pendaftaran'

    def __str__(self):
        return '{} {} {}'.format(
            self.pasien.username,
            str(self.tanggal),
            self.tujuan_kunjungan
        )

    def clean(self):
        if self.tujuan_kunjungan == 'Melahirkan':
            melahirkans = Melahirkan.objects.filter(sudah_pulang=False)
            if not melahirkans:
                Melahirkan.objects.create(kamar='1', pendaftaran=self)
                return super(Pendaftaran, self).clean()
            if len(melahirkans) == 1:
                if melahirkans[0].kamar == '1':
                    Melahirkan.objects.create(kamar='2', pendaftaran=self)
                    return super(Pendaftaran, self).clean()
                if melahirkans[0].kamar == '2':
                    Melahirkan.objects.create(kamar='1', pendaftaran=self)
                    return super(Pendaftaran, self).clean()
            if melahirkans == 2:
                raise ValidationError('kamar sudah penuh')


KAMAR_CHOICES = (
    ('1', '1'),
    ('2', '2')
)


class Melahirkan(models.Model):
    kamar = models.CharField(max_length=1, choices=KAMAR_CHOICES)
    pendaftaran = models.ForeignKey(Pendaftaran)
    sudah_pulang = models.BooleanField(default=False)

JENIS_KELAMIN = (
    ('laki-laki', 'laki-laki'),
    ('perempuan', 'perempuan')
)


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    ibu_atau_anak = models.CharField(max_length=100, null=True, blank=True,
                                     choices=IBU_ATAU_ANAK_CHOICES)
    nama_ibu = models.CharField(max_length=100, null=True, blank=True)
    nama_anak = models.CharField(max_length=100, null=True, blank=True)
    nama_ayah = models.CharField(max_length=100, null=True, blank=True)
    jenis_kelamin = models.CharField(
        max_length=30, choices=JENIS_KELAMIN, null=True, blank=True
    )
    alamat = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=30, null=True, blank=True)
    tanggal_lahir = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username


class Imunisasi(models.Model):
    pasien = models.ForeignKey(User)
    tanggal = models.DateField()
    jenis_imunisasi = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Imunisasi'

    def __str__(self):
        return self.pasien.username

