from django.shortcuts import render, HttpResponseRedirect

from django.http import JsonResponse

import gc


def game(request):
    context = {
        'title': 'Игра',
    }


    return render(request, 'game/game.html', context)
