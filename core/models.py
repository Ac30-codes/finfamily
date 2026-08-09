from django.db import models
from django.contrib.auth.models import User


class Household(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Member(models.Model):
    ROLE_CHOICES = [
        ("admin", "Administrator"),
        ("earner", "Earner"),
        ("contributor", "Contributor"),
        ("dependant", "Dependant"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    household = models.ForeignKey(Household, on_delete=models.CASCADE, related_name="members")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="earner")

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"


class Transaction(models.Model):
    TIER_CHOICES = [
        ("income", "Income"),
        ("essential", "Essential"),
        ("committed", "Committed"),
        ("discretionary", "Discretionary"),
    ]
    household = models.ForeignKey(Household, on_delete=models.CASCADE, related_name="transactions")
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="transactions")
    name = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    tier = models.CharField(max_length=20, choices=TIER_CHOICES)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.amount}"


class Goal(models.Model):
    household = models.ForeignKey(Household, on_delete=models.CASCADE, related_name="goals")
    name = models.CharField(max_length=200)
    target_amount = models.DecimalField(max_digits=12, decimal_places=2)
    target_months = models.IntegerField()
    saved_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return self.name