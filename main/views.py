from django.shortcuts import render, redirect, get_object_or_404
from .forms import (
    CustomUserCreationForm,
    BusRegisterForm,
    RecordForm,
    CustomUserAuthenticationForm,
)
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login as dj_login
from django.contrib.auth import logout as dj_logout
from django.contrib.auth.decorators import login_required
from .decorator import user_role_required
import datetime
from .models import Record, CustomUser
import json


def index(request):
    if request.user.is_anonymous:
        return redirect("main:login")

    elif request.user.is_authenticated and request.user.usertype == "conductor":
        return redirect("main:submit_record")

    elif request.user.is_authenticated and request.user.usertype == "owner":
        return redirect("main:owner_homepage")
    else:
        return HttpResponse("Some error occured")


# Create your views here.
@user_role_required("owner", "admin")
def register_conductor(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            conductor = form.save()
            conductor.usertype = "conductor"
            conductor.save()
            return render(
                request,
                "conductor_created.html",
                {
                    "username": request.POST["username"],
                    "password": request.POST["password1"],
                },
            )
    form = CustomUserCreationForm()
    return render(request, "register_conductor.html", {"form": form})


@user_role_required("admin")
def register_owner(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            owner = form.save()
            owner.usertype = "owner"
            owner.save()

            return HttpResponse(
                f"Owner created.<br>Username: {request.POST['username']}<br>Password:{request.POST['password1']}"
            )
    form = CustomUserCreationForm()
    return render(request, "register_owner.html", {"form": form})


def login(request):
    if request.method == "POST":
        form = CustomUserAuthenticationForm(data=request.POST)
        if form.is_valid():
            dj_login(request, form.get_user())
            if form.get_user().usertype == "conductor":
                return redirect("main:submit_record")
            elif form.get_user().usertype == "owner":
                return redirect("main:daily_records")
            return HttpResponse("logged in")

    form = CustomUserAuthenticationForm()
    return render(request, "login.html", {"form": form})


@user_role_required("owner")
def register_bus(request):
    if request.method == "POST":
        form = BusRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Bus created")

    form = BusRegisterForm()
    return render(request, "register_bus.html", {"form": form})


@user_role_required("conductor")
def submit_record(request):
    if request.method == "POST":
        form = RecordForm(request.POST)
        if form.is_valid():
            record = form.save()
            record.recorder = request.user
            record.bus = request.user.bus
            curr_dt = datetime.datetime.now()
            record.date = curr_dt.date()
            record.time = curr_dt.time()
            record.save()
            return render(request, "record_submitted.html")

    form = RecordForm()
    return render(request, "submit_record.html", {"form": form})


def logout(request):
    dj_logout(request)
    return HttpResponse("Logged out")


@user_role_required("")
def list_records(request):
    records = list(Record.objects.all().values("recorder", "income", "expense"))
    for record in records:
        if record["recorder"]:
            record["recorder"] = str(CustomUser.objects.get(id=record["recorder"]))
    return JsonResponse(records, safe=False)


@user_role_required("conductor")
def conductor_homepage(request):
    return redirect("main:submit_record")


@user_role_required("owner")
def owner_homepage(request):
    return redirect("main:daily_records")


@user_role_required("conductor")
def get_conductor_records(request):
    conductor = request.user
    records = conductor.record_set.order_by("-date", "-time")[:30]
    responses = list(records.values("id", "income", "expense", "date"))

    for response in responses:
        response["modify_access"] = datetime.date.today() - response[
            "date"
        ] == datetime.timedelta(0)

    return responses


@user_role_required("conductor")
def conductor_records(request):
    records = get_conductor_records(request)
    return render(request, "history.html", {"records": records})


@user_role_required("conductor")
def update_record(request):
    if request.method == "POST":
        data = json.loads(request.body)
        income = float(data["income"])
        expense = float(data["expense"])
        id = int(data["id"])
        record = get_object_or_404(Record, id=id)
        record.income = income
        record.expense = expense
        record.save()
        return JsonResponse({"success": True})


@user_role_required("owner")
def daily_records(request):
    records = Record.objects.order_by("date").values("date", "income", "expense")
    for record in records:
        record["income"] = int(record["income"])
        record["expense"] = int(record["expense"])
        record["profit"] = f'{(record["income"] - record["expense"])}'
        record["date"] = record["date"].strftime("%d-%m-%Y")

    return render(request, "daily_records.html", {"records": records})


from django.db.models import Sum
from django.db.models.functions import ExtractMonth, ExtractYear, Round
import calendar


@user_role_required("owner")
def monthly_records(request):
    records = (
        Record.objects.annotate(year=ExtractYear("date"), month=ExtractMonth("date"))
        .values("year", "month")
        .annotate(
            total_income=Round(Sum("income"), 1),
            total_expense=Round(Sum("expense"), 1),
            total_profit=Round(Sum("income") - Sum("expense"), 1),
        )
        .order_by("-year", "-month")
    )

    for record in records:
        record["month"] = calendar.month_abbr[record["month"]]

    return render(request, "monthly_records.html", {"records": records})
