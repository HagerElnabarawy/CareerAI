from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render


def home(request):

    if request.user.is_authenticated:
        return redirect('/dashboard/')

    return redirect('/login/')


def register_view(request):

    if request.user.is_authenticated:
        return redirect('/dashboard/')

    if request.method == 'POST':

        username = request.POST.get(
            'username',
            ''
        ).strip()

        email = request.POST.get(
            'email',
            ''
        ).strip()

        password = request.POST.get(
            'password',
            ''
        )

        if not username or not email or not password:

            return render(
                request,
                'accounts/register.html',
                {
                    'error': 'Please fill in all fields.'
                }
            )

        if User.objects.filter(
            username=username
        ).exists():

            return render(
                request,
                'accounts/register.html',
                {
                    'error': 'Username already exists.'
                }
            )

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(
            request,
            user
        )

        return redirect('/dashboard/')

    return render(
        request,
        'accounts/register.html'
    )


def login_view(request):

    if request.user.is_authenticated:
        return redirect('/dashboard/')

    if request.method == 'POST':

        username = request.POST.get(
            'username',
            ''
        ).strip()

        password = request.POST.get(
            'password',
            ''
        )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(
                request,
                user
            )

            return redirect('/dashboard/')

        return render(
            request,
            'accounts/login.html',
            {
                'error': 'Invalid username or password.'
            }
        )

    return render(
        request,
        'accounts/login.html'
    )


def logout_view(request):

    logout(request)

    return redirect('/login/')