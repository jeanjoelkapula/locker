from django import template
from ..models import PipelineStage, LeadProgress

register = template.Library()


@register.filter
def is_stage_complete(stage, lead):
    try:
        progress = LeadProgress.objects.get(lead=lead)
        complete = progress.task_lines.filter(task__pipeline_stage=stage).filter(is_complete=True)
        is_stage_complete = (len(complete) == len(stage.tasks.all()))

        return is_stage_complete

    except LeadProgress.DoesNotExist:
        return None

@register.filter
def is_task_complete(task, lead):
    try:
        progress = LeadProgress.objects.get(lead=lead)
        task_line = progress.task_lines.get(task=task)

        return task_line.is_complete
    except LeadProgress.DoesNotExist:
        return None