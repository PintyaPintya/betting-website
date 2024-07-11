from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("create-team/", views.create_team, name="create-team"),
    path("create-match/", views.create_match, name="create-match"),
    path("delete-match/<int:match_id>/", views.delete_match, name="delete-match"),
    path("delete-team/<int:team_id>/", views.delete_team, name="delete-team"),
    path("place-bet/<int:match_id>/", views.place_bet, name="place-bet"),
]