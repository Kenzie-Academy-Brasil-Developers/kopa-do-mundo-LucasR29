from django.urls import path
from .views import TeamView, TeamViewDetail

urlpatterns = [
    path("teams/", TeamView.as_view()),
    path("teams/<team_id>/", TeamViewDetail.as_view()),
]
