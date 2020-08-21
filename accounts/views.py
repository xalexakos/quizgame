from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect


# todo: 1) include signup and login links in the related views.
#       2) add the login url in top bar.
#       3) use messages.
def register_page(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # todo: add an info messages that user has been created.
            return redirect('login_page')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


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

        # todo: handle invalid login with messages.

    return render(request, 'accounts/login.html', context)
