from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from .models import * 
from .forms import *
from . import util
import json
from django.db.models import Sum
from datetime import datetime,date, timedelta
from django.db.models import Q
from django.contrib.auth.hashers import make_password


# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    sales_count = 0
    for sale in Sale.objects.filter(date__month=datetime.now().month, customer = request.user.customer):
        sales_count += sale.lead.value()
    
    total_sales = Sale.objects.filter(customer = request.user.customer)
    total_sales_income = 0
    total_sales_count = len(total_sales)

    for sale in total_sales:
        total_sales_income += sale.lead.value()
    
    sales_lost = Lead.objects.filter(customer=request.user.customer, status__name='Lost')
    total_sales_loss = 0
    start_index = 1
    last_sale_date = total_sales.last().date

    start_index = datetime.now().month - 8
    month_sales = []
    month_losses = []
    labels = []
    prev = date.today()
    for i in range(0,8):
        datetime_object = datetime.strptime(str((prev.month)), "%m")
        month_name = datetime_object.strftime("%b")
        month_sales.append(len(total_sales.filter(date__month=prev.month)))
        month_losses.append(len(LeadLoss.objects.filter(date__month=prev.month)))
        labels.append(f"{month_name} - {prev.year}")
        prev = prev.replace(day=1) - timedelta(days=1)
        
        #month_losses = Lead.objects.filter(customer = request.user.customer, )
    labels.reverse()
    month_losses.reverse()
    month_sales.reverse()
    stat_chart_data = {
        'labels': labels,
        'datasets': [
            {
                'label': 'Sales',
                'data': month_sales,
                'borderWidth': 1,
                'backgroundColor': 'rgba(28,180,255,.05)',
                'borderColor': 'rgba(28,180,255,1)'
            },
            {
            'label': 'Losses',
            'data': month_losses,
            'borderWidth': 1,
            'backgroundColor': 'rgba(136, 151, 170, 0.1)',
            'borderColor': '#8897aa'
            }
        ]
    }

    sales_loss_count = len(sales_lost)
    for lead in sales_lost:
        total_sales_loss += lead.value()
    
    hot_leads = Lead.objects.filter(customer=request.user.customer, is_hot=True).order_by('-expected_close_date')

    leads_pie_chart_data =  {
      'labels': ['Lost Leads', 'Open Leads', 'Leads Won'],
      'datasets': [{
        'data': [len(Lead.objects.filter(customer=request.user.customer, status__name='Lost')), len(Lead.objects.filter(customer=request.user.customer, status__name='Open')), len(Lead.objects.filter(customer=request.user.customer, status__name='Won'))],
        'backgroundColor': ['rgba(99,125,138,0.5)', 'rgba(28,151,244,0.5)', 'rgba(2,188,119,0.5)'],
        'borderColor': ['#647c8a', '#2196f3', '#02bc77'],
        'borderWidth': 1
      }]
    }

    pipeline = Pipeline.objects.filter(customer=request.user.customer).last()

    stage_lead_counts = util.get_stage_stats(pipeline)

    current_month_sales = Sale.objects.filter(date__month=datetime.now().month)
    current_month_sales_value = 0
    for sale in current_month_sales:
        current_month_sales_value += sale.lead.value()
    
    doughtnut_progress = (current_month_sales_value * 100) / request.user.customer.sales_target
    if (100 - doughtnut_progress) > 0:
        doughnut_remainder = 100 - doughtnut_progress
    else:
        doughnut_remainder = 0

    doughnut_chart_data = [{
        'data': [doughtnut_progress, doughnut_remainder],
        'backgroundColor': ['#fff', 'rgba(255,255,255,0.3)'],
        'hoverBackgroundColor': ['#fff', 'rgba(255,255,255,0.3)'],
        'borderWidth': 0
    }]

    date_object = datetime.strptime(str((datetime.now().month)), "%m")
    full_month_name = datetime_object.strftime("%B")
    date_today = f"Today is, {datetime.now().day} {full_month_name} {datetime.now().year}"
    context = {
        'sales_count': sales_count,
        'products_count': len(Product.objects.filter(customer=request.user.customer)),
        'companies_count': len(Company.objects.filter(customer=request.user.customer)),
        'people_count': len(CompanyMember.objects.filter(company__customer = request.user.customer)),
        'total_sales': total_sales,
        'total_sales_income': total_sales_income,
        'total_sales_count': total_sales_count,
        'sales_loss_count': sales_loss_count,
        'sales_lost': sales_lost,
        'total_sales_loss': total_sales_loss,
        'stat_chart_data': stat_chart_data,
        'hot_leads': hot_leads, 
        'leads_pie_chart_data': leads_pie_chart_data,
        'pipeline_list': Pipeline.objects.filter(customer=request.user.customer),
        'stage_lead_counts': stage_lead_counts,
        'doughnut_chart_data': doughnut_chart_data,
        'current_month_sales_value': current_month_sales_value,
        'doughtnut_progress': doughtnut_progress,
        'date_today': date_today
    }

    return render(request, "crm/index.html", context)


def stage_stats(request, pipeline_id):
    if request.method == "GET":
        try:
            pipeline = Pipeline.objects.get(pk=pipeline_id)
            stats = util.get_stage_stats(pipeline)

            return JsonResponse({"success": True, 'stats': stats}, status=200)
        except Pipeline.DoesNotExist:
            return JsonResponse({"error": "Pipeline does not exist"}, status=200)
    else:
        return JsonResponse({
            "error": "GET request required."
        }, status=400)

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
    companies = Company.objects.filter(customer=request.user.customer)
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
        'members': CompanyMember.objects.filter(company__customer=request.user.customer)
    }
    return render(request, "crm/people_list.html", context)

def pipeline_create(request):
    return render(request, 'crm/pipeline_create.html')

def pipeline_list(request):
    pipelines = Pipeline.objects.filter(customer = request.user.customer)

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
        'leads': Lead.objects.filter(customer= request.user.customer)
    }
    return render(request, "crm/leads_list.html", context)

def leads_create(request):
    if request.method == "GET":
        products = request.user.customer.products.all()
        pipelines = Pipeline.objects.filter(customer= request.user.customer)
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
                
                    if lead.status.name == "Lost":
                        obj, created = LeadLoss.objects.get_or_create(lead=lead, reason=data.get('reason'))
                    
                    if lead.status.name == "Open":
                        LeadLoss.objects.filter(lead=lead).delete()

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
        products = Product.objects.filter(customer= request.user.customer)
        context = {
            'products': products
        }
        return render(request, "crm/products_list.html", context)

def settings(request):  
    context={
        'user_form': SettingsUserForm(instance=request.user),
        'customer_form': CustomerForm(instance=request.user.customer)
    }
    return render(request, "crm/settings.html", context)

def settings_account(request):
    if request.method == "POST":
        user_form = SettingsUserForm(request.POST, instance=request.user)

        if user_form.is_valid():
            user_form.save()

            return HttpResponseRedirect(reverse("settings"))
        else:
            context = {
                'user_form': user_form,
                'customer_form': CustomerForm(instance=request.user.customer)
            }

            return render(request, "crm/settings.html", context)

    if request.method == "GET":
        context={
            'user_form': SettingsUserForm(instance=request.user),
            'customer_form': CustomerForm(instance=request.user.customer)
        }
        return render(request, "crm/settings.html", context)

def settings_customer(request):
    if request.method == "POST":
        customer_form = CustomerForm(request.POST, instance=request.user.customer)

        if customer_form.is_valid():
            customer_form.save()

            return HttpResponseRedirect(reverse("settings"))
        else:
            context = {
                'customer_form': SettingsUserForm(instance=request.user),
                'customer_form': customer_form
            }

            return render(request, "crm/settings.html", context)

    if request.method == "GET":
        context={
            'user_form': SettingsUserForm(instance=request.user),
            'customer_form': CustomerForm(instance=request.user.customer)
        }
        return render(request, "crm/settings.html", context)

def settings_password(request):
    if request.method == "POST":
        current_message = None
        match_message = None
        new_password = None
        current_password = None
        repeat_password = None
        
        if request.POST.get('current-password'):
            current_password = request.POST['current-password']
        
        if request.POST.get('new-password'):
            new_password = request.POST['new-password']
    
        if request.POST.get('repeat-password'):
            repeat_password = request.POST['repeat-password']

        if  (new_password is None) or (repeat_password is None) or (current_password is None):
            match_message = "Please fill out the form"
            context = {
                'user_form': SettingsUserForm(instance=request.user),
                'customer_form': CustomerForm(instance=request.user.customer),
                'current_password': current_message,
                'current_message': current_message,
                'match_message': match_message,
                'new_password': new_password,
                'repeat_password': repeat_password
            }

            return render(request, "crm/settings.html", context)

        result = authenticate(request, username=request.user.username, password=current_password)
        if result is None:
            current_message = "Current password is invalid"
            context = {
                'user_form': SettingsUserForm(instance=request.user),
                'customer_form': CustomerForm(instance=request.user.customer),
                'current_password': current_message,
                'current_message': current_message,
                'match_message': match_message,
                'new_password': new_password,
                'repeat_password': repeat_password
            }

            return render(request, "crm/settings.html", context)
        
        if new_password != repeat_password:
            match_message = "Password does not match"

            context = {
                'user_form': SettingsUserForm(instance=request.user),
                'customer_form': CustomerForm(instance=request.user.customer),
                'current_password': current_message,
                'current_message': current_message,
                'match_message': match_message,
                'new_password': new_password,
                'repeat_password': repeat_password
            }

            return render(request, "crm/settings.html", context)
        elif new_password.strip() == '':
            match_message = "Please enter a valid password"
            context = {
                'user_form': SettingsUserForm(instance=request.user),
                'customer_form': CustomerForm(instance=request.user.customer),
                'current_password': current_message,
                'current_message': current_message,
                'match_message': match_message,
                'new_password': new_password,
                'repeat_password': repeat_password
            }

            return render(request, "crm/settings.html", context)

        if (current_message is None) and (match_message is None):

            request.user.password = make_password(new_password)
            user = request.user
            request.user.save()
            login(request, user)
            return HttpResponseRedirect(reverse("settings"))

    if request.method == "GET":
        context={
            'user_form': SettingsUserForm(instance=request.user),
            'customer_form': CustomerForm(instance=request.user.customer)
        }
        return render(request, "crm/settings.html", context)

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

                        obj, created = Sale.objects.get_or_create(lead=lead)

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
                obj, created = Sale.objects.get_or_create(lead=lead)

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