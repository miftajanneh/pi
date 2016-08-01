from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login

from .forms import MyUserCreationForm


def home(request):
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data["password1"]
            )
            login(request, user)
            return HttpResponseRedirect("/admin/")
    else:
        form = MyUserCreationForm()
    return render(request, "home.html", {
        'form': form,
    })
