from django.urls import path
from . import views

app_name = "main"
urlpatterns = [
    path("", views.index, name="index"),
    path("register_conductor", views.register_conductor, name="register_conductor"),
    path("register_owner", views.register_owner, name="register_owner"),
    path("register_bus", views.register_bus, name="register_bus"),
    path("submit_record", views.submit_record, name="submit_record"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("list_records", views.list_records, name="list_records"),
    path("conductor_homepage", views.conductor_homepage, name="conductor_homepage"),
    path("owner_homepage", views.owner_homepage, name="owner_homepage"),
    path("conductor_records", views.conductor_records, name="conductor_records"),
    path("update_record", views.update_record, name="update_record"),
    path("daily_records", views.daily_records, name="daily_records"),
    path("monthly_records", views.monthly_records, name="monthly_records"),
]
