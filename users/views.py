from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UpdateUserForm, UpdateProfileForm
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin


def user_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('user-register')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
            return redirect('user-register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered.')
            return redirect('user-register')

        # Create User
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        
        messages.success(request, f'You are now registered and can log in.')
        return redirect('user-login')
    else:
        return render(request, 'user/register.html')
        
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)  # Pass the user object to the login function
                return redirect('blog-home')  # Redirect to the home page after login
            else:
                # Invalid username or password
                messages.error(request, 'Invalid username or password.')
        else:
            # Invalid form data
            messages.error(request, 'Invalid form data.')
    else:
        form = AuthenticationForm()
    return render(request, 'user/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return render(request, 'user/logout.html')

@login_required
def user_profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='user-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'user/profile.html', {'user_form': user_form, 'profile_form': profile_form})

class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'user/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('blog-home')   