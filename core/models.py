from django.db import models
from django.contrib.auth.models import User
import random
import string


def generate_join_code():
    """Make a short, readable family code like 'SHARMA-7K2Q'."""
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=6))


class Household(models.Model):
    name = models.CharField(max_length=100)
    join_code = models.CharField(max_length=6, unique=True, default=generate_join_code)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.join_code})"


class Member(models.Model):
    ROLE_CHOICES = [
        ("admin", "Administrator"),
        ("earner", "Earner"),
        ("contributor", "Contributor"),
        ("dependant", "Dependant"),
    ]
    STATUS_CHOICES = [
        ("pending", "Pending approval"),
        ("approved", "Approved"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    household = models.ForeignKey(Household, on_delete=models.CASCADE, related_name="members")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="earner")
    requested_role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="earner")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()}) - {self.get_status_display()}"


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


class RecurringRule(models.Model):
    """A repeating income or expense, e.g. salary on the 7th, rent on the 10th."""
    TIER_CHOICES = Transaction.TIER_CHOICES
    household = models.ForeignKey(Household, on_delete=models.CASCADE, related_name="recurring_rules")
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="recurring_rules")
    name = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    tier = models.CharField(max_length=20, choices=TIER_CHOICES)
    day_of_month = models.IntegerField(help_text="Day (1-28) this repeats each month")
    active = models.BooleanField(default=True)
    last_run = models.DateField(null=True, blank=True, help_text="Last date this rule posted a transaction")

    def __str__(self):
        return f"{self.name} - {self.amount} on day {self.day_of_month}"


class Goal(models.Model):
    TERM_CHOICES = [
        ("short", "Short term"),
        ("medium", "Medium term"),
        ("long", "Long term"),
    ]
    household = models.ForeignKey(Household, on_delete=models.CASCADE, related_name="goals")
    owner = models.ForeignKey(
        Member, on_delete=models.CASCADE, related_name="goals",
        null=True, blank=True,
        help_text="Leave blank for a whole-family goal; set a member for a personal goal",
    )
    name = models.CharField(max_length=200)
    target_amount = models.DecimalField(max_digits=12, decimal_places=2)
    target_date = models.DateField(null=True, blank=True)
    target_months = models.IntegerField(default=12)
    term = models.CharField(max_length=20, choices=TERM_CHOICES, default="medium")
    saved_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        owner = self.owner.user.username if self.owner else "Family"
        return f"{self.name} ({owner})"