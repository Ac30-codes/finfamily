from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.shortcuts import get_object_or_404
from .models import Member, Transaction, Goal, Household, RecurringRule
from .forms import TransactionForm, StartFamilyForm, JoinFamilyForm
from .engine import analyse_goal
from django.contrib.auth import login, logout
from .recurring import process_recurring
from .forms import RecurringRuleForm


def welcome(request):
    """Landing page: start a new family or join one."""
    return render(request, "core/welcome.html")


def start_family(request):
    if request.method == "POST":
        form = StartFamilyForm(request.POST)
        if form.is_valid():
            user = form.save()
            household = Household.objects.create(name=form.cleaned_data["household_name"])
            Member.objects.create(
                user=user, household=household,
                role="admin", requested_role="admin", status="approved",
            )
            login(request, user)
            return redirect("dashboard")
    else:
        form = StartFamilyForm()
    return render(request, "core/start_family.html", {"form": form})

def join_family(request):
    if request.method == "POST":
        form = JoinFamilyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data["join_code"].strip().upper()
            household = Household.objects.filter(join_code=code).first()
            if not household:
                form.add_error("join_code", "No family found with that code.")
            else:
                user = form.save()
                Member.objects.create(
                    user=user, household=household,
                    role=form.cleaned_data["requested_role"],
                    requested_role=form.cleaned_data["requested_role"],
                    status="pending",
                )
                login(request, user)
                return redirect("dashboard")
    else:
        form = JoinFamilyForm()
    return render(request, "core/join_family.html", {"form": form})


@login_required
def dashboard(request):
    member = Member.objects.get(user=request.user)

    # Approval gate: pending members can't see the dashboard yet.
    if member.status == "pending":
        return render(request, "core/pending.html", {"member": member})

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
            income=float(income), essential=float(essential),
            committed=float(committed), discretionary=float(discretionary),
            target_amount=float(goal.target_amount),
            target_months=goal.target_months,
            saved_amount=float(goal.saved_amount),
        )

    pending_members = Member.objects.filter(household=household, status="pending")

    context = {
        "member": member, "household": household, "transactions": transactions,
        "income": income, "essential": essential, "committed": committed,
        "discretionary": discretionary, "surplus": surplus,
        "form": form, "goal": goal, "analysis": analysis,
        "pending_members": pending_members if member.role == "admin" else None,
    }
    return render(request, "core/dashboard.html", context)


@login_required
def approve_member(request, member_id):
    """Admin approves a pending member."""
    admin_member = Member.objects.get(user=request.user)
    if admin_member.role != "admin":
        return redirect("dashboard")
    target = get_object_or_404(Member, id=member_id, household=admin_member.household)
    target.status = "approved"
    target.save()
    return redirect("dashboard")

def logout_view(request):
    logout(request)
    return redirect("welcome")

@login_required
def recurring(request):
    member = Member.objects.get(user=request.user)
    if member.status == "pending":
        return render(request, "core/pending.html", {"member": member})
    household = member.household

    process_recurring(household)

    if request.method == "POST":
        if "delete" in request.POST:
            RecurringRule.objects.filter(
                id=request.POST["delete"], household=household
            ).delete()
            return redirect("recurring")
        form = RecurringRuleForm(request.POST)
        if form.is_valid():
            rule = form.save(commit=False)
            rule.household = household
            rule.member = member
            rule.save()
            return redirect("recurring")
    else:
        form = RecurringRuleForm()

    rules = RecurringRule.objects.filter(household=household)
    return render(request, "core/recurring.html", {
        "member": member, "household": household,
        "form": form, "rules": rules,
    })