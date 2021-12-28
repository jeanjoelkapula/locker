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

class CompanyMemberForm(forms.ModelForm):
    class Meta:
        model = CompanyMember
        fields = '__all__'
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control rounded-left', 'placeholder':'First name', 'required': True}),
            'last_name': forms.TextInput(attrs={'class': 'form-control rounded-left', 'placeholder':'Last name', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-control rounded-left', 'placeholder':'Email', 'required': False}),
            'phone': forms.TextInput(attrs={'class': 'form-control rounded-left', 'placeholder': 'Phone number'}),
            'company': forms.Select(attrs={'class':'custom-select'})
        }
        labels = {
            'first_name': _('First name'),
            'last_name': _('Last name'),
            'email': _('Email'),
            'phone': _('Phone number'),
            'company': _('Company'),
        }
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['customer']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control rounded-left', 'placeholder':'Product name', 'required': True}),
            'is_service': forms.CheckboxInput(attrs={'class': 'custom-control-input'}),
            'price': forms.NumberInput(attrs={'class':'form-control'}),
            'unit': forms.Select(attrs={'class':'custom-select', 'required': 'true'})

        }
        labels = {
            'name': _('Product name'),
            'is_service': _('Product type'),
            'unit': _('Product unit'),
            'price': _('Product price'),
        }

        
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['unit'].empty_label = None

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        exclude = ['status, product_lines, customer']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control rounded-left', 'placeholder':'Lead name', 'required': True}),
            'expected_closed_date' : forms.TextInput(attrs={'class': 'form-control rounded-left', 'placeholder':'Expected closed date'}),
            'pipeline': forms.Select(attrs={'class':'custom-select'}),
            'is_hot': forms.CheckboxInput(attrs={'class': 'custom-control-input'}),
            'confidence': forms.TextInput(attrs={'class': 'bs-slider-variant', "data-slider-min":"1", "data-slider-max":"100", "data-slider-step":"1", "data-slider-value":"14" ,"style": "display: none;", "data-value" :"9", "value":"9"}),
            'source': forms.Select(attrs={'class':'custom-select'}),
        }
        labels = {
            'name':  _('Lead name'),
            'expected_closed_date':  _('Expected closed date'),
            'pipeline':  _('Pipeline'),
            'is_hot':  _('Priority'),
            'confidence':  _('Confidence'),
            'source':  _('Source'),
        }