from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Member, Transaction, Goal
from .forms import TransactionForm
from .engine import analyse_goal

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