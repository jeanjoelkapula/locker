from unicodedata import name
from .models import *

def is_stage_complete(stage, lead):
    try:
        progress = LeadProgress.objects.get(lead=lead)
        complete = progress.task_lines.filter(task__pipeline_stage=stage).filter(is_complete=True)
        is_stage_complete = (len(complete) == len(stage.tasks.all()))

        return is_stage_complete

    except LeadProgress.DoesNotExist:
        return None

def get_stage_stats(pipeline):
    #check the amount of leads and value at each pipeline stage
    stage_lead_counts = {}
    leads_progress = {}

    for stage in pipeline.stages.all():
        stage_lead_counts[stage.name] = {'name': stage.name, 'count': 0, 'value': 0}
    for lead in  pipeline.leads.all():
        for stage in pipeline.stages.all():
            complete = is_stage_complete(stage, lead)
            if complete == False:
                leads_progress[lead.name] = {'stage': stage, 'value': lead.value()}
                break
         
    for lead in pipeline.leads.all():
        try:
            stage_lead_counts[leads_progress[lead.name]['stage'].name]['count'] += 1
            stage_lead_counts[leads_progress[lead.name]['stage'].name]['value'] += leads_progress[lead.name]['value']
        except KeyError:
            continue
    temp = []
    for item in stage_lead_counts:
        temp.append(stage_lead_counts[item])
    stage_lead_counts = temp

    return stage_lead_counts

def default_lookups():
    units = ['Minute', 'Hour', 'Day', 'Week', 'Month', 'Year']
    statuses = ['Open', 'Lost', 'Won']
    sources = ['Web Signup', 'Referral', 'Conference', 'Meeting', 'Cold Call']

    try:
        value = Unit.objects.get(name='Minute')
    except Unit.DoesNotExist:
        for unit in units:
            Unit.objects.get_or_create(name=unit)
        
        for status in statuses:
            LeadStatus.objects.get_or_create(name=status)
        
        for source in sources:
            LeadSource.objects.get_or_create(name=source)