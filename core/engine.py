import math

# Guardrails from the proposal
DISCRETIONARY_FLOOR_RATIO = 0.5   # can't cut discretionary below half of current
PROTECTION_RATIO = 0.10           # keep 10% of income for emergency fund / long-term


def analyse_goal(income, essential, committed, discretionary, target_amount, target_months, saved_amount=0):
    """Pure function: given the household's numbers and a goal, decide if it's reachable."""

    surplus = income - essential - committed          # sustainable surplus (S)
    protection = round(income * PROTECTION_RATIO)      # protection floor
    disc_floor = round(discretionary * DISCRETIONARY_FLOOR_RATIO)  # can't cut past this

    remaining = target_amount - saved_amount
    if target_months <= 0:
        target_months = 1
    required = remaining / target_months               # run-rate needed to hit the date (R)

    # most we can put toward the goal = surplus, minus protection, minus the discretionary we must keep
    max_goal_allocation = surplus - protection - disc_floor
    # what we can save right now at current discretionary spending
    current_goal_allocation = surplus - protection - discretionary

    if current_goal_allocation < 0:
        current_goal_allocation = 0

    # months to reach the goal at the current pace
    if current_goal_allocation > 0:
        months_at_current = math.ceil(remaining / current_goal_allocation)
    else:
        months_at_current = None

    # verdict
    if required <= current_goal_allocation:
        verdict = "feasible"
    elif required <= max_goal_allocation:
        verdict = "feasible_with_cut"
    else:
        verdict = "infeasible"

    # if infeasible, how long WOULD it take at max effort?
    realistic_months = math.ceil(remaining / max_goal_allocation) if max_goal_allocation > 0 else None

    return {
        "surplus": surplus,
        "protection": protection,
        "required": round(required),
        "max_goal_allocation": max_goal_allocation,
        "current_goal_allocation": current_goal_allocation,
        "months_at_current": months_at_current,
        "verdict": verdict,
        "realistic_months": realistic_months,
        "shortfall": round(required - max_goal_allocation) if verdict == "infeasible" else 0,
    }