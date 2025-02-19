from django.shortcuts import render
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from .forms import CustomUserCreationForm, CustomErrorList
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import check_password, make_password
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.contrib.auth import views as auth_views
from .forms import CustomPasswordResetForm

@login_required
def logout(request):
    auth_logout(request)
    return redirect('home.index')

def login(request):
    template_data = {}
    template_data['title'] = 'Login'
    if request.method == 'GET':
        return render(request, 'accounts/login.html',
                      {'template_data': template_data})
    elif request.method == 'POST':
        user = authenticate(
            request,
            username = request.POST['username'],
            password = request.POST['password']
        )
        if user is None:
            template_data['error'] = 'The username or password is incorrect.'
            return render(request, 'accounts/login.html',
                          {'template_data': template_data})
        else:
            auth_login(request, user)
            return redirect('home.index')

def signup(request):
    template_data = {}
    template_data['title'] = 'Sign Up'
    if request.method == 'GET':
        template_data['form'] = CustomUserCreationForm()
        return render(request, 'accounts/signup.html',
                      {'template_data': template_data})
    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST, error_class=CustomErrorList)
        if form.is_valid():
            form.save()
            return redirect('accounts.login')
        else:
            template_data['form'] = form
            return render(request, 'accounts/signup.html',
                          {'template_data': template_data})

@login_required
def orders(request):
    template_data = {}
    template_data['title'] = 'Orders'
    template_data['orders'] = request.user.order_set.all()
    return render(request, 'accounts/orders.html',
                  {'template_data': template_data})


# accounts/views.py
def reset_password(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            new_password = form.cleaned_data['new_password']

            try:
                #retreive username
                user = User.objects.get(username=username)

                # hash new password
                user.password = make_password(new_password)
                user.save()  # Save the user with the new password

                # send a success message
                messages.success(request, 'Password reset successfully. You can now log in.')
                return redirect('accounts.password_reset_done')  # Redirect to a success page or login page

            except User.DoesNotExist:
                # send error message if user not found
                messages.error(request, 'User not found.')

        else:
            # error if improper request
            messages.error(request, 'Invalid form submission.')
    else:
        form = CustomPasswordResetForm()

    return render(request, '', {'form': form})


# accounts/views.py
class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    form_class = CustomPasswordResetForm
    success_url = 'password_reset_done'


reset_tokens = {}

def reset_request_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user = User.objects.filter(username=username).first()

        if user:
            token = get_random_string(32)  # generate token
            reset_tokens[token] = username  # store token
            return redirect('reset_password', token=token)
        else:
            messages.error(request, "Username not found!")

    return render(request, 'accounts/reset_request.html')

#reset password
def reset_password_view(request, token):
    if token not in reset_tokens:
        messages.error(request, "Invalid or expired token!")
        return redirect('reset_request')

    username = reset_tokens[token]
    user = get_object_or_404(User, username=username)

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # make sure password abides by restrictions
        if len(new_password) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
        elif check_password(new_password, user.password):
            messages.error(request, "New password cannot be the same as the old password.")
        elif new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
        else:
            # save new password
            user.password = make_password(new_password)
            user.save()

            # remove token if password successfully reset
            del reset_tokens[token]

            messages.success(request, "Password successfully reset! Please log in.")
            return redirect('accounts.login')

    return render(request, 'accounts/reset_password.html', {'token': token})