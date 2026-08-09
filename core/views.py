from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .engine import analyse_goal
from django.contrib.auth import login
from .forms import TransactionForm, SignupForm
from .models import Household, Member, Transaction, Goal

@login_required
def dashboard(request):
    member = Member.objects.get(user=request.user)
    household = member.household

    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.household = household
            transaction.member = member
            transaction.save()
            return redirect("dashboard")
    else:
        form = TransactionForm()

    transactions = Transaction.objects.filter(household=household)

    income = sum(t.amount for t in transactions if t.tier == "income")
    essential = sum(t.amount for t in transactions if t.tier == "essential")
    committed = sum(t.amount for t in transactions if t.tier == "committed")
    discretionary = sum(t.amount for t in transactions if t.tier == "discretionary")
    surplus = income - essential - committed

    goal = Goal.objects.filter(household=household).first()
    analysis = None
    if goal:
        analysis = analyse_goal(
            income=float(income),
            essential=float(essential),
            committed=float(committed),
            discretionary=float(discretionary),
            target_amount=float(goal.target_amount),
            target_months=goal.target_months,
            saved_amount=float(goal.saved_amount),
        )

    context = {
        "household": household,
        "transactions": transactions,
        "income": income,
        "essential": essential,
        "committed": committed,
        "discretionary": discretionary,
        "surplus": surplus,
        "form": form,
        "goal": goal,
        "analysis": analysis,
    }
    return render(request, "core/dashboard.html", context)

def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            household = Household.objects.create(name=form.cleaned_data["household_name"])
            Member.objects.create(user=user, household=household, role="admin")
            login(request, user)
            return redirect("dashboard")
    else:
        form = SignupForm()
    return render(request, "core/signup.html", {"form": form})