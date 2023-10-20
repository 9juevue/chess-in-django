from django.urls import path

from game.views import game

from game.models import Pawn
from game.models import Rook
from game.models import Knight
from game.models import Bishop
from game.models import Queen
from game.models import Player

app_name = 'game'

urlpatterns = [
    path('chess', game, name='index'),
]
