from django.contrib.auth.forms import UserCreationForm
from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe
class CustomErrorList(ErrorList):
    def __str__(self):
        if not self:
            return ''
        return mark_safe(''.join([
            f'<div class="alert alert-danger" role="alert">{e}</div>' for e in self]))
class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1',
        'password2']:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget.attrs.update(
                {'class': 'form-control'}
            )

# # accounts/forms.py
# from django import forms
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import PasswordResetForm
#
#
# class UsernamePasswordResetForm(forms.Form):
#     username = forms.CharField(label="Username", max_length=150)
#     new_password1 = forms.CharField(label="New Password", widget=forms.PasswordInput)
#     confirm_password1 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)
#
#     def clean_password(self):
#         username = self.cleaned_data["username"]
#         try:
#             user = User.objects.get(username=username)
#             password =
#         except User.DoesNotExist:
#             raise forms.ValidationError("No user with this username exists.")
#
#         # Instead of using email, we retrieve the email associated with the username
#         self.cleaned_data["email"] = user.email
#         return username


# class CustomPasswordResetForm(forms.Form): username = forms.CharField(label='Username', max_length=150)
#
# new_password = forms.CharField(label='New Password', widget=forms.PasswordInput)
# confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
#
# def clean(self):
#     cleaned_data = super().clean()
#     username = cleaned_data.get("username")
#     password = cleaned_data.get("new_password")
#     confirm_password = cleaned_data.get("confirm_password")
#     # Check if username exists if not
#     User.objects.filter(username=username).exists():
#     raise ValidationError("No user found with this username.")
#     # Check if passwords match
#     if password != confirm_password: raise ValidationError("Passwords do not match.")
#     return cleaned_data


# accounts/forms.py
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class CustomPasswordResetForm(forms.Form):
    username = forms.CharField(label='Username', max_length=150)
    new_password = forms.CharField(label='New Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        # Check if the username exists
        if not User.objects.filter(username=username).exists():
            raise ValidationError("No user found with this username.")

        # Check if passwords match
        if new_password != confirm_password:
            raise ValidationError("Passwords do not match.")

        return cleaned_data
