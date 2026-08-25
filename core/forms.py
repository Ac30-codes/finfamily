from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Transaction, Member, RecurringRule, Goal

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["name", "amount", "tier"]


class StartFamilyForm(UserCreationForm):
    household_name = forms.CharField(max_length=100, label="Family / household name")

    class Meta:
        model = User
        fields = ["username", "household_name"]


class JoinFamilyForm(UserCreationForm):
    join_code = forms.CharField(max_length=6, label="Family code")
    requested_role = forms.ChoiceField(
        choices=[c for c in Member.ROLE_CHOICES if c[0] != "admin"],
        label="Your role in the family",
    )

    class Meta:
        model = User
        fields = ["username", "join_code", "requested_role"]

class RecurringRuleForm(forms.ModelForm):
    class Meta:
        model = RecurringRule
        fields = ["name", "amount", "tier", "day_of_month"]