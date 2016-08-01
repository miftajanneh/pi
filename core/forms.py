import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group

from .models import Pendaftaran, UserProfile, JENIS_KELAMIN


class PendaftaranAdminForm(forms.ModelForm):
    class Meta:
        model = Pendaftaran
        fields = '__all__'

    def clean(self):
        if self.cleaned_data.get('tanggal') < datetime.datetime.today().date():
            raise forms.ValidationError('Tanggal tidak boleh kemarin')
        return self.cleaned_data


class MyUserCreationForm(UserCreationForm):
    nama = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    jenis_kelamin = forms.ChoiceField(
        required=True,
        widget=forms.RadioSelect,
        choices=JENIS_KELAMIN
    )
    alamat = forms.CharField(required=True)
    tanggal_lahir = forms.DateField(required=True, widget=forms.SelectDateWidget(years=range(1950, 2016)))

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.is_staff = True
            user.save()
            g = Group.objects.get(name='Pasien')
            g.user_set.add(user)

        user_profile = UserProfile.objects.get(user=user)
        user_profile.nama = self.cleaned_data.get('nama')
        user_profile.jenis_kelamin = self.cleaned_data.get('jenis_kelamin')
        user_profile.alamat = self.cleaned_data.get('alamat')
        user_profile.phone_number = self.cleaned_data.get('phone_number')
        user_profile.tanggal_lahir = self.cleaned_data.get('tanggal_lahir')
        user_profile.save()

        return user

