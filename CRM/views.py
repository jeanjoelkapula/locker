from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import * 
from .forms import *
from django.contrib.auth.hashers import make_password

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    return render(request, "crm/index.html")

def company_create(request):
    if request.method == "POST":
        form = CompanyForm(request.POST)

        if form.is_valid():
            form.instance.customer = request.user.customer
            form.save()

            return HttpResponseRedirect(reverse('company_create'))
        else:
            context = {
            'form': form
        }
        return render(request, "crm/company_create.html", context) 
    else:
        context = {
            'form': CompanyForm()
        }
        return render(request, "crm/company_create.html", context) 

def company_list(request):
    companies = Company.objects.all()
    context = {
        'companies': companies
    }

    return render(request, "crm/company_list.html", context)

def people_create(request):
    if request.method == "POST":
        form = CompanyMemberForm(request.POST)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse('people_create'))
        else:
            context = {
                'form': form
            }
        return render(request, "crm/people_create.html", context)

    else:
        context = {
            'form': CompanyMemberForm()
        }
        return render(request, "crm/people_create.html", context)

def people_list(request):
    context = {
        'members': CompanyMember.objects.all()
    }
    return render(request, "crm/people_list.html", context)

def leads_list(request):
    return render(request, "crm/leads_list.html")

def leads_create(request):
    return render(request, "crm/leads_create.html")

def leads_page(request):
    return render(request, "crm/leads_page.html")

def settings(request):
    return render(request, "crm/settings.html")

def login_view(request):

    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "crm/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "crm/login.html")


def logout_view(request):

    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        user_form = UserForm(request.POST)
        customer_form = CustomerForm(request.POST)

        if user_form.is_valid() and customer_form.is_valid():
            customer_form.save()
            user_form.instance.customer = customer_form.instance
            user_form.instance.username = user_form.cleaned_data['email']
            user_form.instance.password = make_password(user_form.cleaned_data['password'])
            user_form.save()

            login(request, user_form.instance)

            return HttpResponseRedirect(reverse("index"))
        else:
            context = {
                'user_form': user_form,
                'customer_form': customer_form
            }
            return render(request, "crm/register.html", context)
    else:
        context = {
            'user_form': UserForm(),
            'customer_form': CustomerForm()
        }
        return render(request, "crm/register.html", context)