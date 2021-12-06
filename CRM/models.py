from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE, DO_NOTHING

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    phone = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)

class User(AbstractUser):
    customer = models.ForeignKey(Customer, null=True, blank=True, related_name="business_users", on_delete=CASCADE)

class Company(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    email = models.EmailField(max_length=254, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    URL = models.URLField(null=True, blank=True)      
    customer = models.ForeignKey(Customer, null=False, blank=False, related_name="companies", on_delete=CASCADE)   

class CompanyMember(models.Model):
    first_name = models.CharField(max_length=64, null=False, blank=False)
    last_name = models.CharField(max_length=64, null=False, blank=False)
    email = models.EmailField(max_length=254, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    company = models.ForeignKey(Company, null=False, blank=False, related_name="members", on_delete=CASCADE)

class Unit(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)

class Product(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    is_service = models.BooleanField(null=False, blank=False)
    price = models.FloatField(null=False, blank=False)
    unit = models.ForeignKey(Unit, null=True, blank=True, on_delete=DO_NOTHING)
    customer = models.ForeignKey(Customer, null=False, blank=False, related_name="products", on_delete=CASCADE)  

class ProductLine(models.Model):
    product = models.ForeignKey(Product, null=False, blank=False, on_delete=DO_NOTHING)
    quantity = models.IntegerField()

class Pipeline(models.Model):
    customer = models.ForeignKey(Customer, null=False, blank=False, related_name="pipelines", on_delete=CASCADE)  

class PipelineStage(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    pipe_line = models.ForeignKey(Pipeline, null=False, blank=False, related_name="stages", on_delete=CASCADE)


class Task(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    pipeline_stage = models.ForeignKey(PipelineStage, null=False, blank=False, related_name="tasks", on_delete=CASCADE)
    is_complete = models.BooleanField(null=False, blank=False, default= False)

class LeadSource(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)

class LeadStatus(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)

class Lead(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    expected_close_date = models.DateField()
    pipe_line = models.ForeignKey(Pipeline, null=False, blank=False, on_delete=DO_NOTHING)
    confidence = models.IntegerField()
    is_hot = models.BooleanField(default=False)
    source = models.ForeignKey(LeadSource, null=False, blank=False, related_name="leads", on_delete=DO_NOTHING)
    status = models.ForeignKey(LeadStatus, null=False, blank=False, related_name="leads", on_delete=DO_NOTHING)
    product_lines = models.ManyToManyField(ProductLine)
    customer = models.ForeignKey(Customer, null=False, blank=False, related_name="leads", on_delete=CASCADE)  