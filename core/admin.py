from django.contrib import admin
from .models import Kunjungan, KB, AlatKB, Obat

class KunjunganAdmin(admin.ModelAdmin):
    list_display = [
        '__str__',
        'biaya',
    ]
    list_filter = [
        'tanggal'
    ]

admin.site.register(Kunjungan, KunjunganAdmin)
admin.site.register(KB)
admin.site.register(AlatKB)
admin.site.register(Obat)
