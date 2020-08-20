from django.shortcuts import render, redirect


def register_page(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # todo: add an info message that user has been created.
            return redirect('login_page')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)
