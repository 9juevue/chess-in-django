from django.urls import path

from game.views import game

app_name = 'game'

urlpatterns = [
    path('chess', game, name='index'),
]
