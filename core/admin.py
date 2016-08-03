import datetime

from django.contrib import admin
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save

from .models import Kunjungan, KB, AlatKB, Obat, Pendaftaran, UserProfile
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
            return super(KBAdmin, self).get_readonly_fields(request, obj)
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

        # urutan
        today_min = datetime.datetime.combine(
            datetime.date.today(),
            datetime.time.min
        )
        today_max = datetime.datetime.combine(
            datetime.date.today(),
            datetime.time.max
        )
        pendaftaran_count = Pendaftaran.objects.filter(
            tanggal__range=(today_min, today_max)
        )
        urutan_kunjungan = len(pendaftaran_count) + 1
        obj.urutan_kunjungan = urutan_kunjungan
        obj.save()

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
    pass


def create_user_profile(sender, instance, created, **kwargs):
    if created:
       profile, created = UserProfile.objects.get_or_create(user=instance)

post_save.connect(create_user_profile, sender=User)

admin.site.register(Kunjungan, KunjunganAdmin)
admin.site.register(KB, KBAdmin)
admin.site.register(AlatKB)
admin.site.register(Obat)
admin.site.register(Pendaftaran, PendaftaranAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
