import json

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from game.models import Field

field = Field('1ds4gds7hj42')
field.init_game()


class ChessConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_group_name = None

    def connect(self):
        self.room_group_name = 'test'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

        self.send(text_data=json.dumps({
            'type': 'init_current_field',
            'field': field.get_field_text()
        }))

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        if 'type' in text_data_json:
            if text_data_json['type'] == 'init_game':
                pass

            if text_data_json['type'] == 'figure_move':
                self.figure_move(text_data_json, field.players['white_player'], field.players['black_player'])

            if text_data_json['type'] == 'message':
                self.chat_message(text_data_json)

    def chat_message_event(self, event):
        message = event['message']

        self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message
        }))

    def figure_none_event(self, event):
        status = event['status']

        self.send(text_data=json.dumps({
            'type': 'figure_move',
            'status': status
        }))

    def figure_move_event(self, event):
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

    def figure_move(self, text_data_json, white_player, black_player):
        figure = (field.get_figure(text_data_json['coordinates_old']))
        status = None

        if figure is None:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'figure_none_event',
                    'status': False
                }
            )
        else:
            if figure.is_white():
                status = white_player.move_figure(figure,
                                                  {'x': str(text_data_json['coordinates_new'][0]),
                                                   'y': str(text_data_json['coordinates_new'][1])})
            elif figure.is_black():
                status = black_player.move_figure(figure,
                                                  {'x': str(text_data_json['coordinates_new'][0]),
                                                   'y': str(text_data_json['coordinates_new'][1])})

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

    def chat_message(self, text_data_json):
        message = text_data_json['message']

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message_event',
                'message': message
            }
        )
