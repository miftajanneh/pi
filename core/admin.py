from django.contrib import admin
from django.http import HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse

from .models import KB, AlatKB, Pendaftaran, UserProfile, Imunisasi, Melahirkan
from .forms import PendaftaranAdminForm


class KunjunganAdmin(admin.ModelAdmin):
    list_display = [
        '__str__',
        'biaya',
    ]
    list_filter = [
        'tanggal'
    ]


class KBAdmin(admin.ModelAdmin):
    list_display = [
        '__str__',
        'tanggal_mulai_pemakaian',
        'tanggal_kontrol'
    ]

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ('tanggal_kontrol',)
        return (
            'pasien',
            'tanggal_mulai_pemakaian',
            'tanggal_kontrol',
            'alat_kb'
        )

    def get_queryset(self, request):
        if request.user.is_superuser:
            return KB.objects.all()
        return KB.objects.filter(pasien=request.user)

    def change_view(self, request, object_id, form_url='',
                    extra_context=None):
        if not self.get_queryset(request).filter(id=object_id).exists():
            return HttpResponseRedirect(
                reverse('admin:core_kb_changelist'))

        return super(KBAdmin, self).change_view(request, object_id,
                                                         form_url,
                                                         extra_context)

    def delete_view(self, request, object_id, extra_context=None):
        if not self.get_queryset(request).filter(id=object_id).exists():
            return HttpResponseRedirect(
                reverse('admin:core_kb_changelist'))

        return super(KBAdmin, self).delete_view(request, object_id,
                                                         extra_context)

    def history_view(self, request, object_id, extra_context=None):
        if not self.get_queryset(request).filter(id=object_id).exists():
            return HttpResponseRedirect(
                reverse('admin:core_kb_changelist'))

        return super(KBAdmin, self).history_view(
            request, object_id,
            extra_context
        )


class PendaftaranAdmin(admin.ModelAdmin):
    form = PendaftaranAdminForm
    list_display = [
        '__str__',
        'tanggal',
        'urutan_kunjungan'
    ]
    list_filter = [
        'tanggal'
    ]
    readonly_fields = (
        'pasien',
        'urutan_kunjungan'
    )

    def save_model(self, request, obj, form, change):
        obj.pasien = request.user

        pendaftaran_count = Pendaftaran.objects.filter(
            tanggal=obj.tanggal
        )
        urutan_kunjungan = len(pendaftaran_count) + 1
        obj.urutan_kunjungan = urutan_kunjungan

        pendaftaran = obj

        melahirkan = False
        kamar = None
        if pendaftaran.tujuan_kunjungan == 'melahirkan':
            melahirkan = True
            melahirkans = Melahirkan.objects.filter(sudah_pulang=False)
            print(melahirkans)
            if not melahirkans:
                kamar = 1

            if len(melahirkans) == 1:
                if melahirkans[0].kamar == '1':
                    kamar = 2
                if melahirkans[0].kamar == '2':
                    kamar = 1

            if len(melahirkans) == 2:
                raise ValidationError('kamar sudah penuh')

        obj.save()
        if melahirkan:
            assert kamar
            Melahirkan.objects.create(kamar=kamar, pendaftaran=obj)

    def get_queryset(self, request):
        if request.user.is_superuser:
            return Pendaftaran.objects.all()
        return Pendaftaran.objects.filter(pasien=request.user)

    def change_view(self, request, object_id, form_url='',
                    extra_context=None):
        if not self.get_queryset(request).filter(id=object_id).exists():
            return HttpResponseRedirect(
                reverse('admin:core_pendaftaran_changelist'))

        return super(PendaftaranAdmin, self).change_view(request, object_id,
                                                  form_url, extra_context)

    def delete_view(self, request, object_id, extra_context=None):
        if not self.get_queryset(request).filter(id=object_id).exists():
            return HttpResponseRedirect(
                reverse('admin:core_pendaftaran_changelist'))

        return super(PendaftaranAdmin, self).delete_view(request, object_id,
                                                  extra_context)

    def history_view(self, request, object_id, extra_context=None):
        if not self.get_queryset(request).filter(id=object_id).exists():
            return HttpResponseRedirect(
                reverse('admin:core_pendaftaran_changelist'))

        return super(PendaftaranAdmin, self).history_view(
            request, object_id,
            extra_context
        )


class UserProfileAdmin(admin.ModelAdmin):
    list_display = [
        '__str__',
        'ibu_atau_anak',
        'nama_ibu',
        'nama_anak',
        'nama_ayah',
        'jenis_kelamin',
        'tanggal_lahir'
    ]


class ImunisasiAdmin(admin.ModelAdmin):
    list_display = [
        '__str__',
        'tanggal',
        'jenis_imunisasi'
        ]
    list_filter = [
        'tanggal'
    ]

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return super(ImunisasiAdmin, self).get_readonly_fields(request, obj)
        return (
            'pasien',
            'tanggal',
            'jenis_imunisasi',
        )

    def get_queryset(self, request):
        if request.user.is_superuser:
            return Imunisasi.objects.all()
        return Imunisasi.objects.filter(pasien=request.user)

    def change_view(self, request, object_id, form_url='',
                    extra_context=None):
        if not self.get_queryset(request).filter(id=object_id).exists():
            return HttpResponseRedirect(
                reverse('admin:core_imunisasi_changelist'))

        return super(ImunisasiAdmin, self).change_view(request, object_id,
                                                form_url,
                                                extra_context)

    def delete_view(self, request, object_id, extra_context=None):
        if not self.get_queryset(request).filter(id=object_id).exists():
            return HttpResponseRedirect(
                reverse('admin:core_imunisasi_changelist'))

        return super(ImunisasiAdmin, self).delete_view(request, object_id,
                                                extra_context)

    def history_view(self, request, object_id, extra_context=None):
        if not self.get_queryset(request).filter(id=object_id).exists():
            return HttpResponseRedirect(
                reverse('admin:core_imunisasi_changelist'))

        return super(ImunisasiAdmin, self).history_view(
            request, object_id,
            extra_context
        )


class AlatKBAdmin(admin.ModelAdmin):
    list_display = [
        'nama',
        'periode_pemakaian',
        'id'
    ]


class MelahirkanAdmin(admin.ModelAdmin):
    list_display = [
        '__str__',
        'kamar'
    ]

admin.site.register(KB, KBAdmin)
admin.site.register(AlatKB, AlatKBAdmin)
admin.site.register(Pendaftaran, PendaftaranAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Imunisasi, ImunisasiAdmin)
admin.site.register(Melahirkan, MelahirkanAdmin)
