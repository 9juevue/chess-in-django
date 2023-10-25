import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from game.models import Pawn
from game.models import Rook
from game.models import Knight
from game.models import Bishop
from game.models import Queen
from game.models import Player

white_figures = {
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
}

black_figures = {
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

white_player = Player('White', white_figures)
black_player = Player('Black', black_figures)


class ChessConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        print('helllo')

    def connect(self):
        white_player._init_figures()
        black_player._init_figures()
        print(white_player._get_console_field())

        self.room_group_name = 'test'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if 'type' in text_data_json:
            if text_data_json['type'] == 'figure_move':
                coordinates_old = text_data_json['coordinates_old']
                coordinates_new = text_data_json['coordinates_new']
                figure = (white_player._get_figure(coordinates_old))
                status = None

                if figure is None:
                    async_to_sync(self.channel_layer.group_send)(
                        self.room_group_name,
                        {
                            'type': 'figure_none',
                            'status': False
                        }
                    )
                else:
                    if figure.is_white():
                        status = white_player.move_figure(figure,
                                                          {'x': str(coordinates_new[0]), 'y': str(coordinates_new[1])})
                    elif figure.is_black():
                        status = black_player.move_figure(figure,
                                                          {'x': str(coordinates_new[0]), 'y': str(coordinates_new[1])})

                    async_to_sync(self.channel_layer.group_send)(
                        self.room_group_name,
                        {
                            'type': 'figure_move',
                            'status': status,
                            'coordinates_old': coordinates_old,
                            'coordinates_new': coordinates_new,
                            'figure_id': text_data_json['figure_id'],
                            'original_position_left': text_data_json['original_position_left'],
                            'original_position_top': text_data_json['original_position_top'],
                        }
                    )

                    print(figure._get_console_field())

            if text_data_json['type'] == 'message':
                message = text_data_json['message']

                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': message
                    }
                )

    def chat_message(self, event):
        message = event['message']

        self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message
        }))

    def figure_none(self, event):
        status = event['status']

        self.send(text_data=json.dumps({
            'type': 'figure_move',
            'status': status
        }))

    def figure_move(self, event):
        status = event['status']

        self.send(text_data=json.dumps({
            'type': 'figure_move',
            'status': status,
            'coordinates_old': event['coordinates_old'],
            'coordinates_new': event['coordinates_new'],
            'figure_id': event['figure_id'],
            'original_position_left': event['original_position_left'],
            'original_position_top': event['original_position_top'],
        }))
