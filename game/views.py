from django.shortcuts import render, HttpResponseRedirect

from django.http import JsonResponse

import uuid


def index(request):
    if request.method == 'POST':
        if 'type' in request.POST:
            if request.POST['type'] == 'create_room':
                unique_string = uuid.uuid4().hex[:6].upper()
                return JsonResponse({'status': True, 'unique_string': unique_string}, status=200)
    context = {

    }
    return render(request, 'game/index.html', context)


def game(request, unique_string):
    context = {
        'title': 'Игра',
    }
    return render(request, 'game/game.html', context)
