from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass


class Team(models.Model):
    tag = models.CharField(max_length=4)
    name = models.CharField(max_length=24)


class Match(models.Model):
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team1")
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team2")

class Bet(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name="bets", default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bets")
    user_choice = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="user_bets")