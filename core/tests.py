import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from .models import Household, Member, Transaction


class TransactionDateTests(TestCase):
    def setUp(self):
        self.household = Household.objects.create(name="Test Family")
        self.user = User.objects.create_user(username="alice", password="pass12345")
        self.member = Member.objects.create(
            user=self.user, household=self.household,
            role="admin", requested_role="admin", status="approved",
        )

    def test_explicit_date_is_kept(self):
        backdated = datetime.date(2026, 1, 15)
        t = Transaction.objects.create(
            household=self.household, member=self.member,
            name="Groceries", amount=500, tier="essential",
            date=backdated,
        )
        t.refresh_from_db()
        self.assertEqual(t.date, backdated)

    def test_date_defaults_to_today_when_omitted(self):
        t = Transaction.objects.create(
            household=self.household, member=self.member,
            name="Salary", amount=50000, tier="income",
        )
        self.assertEqual(t.date, datetime.date.today())
