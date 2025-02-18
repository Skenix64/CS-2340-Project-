from django.shortcuts import render
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from .forms import CustomUserCreationForm, CustomErrorList
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User



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


from .forms import CustomPasswordResetForm
from django.contrib.auth.hashers import make_password
# accounts/views.py
# def resetpassword(request):
#     if request.method == 'POST':
#         form = CustomPasswordResetForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             new_password = form.cleaned_data['new_password']
#
#         # Update the user's password
#         try: user = User.objects.get(username=username)
#         user.password = make_password(new_password)
#         user.save() messages.success(request, 'Password reset successfully. You can now log in.')
#         return redirect('accounts.password_reset')
#         except User.DoesNotExist: messages.error(request, 'User not found.')
#         else:
#         messages.error(request, 'Invalid form submission.')
#         else: form = CustomPasswordResetForm()
#         return render(request, 'accounts/password_reset.html', {'form': form})


# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .forms import CustomPasswordResetForm


def reset_password(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            new_password = form.cleaned_data['new_password']

            try:
                # Get user by username
                user = User.objects.get(username=username)

                # Hash the new password
                user.password = make_password(new_password)
                user.save()  # Save the user with the new password

                # Success message
                messages.success(request, 'Password reset successfully. You can now log in.')
                return redirect('accounts.password_reset_done')  # Redirect to a success page or login page

            except User.DoesNotExist:
                # Error message if user doesn't exist
                messages.error(request, 'User not found.')

        else:
            # Error message for invalid form submission
            messages.error(request, 'Invalid form submission.')
    else:
        form = CustomPasswordResetForm()

    return render(request, '', {'form': form})


# accounts/views.py
from django.contrib.auth import views as auth_views
from .forms import CustomPasswordResetForm

class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    form_class = CustomPasswordResetForm
    success_url = 'password_reset_done'  # Redirect after a successful password reset request



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import check_password, make_password

# Temporary token storage (consider using a model for production)
reset_tokens = {}

def reset_request_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user = User.objects.filter(username=username).first()

        if user:
            token = get_random_string(32)  # Generate secure reset token
            reset_tokens[token] = username  # Store token (should use DB in real app)
            return redirect('reset_password', token=token)
        else:
            messages.error(request, "Username not found!")

    return render(request, 'accounts/reset_request.html')


# def reset_password_view(request, token):
#     if token not in reset_tokens:
#         messages.error(request, "Invalid or expired token!")
#         return redirect('reset_request')
#
#     username = reset_tokens[token]
#     user = get_object_or_404(User, username=username)
#
#     if request.method == 'POST':
#         new_password = request.POST.get('new_password')
#         confirm_password = request.POST.get('confirm_password')
#
#         # Password validation
#         if len(new_password) < 8:
#             messages.error(request, "Password must be at least 8 characters long!")
#         elif check_password(new_password, user.password):
#             messages.error(request, "New password cannot be the same as the old password!")
#         elif new_password != confirm_password:
#             messages.error(request, "Passwords do not match!")
#         else:
#             user.password = make_password(new_password)
#             user.save()
#             del reset_tokens[token]  # Remove token after reset
#             messages.success(request, "Password successfully reset! Please log in.")
#             return redirect('login')
#
#     return render(request, 'accounts/reset_password.html')

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password, make_password
from django.contrib import messages

def reset_password_view(request, token):
    if token not in reset_tokens:
        messages.error(request, "Invalid or expired token!")
        return redirect('reset_request')

    username = reset_tokens[token]
    user = get_object_or_404(User, username=username)

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Password validation
        if len(new_password) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
        elif check_password(new_password, user.password):
            messages.error(request, "New password cannot be the same as the old password.")
        elif new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
        else:
            # Save the new password
            user.password = make_password(new_password)
            user.save()

            # Remove the token after a successful reset
            del reset_tokens[token]

            messages.success(request, "Password successfully reset! Please log in.")
            return redirect('accounts.login')

    return render(request, 'accounts/reset_password.html', {'token': token})

