from django.contrib import admin
from .models import Household, Member, Transaction, Goal

admin.site.register(Household)
admin.site.register(Member)
admin.site.register(Transaction)
admin.site.register(Goal)
