from .models import * 
from django import forms
from django.utils.translation import gettext_lazy as _

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control rounded-left', 'placeholder':'First name', 'required': True}),
            'last_name': forms.TextInput(attrs={'class': 'form-control rounded-left', 'placeholder':'Last name', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-control rounded-left', 'placeholder':'Email', 'required': True}),
            'password': forms.PasswordInput(attrs={'class': 'form-control rounded-left', 'placeholder':'Password', 'required': True}),
        }
        labels = {
            'first_name': _('First name'),
            'last_name': _('Last name'),
            'email': _('Email'),
            'password': _('Password'),
        }

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['customer_name', 'customer_phone', 'customer_email']
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control rounded-left', 'placeholder': 'What is your company name?'}),
            'customer_phone': forms.TextInput(attrs={'class': 'form-control rounded-left', 'placeholder': 'What is your company phone number?'}),
            'customer_email': forms.EmailInput(attrs={'class': 'form-control rounded-left', 'placeholder': 'What is your company email?'}),
        }
        labels = {
            'customer_name': _('What is your company name?'),
            'customer_phone': _('What is your company phone number?'),
            'customer_email': _('What is your company email?'),
        }

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        exclude = ['customer']
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control rounded-left', 'placeholder': 'Company name'}),
            'company_phone': forms.TextInput(attrs={'class': 'form-control rounded-left', 'placeholder': 'Company phone'}),
            'company_email': forms.EmailInput(attrs={'class': 'form-control rounded-left', 'placeholder': 'Company email'}),
            'company_address': forms.TextInput(attrs={'class': 'form-control rounded-left', 'placeholder': 'Company address'}),
            'company_URL': forms.URLInput(attrs={'class': 'form-control rounded-left', 'placeholder': 'URL'}),
            'company_description': forms.TextInput(attrs={'class': 'form-control rounded-left', 'placeholder': 'Company description'}),
        }
        labels = {
            'company_name': _('Company Name'),
            'company_phone': _('Phone'),
            'company_email': _('Email'),
            'company_address': _('Address'),
            'company_URL': _('URL'),
            'company_description': _('Description'),
        }
