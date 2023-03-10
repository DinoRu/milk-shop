from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from .models import Customer

class LoginForm(AuthenticationForm):
	username = UsernameField(widget=forms.TextInput(attrs={'class': 'form-control', 'autofocus': 'True'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'current-password'}))

class CustomerRegForm(UserCreationForm):
	username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
	password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
	email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

	class Meta:
		model = User
		fields = ['username', 'password1', 'password2', 'email']


class MyPasswordChangeForm(PasswordChangeForm):
	old_password = forms.CharField(label='Old password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete':'current-password'}))
	new_password1 = forms.CharField(label='New password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'current-password'}))
	new_password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete':'current-password'}))


class MyPasswordResetForm(PasswordResetForm):
	email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))


class MySetPasswordForm(SetPasswordForm):
	new_password1 = forms.CharField(label='New password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'current-password'}))
	new_password2 = forms.CharField(label='Confirm new password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'current-password'}))


class CustomerProfileForm(forms.ModelForm):
	class Meta:
		model = Customer
		fields = ['name', 'locality','number', 'city', 'zipcode', 'state']
		widgets = {
			'name': forms.TextInput(attrs={'class': 'form-control'}),
			'city': forms.TextInput(attrs={'class': 'form-control'}),
			'locality': forms.TextInput(attrs={'class': 'form-control'}),
			'number': forms.NumberInput(attrs={'class': 'form-control'}),
			'zipcode': forms.NumberInput(attrs={'class': 'form-control'}),
			'state': forms.Select(attrs={'class': 'form-control'}),
		}
			
	