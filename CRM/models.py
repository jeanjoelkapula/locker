from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE, DO_NOTHING

# Create your models here.
class Customer(models.Model):
    customer_name = models.CharField(max_length=255, null=False, blank=False)
    customer_phone = models.CharField(max_length=15, null=True, blank=True)
    customer_email = models.EmailField(max_length=254, null=True, blank=True)
    sales_target = models.FloatField(null=True, blank=True, default=1000)
    
    def __str__(self):
        return f"{self.customer_name}"

class User(AbstractUser):
    customer = models.ForeignKey(Customer, null=True, blank=True, related_name="business_users", on_delete=CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.username}"

class Company(models.Model):
    company_name = models.CharField(max_length=255, null=False, blank=False)
    company_email = models.EmailField(max_length=254, null=True, blank=True)
    company_phone = models.CharField(max_length=15, null=True, blank=True)
    company_address = models.CharField(max_length=255, null=True, blank=True)
    company_description = models.CharField(max_length=255, null=True, blank=True)
    company_URL = models.URLField(null=True, blank=True)      
    customer = models.ForeignKey(Customer, null=False, blank=False, related_name="companies", on_delete=CASCADE)   

    def __str__(self):
        return f"{self.company_name}"
    
    def  serialize(self):
        return {
            'id': self.id,
            'company_name': self.company_name,
            'members': [{'id': member.id, 'first_name': member.first_name, 'last_name': member.last_name} for member in self.members.all()]
        }

class CompanyMember(models.Model):
    first_name = models.CharField(max_length=64, null=False, blank=False)
    last_name = models.CharField(max_length=64, null=False, blank=False)
    email = models.EmailField(max_length=254, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    company = models.ForeignKey(Company, null=False, blank=False, related_name="members", on_delete=CASCADE)

    def __str__(self):
        return f"{self.company} - {self.first_name} {self.last_name}"

    def serialize(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
        }

class Unit(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return f"{self.name}"

class Product(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    is_service = models.BooleanField(null=False, blank=False)
    price = models.FloatField(null=False, blank=False)
    unit = models.ForeignKey(Unit, null=True, blank=True, on_delete=DO_NOTHING)
    customer = models.ForeignKey(Customer, null=False, blank=False, related_name="products", on_delete=CASCADE)  

    def __str__(self):
        return f"{self.name}"

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'unit': self.unit.name,
        }

class ProductLine(models.Model):
    product = models.ForeignKey(Product, null=False, blank=False, on_delete=DO_NOTHING)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.product} - {self.quantity}"

class Pipeline(models.Model):
    customer = models.ForeignKey(Customer, null=False, blank=False, related_name="pipelines", on_delete=CASCADE)  
    name = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return f"{self.name}"

class PipelineStage(models.Model):
    step = models.IntegerField()
    guidance = models.CharField(max_length=255, null=False, blank=False)
    name = models.CharField(max_length=255, null=False, blank=False)
    pipeline = models.ForeignKey(Pipeline, null=False, blank=False, related_name="stages", on_delete=CASCADE)

    def __str__(self):
        return f"{self.name}"

    def serialize(self):
        return {
            'step': self.step,
            'stage_name': self.name,
            'guidance': self.guidance,
            'tasks': [{'id': task.id, 'task_name':task.name} for task in self.tasks.all()]
        }

class Task(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    pipeline_stage = models.ForeignKey(PipelineStage, null=False, blank=False, related_name="tasks", on_delete=CASCADE)

    def __str__(self):
        return f"{self.name}"

class TaskProgessLine(models.Model):
    task = models.ForeignKey(Task, null=False, blank=False, on_delete=CASCADE)
    is_complete = models.BooleanField(null=False, blank=False, default= False)

    def __str__(self):
        return f"task - {self.task} stage id: {self.task.pipeline_stage.id} stage name: {self.task.pipeline_stage}"
class LeadSource(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return f"{self.name}"

class LeadStatus(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return f"{self.name}"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }

class Lead(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    expected_close_date = models.DateField()
    pipeline = models.ForeignKey(Pipeline, null=False, blank=False, on_delete=DO_NOTHING, related_name="leads")
    confidence = models.IntegerField()
    is_hot = models.BooleanField(default=False)
    source = models.ForeignKey(LeadSource, null=False, blank=False, related_name="leads", on_delete=DO_NOTHING)
    status = models.ForeignKey(LeadStatus, null=False, blank=False, related_name="leads", on_delete=DO_NOTHING)
    product_lines = models.ManyToManyField(ProductLine)
    people = models.ManyToManyField(CompanyMember)
    company = models.ForeignKey(Company, blank=False, null=False, on_delete=CASCADE)
    customer = models.ForeignKey(Customer, null=False, blank=False, related_name="leads", on_delete=CASCADE) 
    opened_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"
    
    def value(self):
        value = 0
        for product_line in self.product_lines.all():
            value += product_line.product.price * product_line.quantity

        return value
    
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'status': self.status.serialize(),
            'pipeline_stages': [item.serialize() for item in  self.pipeline.stages.all()]
        }

class LeadProgress(models.Model):
    lead = models.ForeignKey(Lead, null=False, blank=False, on_delete=CASCADE)
    task_lines = models.ManyToManyField(TaskProgessLine, blank=True)

    def save(self, *args, **kwargs):
        super(LeadProgress, self).save(*args, **kwargs)
        for stage in self.lead.pipeline.stages.all():
            for task in stage.tasks.all():
                t = TaskProgessLine(task=task)
                t.save()
                self.task_lines.add(t)

    def __str__(self):
        return f"{self.lead}"
class LeadLoss(models.Model):
    lead = models.ForeignKey(Lead, null=False, blank=False, on_delete=CASCADE, related_name="losses")
    customer = models.ForeignKey(Customer, null=False, blank=False, related_name="customer_losses", on_delete=CASCADE) 
    reason = models.TextField(max_length=255, null=False, blank=False)
    date = models.DateField(auto_now_add=True)


class Sale(models.Model):
    lead = models.ForeignKey(Lead, null=False, blank=False, on_delete=CASCADE)
    date = models.DateField(auto_now_add=True)
    customer = models.ForeignKey(Customer, null=False, blank=False, related_name="sales", on_delete=CASCADE) 

    def __str__(self):
        return f"{self.lead}"