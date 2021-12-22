from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from .models import * 
from .forms import *
import json
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

def pipeline_create(request):
    return render(request, 'crm/pipeline_create.html')

def pipeline_list(request):
    return render(request, 'crm/pipeline_list.html')

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

def save_pipeline(request):
    if request.method == "POST":
        data = json.loads(request.body)

        #update user following
        if data.get('pipeline_name'):
            if data.get('steps'):

                pipeline = Pipeline(name= data.get('pipeline_name'), customer=request.user.customer)
                

                is_valid = True
                stages = []
                for stage in data.get('steps'):
                    if len(stage['tasks']) == 0:
                        is_valid = False
                    else:
                        stages.append(PipelineStage(step=stage['step'], name=stage['stage_name'], pipeline=pipeline, guidance= stage['guidance']))

                if is_valid:
                    pipeline.save()

                    for i in range(0, len(stages)):
                        stages[i].save()
                        for task in data.get('steps')[i]['tasks']:
                            task = Task(name=task['task_name'], pipeline_stage=stages[i])
                            task.save()

                    return JsonResponse({"success": "Pipeline was successfully created"}, status=201)
                else:
                    return JsonResponse({"error": "Please ensure each stage has at least one task"}, status=403)

            else:
                return JsonResponse({"error": "No pipeline name specified"}, status=403)

        else:
            return JsonResponse({"error": "No pipeline name specified"}, status=403)
    # Post must be via POST
    else:
        return JsonResponse({
            "error": "POST request required."
        }, status=400)

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