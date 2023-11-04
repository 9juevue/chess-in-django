import json

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from game.models import Field


class ChessConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.fields = {}
        self.field = None
        self.room_group_name = None
        self.game_id = None

    def connect(self):
        self.room_group_name = self.scope['url_route']['kwargs']['room_name']

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

        # self.send(text_data=json.dumps({
        #     'type': 'init_current_field',
        #     'field': self.field.get_field_text()
        # }))

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        if 'type' in text_data_json:
            if text_data_json['type'] == 'init_game':
                self.field = Field(text_data_json['id'])
                self.field.init_game(self.field)
                self.game_id = text_data_json['id']

            if text_data_json['type'] == 'figure_move':
                self.figure_move(text_data_json, self.field.players['white_player'], self.field.players['black_player'])

            if text_data_json['type'] == 'message':
                self.chat_message(text_data_json)

    def chat_message_event(self, event):
        message = event['message']

        self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message
        }))

    def chat_message(self, text_data_json):
        message = text_data_json['message']

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message_event',
                'message': message
            }
        )

    def figure_move_event(self, event):
        status = event['status']

        self.send(text_data=json.dumps({
            'type': 'figure_move',
            'game_id': self.game_id,
            'status': status,
            'coordinates_old': event['coordinates_old'],
            'coordinates_new': event['coordinates_new'],
            'figure_id': event['figure_id'],
            'original_position_left': event['original_position_left'],
            'original_position_top': event['original_position_top'],
        }))
        
    def figure_move(self, text_data_json, white_player, black_player):
        piece = (self.field.get_piece(text_data_json['coordinates_old'], self.field))
        status = None

        if piece is None:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'figure_none_event',
                    'status': False
                }
            )
        else:
            if piece.is_white():
                status = white_player.move_piece(piece,
                                                 {'x': str(text_data_json['coordinates_new'][0]),
                                                  'y': str(text_data_json['coordinates_new'][1])}, self.field)
            elif piece.is_black():
                status = black_player.move_piece(piece,
                                                 {'x': str(text_data_json['coordinates_new'][0]),
                                                  'y': str(text_data_json['coordinates_new'][1])}, self.field)

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'figure_move_event',
                    'status': status,
                    'coordinates_old': text_data_json['coordinates_old'],
                    'coordinates_new': text_data_json['coordinates_new'],
                    'figure_id': text_data_json['figure_id'],
                    'original_position_left': text_data_json['original_position_left'],
                    'original_position_top': text_data_json['original_position_top'],
                }
            )

    def figure_none_event(self, event):
        status = event['status']

        self.send(text_data=json.dumps({
            'type': 'figure_move',
            'status': status
        }))


