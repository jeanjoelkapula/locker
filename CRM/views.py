from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from .models import * 
from .forms import *
import json
from django.db.models import Q
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
    pipelines = Pipeline.objects.all()

    context = {
        'pipelines': pipelines
    }
    return render(request, 'crm/pipeline_list.html', context)

def pipeline_edit(request, pipeline_id):
    try:
        pipeline = Pipeline.objects.get(pk=pipeline_id)
    except Pipeline.DoesNotExist:
        return HttpResponse('Page not found')
        
    if request.method == "GET":

        context = {
            'pipeline': pipeline
        }
        return render(request, 'crm/pipeline_edit.html', context)

    if request.method == "POST":
        data = json.loads(request.body)

        #update user following
        if data.get('pipeline_name'):
            if data.get('steps'):

                pipeline.name= data.get('pipeline_name')

                is_valid = True
                stages = []
                for stage in data.get('steps'):
                    if len(stage['tasks']) == 0:
                        is_valid = False
                    else:
                        stages.append(PipelineStage(step=stage['step'], name=stage['stage_name'], pipeline=pipeline, guidance= stage['guidance']))

                if is_valid:
                    pipeline.save()
                    pipeline.stages.all().delete()
                    for i in range(0, len(stages)):
                        stages[i].save()
                        for task in data.get('steps')[i]['tasks']:
                            task = Task(name=task['task_name'], pipeline_stage=stages[i])
                            task.save()

                    return JsonResponse({"success": "Pipeline was successfully edited"}, status=201)
                else:
                    return JsonResponse({"error": "Please ensure each stage has at least one task"}, status=403)

            else:
                return JsonResponse({"error": "No pipeline name specified"}, status=403)

        else:
            return JsonResponse({"error": "No pipeline name specified"}, status=403)

def leads_list(request):
    context = {
        'leads': Lead.objects.all()
    }
    return render(request, "crm/leads_list.html", context)

def leads_create(request):
    if request.method == "GET":
        products = request.user.customer.products.all()
        pipelines = Pipeline.objects.all()
        sources = LeadSource.objects.all()
        companies = request.user.customer.companies.all()
        people = companies.first().members.all()
        context = {
            'products': products,
            'sources': sources,
            'pipelines': pipelines,
            'companies': companies,
            'people': people
        }

        return render(request, "crm/leads_create.html", context)

def lead_page(request, lead_id):
    try:
        lead = Lead.objects.get(id=lead_id)
        statuses = LeadStatus.objects.filter(~Q(name="Won"))
        context = {
            'lead': lead,
            'statuses': statuses
        }
    except Lead.DoesNotExist:
        return HttpResponse('This page does not exist')

    return render(request, "crm/leads_page.html", context)

def update_lead_status(request, lead_id):
    if request.method == "POST":
        data = json.loads(request.body)
        if data.get('status'):
            try:
                lead = Lead.objects.get(pk=lead_id)
                s = LeadStatus.objects.get(pk=int(data.get('status')))

                if lead.status.name == "Open" or lead.status.name == "Lost" or lead.status.name == 'Cancelled':
                    lead.status = s
                    lead.save()

                    return JsonResponse({"success": "Lead was successfully updated", "status":s.serialize()}, status=200)
                else:
                    return JsonResponse({"error": "Lead cannot be updated", "status":s.serialize()}, status=200)
            except Lead.DoesNotExist:
                return JsonResponse({"error": "Lead does not exist"}, status=200)
        else:
            return JsonResponse({"error": "Status value required"}, status=200)
    else:
        return JsonResponse({
            "error": "POST request required."
        }, status=400)

def products_create(request):
    if request.method == "GET":
        context = {
            'form': ProductForm(initial={'unit': Unit.objects.first().id})
        }
        return render(request, "crm/products_create.html", context)

    if request.method =="POST":
        form = ProductForm(request.POST)

        if form.is_valid():
            if form.cleaned_data['is_service'] == False:
                form.cleaned_data['unit'] = None
            form.instance.customer = request.user.customer
            form.save()
            return HttpResponseRedirect(reverse('products_create'))
        else:
            context = {
                'form': form
            }
            return render(request, "crm/products_create.html", context)

def products_list(request):
    if request.method == "GET":
        products = Product.objects.all()
        context = {
            'products': products
        }
        return render(request, "crm/products_list.html", context)

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

def save_lead(request):
    if request.method == "POST":
        data = json.loads(request.body)
        valid = True
        message = ""
        pipeline = None
        source = None
        company = None
        products = []
        people = []

        #update user following
        if data.get('lead_name') is  None:
            valid = False
            message += f"* Lead name missing \n"

        if data.get('closed_date') is None:
            valid = False
            message += f"* Expected closed date missing \n"

        if data.get('pipeline') is  None:
            valid = False
            message += f"* Pipeline missing \n"
        else:
            try:
                pipeline = Pipeline.objects.get(pk=int(data.get('pipeline')))
            except Pipeline.DoesNotExist:
                valid = False

        if data.get('confidence') is  None:
            valid = False
            message += f"* Confidence level missing \n"

        if data.get('priority') is  None:
            valid = False
            message += f"* Priority missing \n"

        if data.get('company') is  None:
            valid = False
            message += f"* Company missing \n"
        else:
            try:
                company = Company.objects.get(pk=data.get('company'))
            except Company.DoesNotExist:
                valid = False

        if data.get('source') is  None:
            valid = False
            message += f"* Expected closed date missing \n"
        else:
            try:
                source = LeadSource.objects.get(pk=int(data.get('source')))
            except LeadSource.DoesNotExist:
                valid = False

        if data.get('products') is  None:
            valid = False
            message += f"* Products missing \n"
        else:
            if len(data.get('products')) == 0:
                valid = False
            else:
                for item in data.get('products'):
                    try:
                        product = Product.objects.get(pk=item['id'])
                        products.append(ProductLine(product=product, quantity=item['quantity']))
                    except Product.DoesNotExist:
                        valid = False
                        break


        if data.get('people') is  None:
            valid = False
            message += f"* People date missing \n"
        else:
            if len(data.get('people')) == 0:
                valid = False
            else:
                for item in data.get('people'):
                    try:
                        person = CompanyMember.objects.get(pk=item['id'])
                        people.append(person)
                    except CompanyMember.DoesNotExist:
                        valid = False
                        break
        if valid:
            status = LeadStatus.objects.get(name='Open')
            lead = Lead(name=data.get('lead_name'), expected_close_date=data.get('closed_date'), pipeline = pipeline, company= company, source=source, customer=request.user.customer, confidence = data.get('confidence'), is_hot=data.get('priority'), status=status)
            lead.save()

            for product in products:
                product.save()
                lead.product_lines.add(product)

            for person in people:
                lead.people.add(person)

            LeadProgress(lead=lead).save()

            return JsonResponse({"success": "Lead was successfully created"}, status=200)
        else:
            return JsonResponse({"error": message}, status=200)

    else:
        return JsonResponse({
            "error": "POST request required."
        }, status=400)
def advance_to_stage(request, lead_id):
    if request.method == "POST":
        try:
            lead = Lead.objects.get(pk=lead_id)
            progress = LeadProgress.objects.get(lead=lead)

            data = json.loads(request.body)

            if data.get('stage'):
                try:
                    stage = PipelineStage.objects.get(pk=int(data.get('stage')))
                    for step in lead.pipeline.stages.all():
                        if step.step <= stage.step:
                            progress.task_lines.filter(task__pipeline_stage=step).update(is_complete=True)
                    
                    is_lead_complete = False

                    if len(progress.task_lines.all()) == len(progress.task_lines.filter(is_complete=True)):
                        is_lead_complete = True
                        s = LeadStatus.objects.get(name="Won")
                        lead.status = s
                        lead.save()

                    return JsonResponse({"success": "Succesfully advanced to next stage", "is_lead_complete": is_lead_complete, "status": lead.status.serialize()}, status=200)
                except PipelineStage.DoesNotExist:
                    return JsonResponse({"error": "Stage does not exist"}, status=200)

        except Lead.DoesNotExist:
            return JsonResponse({"error": "Lead does not exist"}, status=200)
    else:
        return JsonResponse({
            "error": "POST request required."
        }, status=400)

def complete_task(request, task_id):
    if request.method =="POST":
        data = json.loads(request.body)
        try:
            task = Task.objects.get(pk=task_id)
            try:
                lead = Lead.objects.get(pk=int(data.get('lead')))
            except Lead.DoesNotExist:
                return JsonResponse({"error": "Lead does not exist"}, status=200)

            progress = LeadProgress.objects.get(lead=lead)
            task_line = progress.task_lines.get(task=task)
            task_line.is_complete = data.get('is_complete')
            task_line.save()
            complete = progress.task_lines.filter(task__pipeline_stage=task.pipeline_stage).filter(is_complete=True)
            is_stage_complete = (len(complete) == len(task.pipeline_stage.tasks.all()))

            if is_stage_complete:
                for step in lead.pipeline.stages.all():
                    if step.step <= task.pipeline_stage.step:
                        progress.task_lines.filter(task__pipeline_stage=step).update(is_complete=True)


            is_lead_complete = False

            if len(progress.task_lines.all()) == len(progress.task_lines.filter(is_complete=True)):
                is_lead_complete = True
                s = LeadStatus.objects.get(name="Won")
                lead.status = s
                lead.save()

            return JsonResponse({"success": "Task was successfully updated", "is_stage_complete": is_stage_complete, "is_lead_complete": is_lead_complete, "status": lead.status.serialize()}, status=200)
        except Task.DoesNotExist:
            return JsonResponse({"error": "Task does not exist"}, status=200)
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