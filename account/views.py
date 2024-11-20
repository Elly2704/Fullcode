from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django_email_verification import send_email
from .forms import UserCreateForm, LoginForm, UserUpdateForm

User = get_user_model()


def register_user(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user_email = form.cleaned_data.get('email')
            user_username = form.cleaned_data.get('username')
            user_password = form.cleaned_data.get('password1')

            #Create a new user
            user = User(username=user_username, email=user_email)
            user.set_password(user_password)  # Хэшируем пароль
            user.is_active = False  # Делаем пользователя неактивным до подтверждения email
            user.save()

            send_email(user)
            return redirect('/account/email_verification_sent/')

            #send_email(user.email, 'Activate your account', 'verify_email.html', {'user': user})
            #messages.success(request, 'Registration successful. Please verify your email address.')
            #return redirect('account:login')
    else:
        form = UserCreateForm()
    return render(request, 'account/registration/register.html', {'form': form})


def login_user(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if request.user.is_authenticated:
            return redirect('shop:products')

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('account:dashboard')
            else:
                messages.error(request, 'Your account is not active.')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('account:login')
    #return render(request, 'account/login/login.html')
    context = {
        'form': form,
    }
    return render(request, 'account/login/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('shop:products')


@login_required
def dashboard_user(request):
    return render(request, 'account/dashboard/dashboard.html')


@login_required
def profile_user(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('account:dashboard')
    else:
        form = UserUpdateForm(request.POST, instance=request.user)
    context = {'form': form}
    return render(request, 'account/dashboard/profile_management.html', context)


@login_required
def delete_user(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        logout(request)
        messages.success(request, 'User deleted successfully.')
        return redirect('shop:products')
    return render(request, 'account/dashboard/account_delete.html')
