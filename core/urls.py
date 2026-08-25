from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("welcome/", views.welcome, name="welcome"),
    path("start/", views.start_family, name="start_family"),
    path("join/", views.join_family, name="join_family"),
    path("approve/<int:member_id>/", views.approve_member, name="approve_member"),
    path("logout/", views.logout_view, name="logout"),
]