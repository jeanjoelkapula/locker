
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("companies/list", views.company_list, name="company_list"),
    path("company/create", views.company_create, name="company_create"),
    path("people/list", views.people_list, name="people_list"),
    path("people/create", views.people_create, name="people_create"),
    path("leads/create", views.leads_create, name="leads_create"),
    path("leads/list", views.leads_list, name="leads_list"),
    path("leads/page/<int:lead_id>", views.lead_page, name="lead_page"),
    path('settings', views.settings, name="settings"),
    path('settings/account', views.settings_account, name="settings_account"),
    path('settings/customer', views.settings_customer, name="settings_customer"),
    path('settings/password', views.settings_password, name="settings_password"),
    path('pipeline/create', views.pipeline_create, name='pipeline_create'),
    path('pipeline/list', views.pipeline_list, name='pipeline_list'),
    path('pipeline/save', views.save_pipeline, name='pipeline_save'),
    path('pipeline/<int:pipeline_id>/edit', views.pipeline_edit, name='pipeline_edit'),
    path('products/create', views.products_create, name="products_create"),
    path('products/list', views.products_list, name="products_list"),
    path('lead/save', views.save_lead, name='lead_save'),
    path('lead/<int:lead_id>/advance', views.advance_to_stage, name="advance_stage"),
    path('task/<int:task_id>/complete', views.complete_task, name="complete_task"),
    path('lead/<int:lead_id>/status', views.update_lead_status, name="lead_status_update"),
    path('stage/<int:pipeline_id>/stats', views.stage_stats, name="stage_stats")
]