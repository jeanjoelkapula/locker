from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Company)
admin.site.register(CompanyMember)
admin.site.register(Unit)
admin.site.register(Product)
admin.site.register(ProductLine)
admin.site.register(Pipeline)
admin.site.register(PipelineStage)
admin.site.register(Task)
admin.site.register(LeadSource)
admin.site.register(LeadStatus)
admin.site.register(Lead)
admin.site.register(TaskProgessLine)
admin.site.register(LeadProgress)
admin.site.register(Sale)


