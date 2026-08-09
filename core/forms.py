from django import forms
from .models import Transaction
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["name", "amount", "tier"]


class SignupForm(UserCreationForm):
    household_name = forms.CharField(max_length=100, label="Household name")

    class Meta:
        model = User
        fields = ["username", "household_name"]