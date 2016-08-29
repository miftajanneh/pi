import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group

from .models import Pendaftaran, UserProfile, JENIS_KELAMIN, IBU_ATAU_ANAK_CHOICES, Melahirkan


class PendaftaranAdminForm(forms.ModelForm):
    class Meta:
        model = Pendaftaran
        fields = '__all__'

    def clean(self):
        if self.cleaned_data.get('tanggal') < datetime.datetime.today().date():
            raise forms.ValidationError('Tanggal tidak boleh kemarin')

        if self.cleaned_data.get('tujuan_kunjungan') == 'melahirkan':
            if len(Melahirkan.objects.filter(sudah_pulang=False)) == 2:
                raise forms.ValidationError('kamar sudah penuh')

        return self.cleaned_data


class MyUserCreationForm(UserCreationForm):
    ibu_atau_anak = forms.ChoiceField(
        required=True,
        widget=forms.RadioSelect,
        choices=IBU_ATAU_ANAK_CHOICES
    )
    nama_ibu = forms.CharField(required=True)
    nama_anak = forms.CharField(required=False,
                                help_text='kosongkan jika anda adalah ibu dan belum mempunyai nama anak')
    nama_ayah_atau_suami = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    jenis_kelamin = forms.ChoiceField(
        required=True,
        widget=forms.RadioSelect,
        choices=JENIS_KELAMIN
    )
    alamat = forms.CharField(required=True)
    tanggal_lahir = forms.DateField(required=True, widget=forms.SelectDateWidget(years=range(1950, 2016)))

    def clean_nama_anak(self):
        ibu_atau_anak = self.cleaned_data.get('ibu_atau_anak')
        nama_anak = self.cleaned_data.get('nama_anak')
        if ibu_atau_anak == 'anak' and not nama_anak:
            raise forms.ValidationError('')
        return nama_anak

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.is_staff = True
            user.save()
            g = Group.objects.get(name='Pasien')
            g.user_set.add(user)

        user_profile = UserProfile.objects.create(user=user)
        user_profile.nama_anak = self.cleaned_data.get('nama_anak')
        user_profile.nama_ibu = self.cleaned_data.get('nama_ibu')
        user_profile.nama_ayah = self.cleaned_data.get('nama_ayah_atau_suami')
        user_profile.ibu_atau_anak = self.cleaned_data.get('ibu_atau_anak')
        user_profile.jenis_kelamin = self.cleaned_data.get('jenis_kelamin')
        user_profile.alamat = self.cleaned_data.get('alamat')
        user_profile.phone_number = self.cleaned_data.get('phone_number')
        user_profile.tanggal_lahir = self.cleaned_data.get('tanggal_lahir')
        user_profile.save()

        return user

