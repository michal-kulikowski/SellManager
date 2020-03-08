from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


@login_required
def dashboard(request):
    if request.user.first_login is True:
        return redirect('dashboard:change_password')
    else:
        car = 'none'
        context = {
            'car': car,
        }

        return render(request, 'dashboard/home.html', context)


@login_required
def list(request):
    return render(request, 'dashboard/home-list.html')


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
