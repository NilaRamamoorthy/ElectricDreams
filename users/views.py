from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile
from .forms import RegisterForm


def login_view(request):
    # ✅ If already logged in → redirect to "already logged in" view (same page)
    if request.user.is_authenticated:
        return render(request, 'users/login.html', {'already_logged_in': True})

    if request.method == 'POST':
        # Email login
        if 'email' in request.POST:
            email = request.POST.get('email')
            password = request.POST.get('password')
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, "Invalid email or password")
                return redirect('login')

            user = authenticate(username=user.username, password=password)
            if user:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Invalid email or password")

        # Phone login
        elif 'phone' in request.POST:
            phone = request.POST.get('phone')
            password = request.POST.get('phone_password')

            try:
                profile = Profile.objects.get(phone_number=phone)
                user = profile.user
            except Profile.DoesNotExist:
                messages.error(request, "Phone number not registered")
                return redirect('login')

            user = authenticate(username=user.username, password=password)
            if user:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Invalid phone credentials")

    return render(request, 'users/login.html')



def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            Profile.objects.create(user=user, phone_number=form.cleaned_data['phone_number'])
            messages.success(request, "Registration successful! Please log in.")
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})



def logout_view(request):
    logout(request)
    return redirect('home')
