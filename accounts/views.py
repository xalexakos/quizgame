from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect

from accounts.decorators import anonymous_user


@anonymous_user
def registration_page(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,
                                 'User "' + form.cleaned_data.get('username') + '" has been registered.')
            return redirect('login_page')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


@anonymous_user
def login_page(request):
    form = AuthenticationForm()
    context = {'form': form}

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home_page')
        else:
            messages.add_message(request, messages.ERROR, 'Invalid username or password')

    return render(request, 'accounts/login.html', context)


def logout_page(request):
    logout(request)
    return redirect('login_page')
