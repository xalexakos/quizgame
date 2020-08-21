from django.shortcuts import redirect


def anonymous_user(view_func):
    """ Redirect authenticated users to home page """
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home_page')

        return view_func(request, *args, **kwargs)

    return wrapper_func
