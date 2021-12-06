from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import * 

# Create your views here.
def index(request):
    return render(request, "crm/index.html")

def company_create(request):
    return render(request, "crm/company_create.html") 

def company_list(request):
    return render(request, "crm/company_list.html")

def people_create(request):
    return render(request, "crm/people_create.html")

def people_list(request):
    return render(request, "crm/people_list.html")

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
        email = request.POST["email"]
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        company_name = request.POST['company_name']
        company_phone = request.POST['company_phone']
        company_email = request.POST['company_email']

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "crm/register.html", {
                "message": "Passwords must match."
            })

        # create new customer account
        customer = Customer(name= company_name, phone=company_phone, email=company_email)
        customer.save()

        # Attempt to create new user
        try:
            user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email,password=password, customer=customer)
            user.save()
        except IntegrityError:
            return render(request, "crm/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "crm/register.html")