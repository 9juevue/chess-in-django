from django.shortcuts import render

from django.http import JsonResponse

import gc

from game.models import Pawn
from game.models import Rook
from game.models import Knight
from game.models import Bishop
from game.models import Queen
from game.models import Player


# Create your views here.
figures = {
    'white_pawn_1': Pawn({'x': 'A', 'y': '2'}, 'White'),
    'white_pawn_2': Pawn({'x': 'B', 'y': '2'}, 'White'),
    'white_pawn_3': Pawn({'x': 'C', 'y': '2'}, 'White'),
    'white_pawn_4': Pawn({'x': 'D', 'y': '2'}, 'White'),
    'white_pawn_5': Pawn({'x': 'E', 'y': '2'}, 'White'),
    'white_pawn_6': Pawn({'x': 'F', 'y': '2'}, 'White'),
    'white_pawn_7': Pawn({'x': 'G', 'y': '2'}, 'White'),
    'white_pawn_8': Pawn({'x': 'H', 'y': '2'}, 'White'),
    'white_rook_1': Rook({'x': 'A', 'y': '1'}, 'White'),
    'white_rook_2': Rook({'x': 'H', 'y': '1'}, 'White'),
    'white_knight_1': Knight({'x': 'B', 'y': '1'}, 'White'),
    'white_knight_2': Knight({'x': 'G', 'y': '1'}, 'White'),
    'white_bishop_1': Bishop({'x': 'C', 'y': '1'}, 'White'),
    'white_bishop_2': Bishop({'x': 'F', 'y': '1'}, 'White'),
    'white_queen_1': Queen({'x': 'D', 'y': '1'}, 'White'),
    'black_pawn_1': Pawn({'x': 'A', 'y': '7'}, 'Black'),
    'black_pawn_2': Pawn({'x': 'B', 'y': '7'}, 'Black'),
    'black_pawn_3': Pawn({'x': 'C', 'y': '7'}, 'Black'),
    'black_pawn_4': Pawn({'x': 'D', 'y': '7'}, 'Black'),
    'black_pawn_5': Pawn({'x': 'E', 'y': '7'}, 'Black'),
    'black_pawn_6': Pawn({'x': 'F', 'y': '7'}, 'Black'),
    'black_pawn_7': Pawn({'x': 'G', 'y': '7'}, 'Black'),
    'black_pawn_8': Pawn({'x': 'H', 'y': '7'}, 'Black'),
    'black_rook_1': Rook({'x': 'A', 'y': '8'}, 'Black'),
    'black_rook_2': Rook({'x': 'H', 'y': '8'}, 'Black'),
    'black_knight_1': Knight({'x': 'B', 'y': '8'}, 'Black'),
    'black_knight_2': Knight({'x': 'G', 'y': '8'}, 'Black'),
    'black_bishop_1': Bishop({'x': 'C', 'y': '8'}, 'Black'),
    'black_bishop_2': Bishop({'x': 'F', 'y': '8'}, 'Black'),
    'black_queen_1': Queen({'x': 'D', 'y': '8'}, 'Black'),
}

white_player = Player('White')
black_player = Player('Black')


def game(request):
    if request.method == 'POST':
        if 'reload' in request.POST:
            if request.POST['reload']:
                pass

        if 'coordinates_old' in request.POST:
            coordinates_old = request.POST['coordinates_old']
            coordinates_new = request.POST['coordinates_new']
            figure = (white_player._get_figure(coordinates_old))
            status = None

            if figure is None:
                return JsonResponse({'status': False}, status=200)

            if figure.is_white():
                status = white_player.move_figure(figure, {'x': str(coordinates_new[0]), 'y': str(coordinates_new[1])})
            elif figure.is_black():
                status = black_player.move_figure(figure, {'x': str(coordinates_new[0]), 'y': str(coordinates_new[1])})

            print(figure._get_console_field())

            data = {
                'status': status,
                'coordinates_old': coordinates_old,
                'coordinates_new': coordinates_new
            }

            return JsonResponse(data, status=200)

    context = {
        'title': 'Игра'
    }

    return render(request, 'game/game.html', context)
