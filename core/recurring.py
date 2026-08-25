from datetime import date
from .models import RecurringRule, Transaction


def process_recurring(household):
    """
    Check every active recurring rule for this household and post any
    transactions that have come due since the rule last ran.
    Called whenever a member opens the dashboard.
    """
    today = date.today()

    for rule in RecurringRule.objects.filter(household=household, active=True):
        # The date this rule should post in the current month.
        # Clamp the day to a safe 1-28 so short months never break it.
        day = min(rule.day_of_month, 28)
        due_this_month = date(today.year, today.month, day)

        # Has this month's occurrence already happened (date reached)?
        if today < due_this_month:
            continue  # not due yet this month

        # Has it already been posted for this occurrence?
        if rule.last_run and rule.last_run >= due_this_month:
            continue  # already posted this month

        # Post the transaction.
        Transaction.objects.create(
            household=household,
            member=rule.member,
            name=rule.name,
            amount=rule.amount,
            tier=rule.tier,
        )
        rule.last_run = today
        rule.save()