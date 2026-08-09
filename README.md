# FinFamily 🏠💰

**A multi-user household finance platform that doesn't just track money — it tells you whether your financial goals are actually reachable.**

Built for Hack Devengers 1.0 · An open-innovation submission.

---

## The Problem

Every personal finance app assumes one person managing one wallet. Real families don't work that way — multiple people earn, multiple people spend, and money is committed to obligations that span generations.

The consequence is measurable: RBI reporting places Indian household debt at ~41.3% of GDP (end-March 2025), above its five-year average, with consumption — not asset-building — driving most of the borrowing. This is a *visibility* problem as much as an income problem. When no single person can see the household aggregate, EMI stacking and lifestyle drift accumulate invisibly.

And critically: existing apps **track** goals but never **test** them. They show progress against a target they never checked was achievable — so a family discovers a shortfall in the final month instead of the first.

## What FinFamily Does Differently

Most apps answer *"are we on track for our goal?"*
FinFamily answers *"is this goal reachable at all — and if not, what are our options?"*

**1. Three-tier expense classification.** Every expense is tagged:
- **Essential** — structurally protected, never suggested for cuts (groceries, medicine, school fees)
- **Committed** — bound this month but reducible over time (EMIs, subscriptions)
- **Discretionary** — the only tier the engine ever proposes trimming

**2. The Goal Feasibility Engine (our core innovation).** It computes the household's *sustainable surplus*, applies a protection floor for emergencies, works out the monthly run-rate a goal requires, and delivers an honest verdict:
- ✅ **Reachable** — here's the monthly saving needed
- ⚠️ **Reachable with a trim** — cut this much discretionary spend
- ❌ **Not reachable** — here's the shortfall, and how long it would *actually* take

No commercial family finance app performs this feasibility test.

**3. Multi-user households.** Every family member has their own login and role (Administrator, Earner, Contributor, Dependant), all contributing to one shared household picture.

## Worked Example (live in the app)

A two-earner household: income ₹2,00,000, unavoidable spending ₹1,00,000 → sustainable surplus **₹1,00,000**. Goal: a ₹10,00,000 car in 12 months.

The engine reports: *needs ₹83,333/month, but the most safely saveable is ₹58,250 — a shortfall. At best effort, reachable in ~18 months, not 12.* **Told to the family in month one, not month eleven.**

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python · Django |
| Database | SQLite |
| Frontend | Django Templates · HTML · CSS |
| Auth | Django's built-in authentication |

The feasibility engine is written as a **pure, database-independent function** (`core/engine.py`) — making it correct, testable, and reusable.

## Running Locally

```bash
# clone and enter the project
git clone <your-repo-url>
cd finfamily

# create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

# install dependencies
pip install -r requirements.txt

# set up the database
python manage.py migrate
python manage.py createsuperuser

# run
python manage.py runserver
```

Then open **http://127.0.0.1:8000/** and log in.

## Scope & Honesty

**Built and working:** multi-user households, tiered transaction tracking, the goal feasibility engine, a login-protected dashboard.

**Designed but not yet built** (documented as future scope): automatic bank-statement import, ML-based transaction categorisation, and an interactive acceleration slider. We've deliberately scoped this to what genuinely works rather than overclaiming.

## Team

[Your names / roll numbers here]