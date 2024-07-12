from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import User, Team, Bet, Match

# Create your views here.


def index(request):
    teams = Team.objects.all()
    users = User.objects.all()
    matches = Match.objects.all()
    return render(
        request,
        "betlord/index.html",
        {"teams": teams, "users": users, "matches": matches},
    )


def create_team(request):

    if request.user.is_superuser and request.method == "GET":
        return render(request, "betlord/createTeam.html")

    elif request.user.is_superuser and request.method == "POST":
        name = request.POST["name"]
        tag = request.POST["tag"].upper()

        try:
            team = Team.objects.create(name=name, tag=tag)
            team.save()
        except IntegrityError:
            return render(
                request, "betlord/createTeam.html", {"message": "Team already exists"}
            )

        return HttpResponseRedirect(reverse("index"))

    else:
        return HttpResponseRedirect(reverse("index"))


def create_match(request):
    teams = Team.objects.all()

    if request.user.is_superuser and request.method == "GET":
        return render(request, "betlord/createMatch.html", {"teams": teams})

    elif request.user.is_superuser and request.method == "POST":
        team1_name = request.POST.get("team1")
        team2_name = request.POST.get("team2")

        team1 = Team.objects.filter(name=team1_name).first()
        team2 = Team.objects.filter(name=team2_name).first()

        if team1 == team2:
            return render(
                request,
                "betlord/createMatch.html",
                {"teams": teams, "message": "Both teams cannot be the same"},
            )

        if team1.name > team2.name:
            team1, team2 = team2, team1

        matches = Match.objects.all()
        for match in matches:
            if team1 == match.team1 and team2 == match.team2:
                return render(
                request,
                "betlord/createMatch.html",
                {"teams": teams, "message": "Match already exists"},
            )

        try:
            Match.objects.create(team1=team1, team2=team2)
        except IntegrityError:
            return render(
                request,
                "betlord/createMatch.html",
                {"teams": teams, "message": "Match already exists"},
            )

        return HttpResponseRedirect(reverse("index"))

    else:
        return HttpResponseRedirect(reverse("index"))


def delete_match(request, match_id):
    if request.user.is_superuser:
        match = get_object_or_404(Match, id=match_id)
        match.delete()
        return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponseRedirect(reverse("index"))
    

def delete_team(request, team_id):
    if request.user.is_superuser:
        team = get_object_or_404(Team, id=team_id)
        team.delete()
        return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponseRedirect(reverse("index"))


def place_bet(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    team1_name = match.team1.name.lower().replace(" ","-")
    team2_name = match.team2.name.lower().replace(" ","-")
    if request.method == "GET" and request.user.is_authenticated and not request.user.is_superuser:       
        return render(request, "betlord/placeBet.html", {
            "match": match,
            "team1_name": team1_name,
            "team2_name": team2_name,
        })
    elif request.method == "POST" and request.user.is_authenticated and not request.user.is_superuser:
        user = request.user
        user_choice = get_object_or_404(Team, id=request.POST.get('user_choice'))

        bets = Bet.objects.all()
        for bet in bets:
            if bet.user == user and bet.match == match:
                matches = Match.objects.all()
                return render(
                    request,
                    "betlord/index.html",
                    {"matches": matches ,"message": "Bet already placed"},
                )

        try:
            Bet.objects.create(match=match, user=user, user_choice=user_choice)
        except IntegrityError:
            return render(request, "betlord/placeBet.html", {
                    "match": match,
                    "team1_name": team1_name,
                    "team2_name": team2_name,
                })
        
        return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(
                request, "betlord/register.html", {"message": "Passwords must match"}
            )

        try:
            user = User.objects.create_user(
                username=username, email=email, password=password
            )
            user.save()
        except IntegrityError:
            return render(
                request, "betlord/register.html", {"message": "Username already taken"}
            )

        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "betlord/register.html")


def login_view(request):
    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "betlord/login.html",
                {"message": "Invalid username and/or password"},
            )

    else:
        return render(request, "betlord/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))
