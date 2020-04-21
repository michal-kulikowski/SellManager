from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from core.models import Lokale

now = timezone.now()


@login_required
def dashboard(request):
    if request.user.first_login is True:
        return redirect('dashboard:change_password')
    else:

        time_threshold = timezone.now() + timedelta(days=30)
        leady = Lokale.objects.filter(uzytkownik=request.user).filter(data_kolejnego_kontaktu__lte=time_threshold)

        context = {
            'leady': leady,
        }

        return render(request, 'dashboard/home.html', context)


from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if user.first_login is True:
                user.first_login = False
            user.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('dashboard:dashboard')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'dashboard/change-password.html', {
        'form': form
    })
