from django.urls import path

from game.views import index
from game.views import game

app_name = 'game'

urlpatterns = [
    path('', index, name='index'),
    path('<str:unique_string>/', game, name='game'),
]

