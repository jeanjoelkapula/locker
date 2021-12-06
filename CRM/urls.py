
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
    path("leads/page", views.leads_page, name="leads_page"),
    path('settings', views.settings, name="settings")
]