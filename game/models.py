from abc import abstractmethod

from django.db import models


# Create your models here.


# Класс игрового поля
class Field:
    # Необходим для индексации фигуры по иксам (A => 0, B => 1, ... , H => 7)
    _field_x = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    _moves_count = 0

    def __init__(self, game_id=None, *args, **kwargs):
        self.__game_id = game_id
        self._field = {
            'A8': None, 'B8': None, 'C8': None, 'D8': None, 'E8': None, 'F8': None, 'G8': None, 'H8': None,
            'A7': None, 'B7': None, 'C7': None, 'D7': None, 'E7': None, 'F7': None, 'G7': None, 'H7': None,
            'A6': None, 'B6': None, 'C6': None, 'D6': None, 'E6': None, 'F6': None, 'G6': None, 'H6': None,
            'A5': None, 'B5': None, 'C5': None, 'D5': None, 'E5': None, 'F5': None, 'G5': None, 'H5': None,
            'A4': None, 'B4': None, 'C4': None, 'D4': None, 'E4': None, 'F4': None, 'G4': None, 'H4': None,
            'A3': None, 'B3': None, 'C3': None, 'D3': None, 'E3': None, 'F3': None, 'G3': None, 'H3': None,
            'A2': None, 'B2': None, 'C2': None, 'D2': None, 'E2': None, 'F2': None, 'G2': None, 'H2': None,
            'A1': None, 'B1': None, 'C1': None, 'D1': None, 'E1': None, 'F1': None, 'G1': None, 'H1': None,
        }
        self.players = {}
        self._queue = 'White'

    @property
    def field(self):
        return self._field

    @property
    def queue(self):
        return self._queue

    @property
    def field_x(self):
        return self._field_x

    @property
    def game_id(self):
        return self.__game_id

    @property
    def moves_count(self):
        return self._moves_count

    @classmethod
    def new_move_piece(cls):
        cls._moves_count += 1

    @classmethod
    def _moves_count_none(cls):
        cls._moves_count = 0

    def get_game_id(self):
        return self.__game_id

    # Возвращает поле в читабельном виде для консоли
    def get_console_field(self):
        i = 0
        y = 8

        print('')
        print('Chess board id: ' + self.__game_id + '. Queue: ' + self._queue)
        for key in self._field:
            obj = self._field[key]

            if i % 8 == 0:
                print('')
                print("{:<3}".format(y), end='')

                y -= 1
            if obj is None:
                print('None     ', end=' ')
            else:
                print("{:<9}".format(obj.color[0] + obj.name), end=' ')
            i += 1

        print('')
        print('   ', end='')

        for i in range(0, len(self.field_x)):
            print("{:<9}".format(self.field_x[i]), end=' ')

        print('')
        print('')

    # Возвращает поле с фигурами
    def get_field_text(self):
        text_field = self.field.copy()
        for key in text_field:
            if text_field[key] is not None:
                if hasattr(text_field[key], 'name'):
                    text_field[key] = {
                        'name': text_field[key].name,
                        'color': text_field[key].color,
                        'start_coordinates': str(text_field[key].start_coordinates['x']) + str(
                            text_field[key].start_coordinates['y'])
                    }

        return text_field

    # Ставит фигуру на заданное положение в доске
    def _set_piece(self, piece, coordinates, chess_board: 'Field'):
        if self._check_coordinates(coordinates):
            chess_board._field[coordinates['x'] + coordinates['y']] = piece

    # Создает фигуру на доске в заданной позиции
    @staticmethod
    def _create_piece(piece, coordinates, chess_board: 'Field'):
        if chess_board._check_coordinates(coordinates):
            if chess_board._field[coordinates['x'] + coordinates['y']] is None:
                chess_board._field[coordinates['x'] + coordinates['y']] = piece
            else:
                raise Exception('Нельзя создать фигуру поверх другой')

    # Удаляет фигуру с позиции
    def _set_none(self, coordinates, chess_board: 'Field'):
        if self._check_coordinates(coordinates):
            chess_board._field[coordinates['x'] + coordinates['y']] = None

    # Проверяет, правильно ли введены координаты
    def _check_coordinates(self, coordinates):
        if 'x' in coordinates:
            if 'y' in coordinates:
                if coordinates['x'] + coordinates['y'] in self._field:
                    return True
                else:
                    print('Неверно введены координаты')
                    return False
        else:
            print('Неверно введены ключи координат')
            return False

    # Возвращает объект фигуры по координатам (в формате 'A2')
    @staticmethod
    def get_piece(coordinates, chess_board: 'Field'):
        return chess_board._field[coordinates]

    # Ставит противоположный цвет
    def set_negative_color(self):
        if self._queue == 'White':
            self._queue = 'Black'
        else:
            self._queue = 'White'

    # Создает фигуры и расставляет на начальные позиции
    def init_game(self, chess_board):
        white_pieces = {
            'white_pawn_1': Pawn({'x': 'A', 'y': '2'}, 'White', chess_board),
            'white_pawn_2': Pawn({'x': 'B', 'y': '2'}, 'White', chess_board),
            'white_pawn_3': Pawn({'x': 'C', 'y': '2'}, 'White', chess_board),
            'white_pawn_4': Pawn({'x': 'D', 'y': '2'}, 'White', chess_board),
            'white_pawn_5': Pawn({'x': 'E', 'y': '2'}, 'White', chess_board),
            'white_pawn_6': Pawn({'x': 'F', 'y': '2'}, 'White', chess_board),
            'white_pawn_7': Pawn({'x': 'G', 'y': '2'}, 'White', chess_board),
            'white_pawn_8': Pawn({'x': 'H', 'y': '2'}, 'White', chess_board),
            'white_rook_1': Rook({'x': 'A', 'y': '1'}, 'White', chess_board),
            'white_rook_2': Rook({'x': 'H', 'y': '1'}, 'White', chess_board),
            'white_knight_1': Knight({'x': 'B', 'y': '1'}, 'White', chess_board),
            'white_knight_2': Knight({'x': 'G', 'y': '1'}, 'White', chess_board),
            'white_bishop_1': Bishop({'x': 'C', 'y': '1'}, 'White', chess_board),
            'white_bishop_2': Bishop({'x': 'F', 'y': '1'}, 'White', chess_board),
            'white_queen_1': Queen({'x': 'D', 'y': '1'}, 'White', chess_board),
        }
        black_pieces = {
            'black_pawn_1': Pawn({'x': 'A', 'y': '7'}, 'Black', chess_board),
            'black_pawn_2': Pawn({'x': 'B', 'y': '7'}, 'Black', chess_board),
            'black_pawn_3': Pawn({'x': 'C', 'y': '7'}, 'Black', chess_board),
            'black_pawn_4': Pawn({'x': 'D', 'y': '7'}, 'Black', chess_board),
            'black_pawn_5': Pawn({'x': 'E', 'y': '7'}, 'Black', chess_board),
            'black_pawn_6': Pawn({'x': 'F', 'y': '7'}, 'Black', chess_board),
            'black_pawn_7': Pawn({'x': 'G', 'y': '7'}, 'Black', chess_board),
            'black_pawn_8': Pawn({'x': 'H', 'y': '7'}, 'Black', chess_board),
            'black_rook_1': Rook({'x': 'A', 'y': '8'}, 'Black', chess_board),
            'black_rook_2': Rook({'x': 'H', 'y': '8'}, 'Black', chess_board),
            'black_knight_1': Knight({'x': 'B', 'y': '8'}, 'Black', chess_board),
            'black_knight_2': Knight({'x': 'G', 'y': '8'}, 'Black', chess_board),
            'black_bishop_1': Bishop({'x': 'C', 'y': '8'}, 'Black', chess_board),
            'black_bishop_2': Bishop({'x': 'F', 'y': '8'}, 'Black', chess_board),
            'black_queen_1': Queen({'x': 'D', 'y': '8'}, 'Black', chess_board),
        }
        white_player = Player('White', white_pieces)
        black_player = Player('Black', black_pieces)
        self.players = {'white_player': white_player, 'black_player': black_player}


# Класс описывающий правила игры
class GameRules(Field):

    # Проверяет, занято ли поле фигурой
    @staticmethod
    def _is_field_occupied(coordinates, chess_board: 'Field'):
        key = coordinates['x'] + coordinates['y']

        if chess_board.field[key] is not None:
            return True

    # Проверяет, есть ли на вертикальном пути фигуры
    def _is_vertical_overstep(self, piece, coordinates, chess_board: 'Field'):
        index_current = self.field_x.index(piece.coordinates['x'])
        index_future = self.field_x.index(coordinates['x'])
        step_x = index_future - index_current
        step_y = int(coordinates['y']) - int(piece.coordinates['y'])

        if step_x == 0:
            if step_y > 0:
                for i in range(int(piece.coordinates['y']) + 1, int(coordinates['y'])):
                    if chess_board.field[coordinates['x'] + str(i)] is not None:
                        return True
            else:
                for i in range(int(piece.coordinates['y']) - 1, int(coordinates['y']), -1):
                    if chess_board.field[coordinates['x'] + str(i)] is not None:
                        return True
        else:
            if step_x > 0:
                for i in range(index_current + 1, index_future):
                    if chess_board.field[self.field_x[i] + piece.coordinates['y']] is not None:
                        return True
            else:
                for i in range(index_current - 1, index_future, -1):
                    if chess_board.field[self.field_x[i] + piece.coordinates['y']] is not None:
                        return True

    # Проверяет, есть ли на диагональном пути фигуры
    def _is_diagonal_overstep(self, piece, coordinates, chess_board: 'Field'):
        index = self.field_x.index(piece.coordinates['x'])
        step_y = self.field_x.index(coordinates['x']) - index
        if step_y > 0:
            if coordinates['y'] > piece.coordinates['y']:
                step = 1
                for i in range(int(piece.coordinates['y']), int(coordinates['y']) - 1):
                    if chess_board.field[self.field_x[index + step] + str(i + 1)] is not None:
                        return True
                    step += 1

            else:
                step = 1
                for i in range(int(piece.coordinates['y']), int(coordinates['y']) + 1, -1):
                    if chess_board.field[self.field_x[index + step] + str(i - 1)] is not None:
                        return True
                    step += 1
        else:
            if coordinates['y'] > piece.coordinates['y']:
                step = 1
                for i in range(int(piece.coordinates['y']), int(coordinates['y']) - 1):
                    if chess_board.field[self.field_x[index - step] + str(i + 1)] is not None:
                        return True
                    step += 1
            else:
                step = 1
                for i in range(int(piece.coordinates['y']), int(coordinates['y']) + 1, -1):
                    if chess_board.field[self.field_x[index - step] + str(i - 1)] is not None:
                        return True
                    step += 1

    # Взятие пешкой
    def _is_capture_by_pawn(self, pawn, coordinates, chess_board: 'Field'):
        def _is_capture():
            if self._is_field_occupied(coordinates, chess_board):
                piece_target = chess_board._field[coordinates['x'] + coordinates['y']]
                if pawn.color != piece_target.color:
                    if pawn.is_white():
                        if int(coordinates['y']) - int(pawn.coordinates['y']) == 1:
                            return True
                    elif pawn.is_black():
                        if int(pawn.coordinates['y']) - int(coordinates['y']) == 1:
                            return True
                return False

        index = pawn.field_x.index(pawn.coordinates['x'])

        if 0 < index < len(pawn.field_x) - 1:
            if coordinates['x'] == pawn.field_x[index - 1] or coordinates['x'] == pawn.field_x[index + 1]:
                if _is_capture():
                    return True
        elif index == 0:
            if coordinates['x'] == pawn.field_x[index + 1]:
                if _is_capture():
                    return True
        elif index == len(pawn.field_x) - 1:
            if coordinates['x'] == pawn.field_x[index - 1]:
                if _is_capture():
                    return True

    # # Взятие на проходе
    # def _is_en_passant(self, pawn, coordinates):
    #     if pawn.is_white():
    #         if pawn.coordinates['y'] == '5':
    #             pass
    #     elif pawn.is_black():
    #         if pawn.coordinates['y'] == '4':
    #             pass

    # Взятие фигурами кроме пешки
    @staticmethod
    def _is_capture(piece, coordinates, chess_board: 'Field'):
        piece_target = chess_board._field[coordinates['x'] + coordinates['y']]
        if piece.color != piece_target.color:
            return True
        else:
            return False


# Класс правил хода для фигур
class PieceRules:

    # Проверяет, может ли пешка сделать ход
    @staticmethod
    def _pawn_rules(pawn, coordinates):
        if pawn.name == 'Pawn':
            if pawn.coordinates != coordinates:
                if pawn.coordinates['x'] == coordinates['x']:
                    if pawn.moves_count == 0:
                        if pawn.is_white():
                            if 0 < int(coordinates['y']) - int(pawn.coordinates['y']) <= 2:
                                return True
                        elif pawn.is_black():
                            if 0 < int(pawn.coordinates['y']) - int(coordinates['y']) <= 2:
                                return True
                    else:
                        if pawn.is_white():
                            if 0 < int(coordinates['y']) - int(pawn.coordinates['y']) <= 1:
                                return True
                        elif pawn.is_black():
                            if 0 < int(pawn.coordinates['y']) - int(coordinates['y']) <= 1:
                                return True
        return False

    # Проверяет, может ли ладья сделать ход
    @staticmethod
    def _rook_rules(rook, coordinates):
        if rook.name == 'Rook' or 'Queen':
            if rook.coordinates != coordinates:
                if rook.coordinates['x'] == coordinates['x'] or rook.coordinates['y'] == coordinates['y']:
                    return True
        return False

    # Проверяет, может ли конь сделать ход
    @staticmethod
    def _knight_rules(knight, coordinates):
        if knight.name == 'Knight':
            if knight.coordinates != coordinates:
                index = knight.field_x.index(knight.coordinates['x'])

                if index + 1 <= len(knight.field_x) - 1:
                    if coordinates['x'] == knight.field_x[index + 1]:
                        if int(coordinates['y']) == int(knight.coordinates['y']) + 2 or int(coordinates['y']) == int(
                                knight.coordinates['y']) - 2:
                            return True

                if index + 2 <= len(knight.field_x) - 1:
                    if coordinates['x'] == knight.field_x[index + 2]:
                        if int(coordinates['y']) == int(knight.coordinates['y']) + 1 or int(coordinates['y']) == int(
                                knight.coordinates['y']) - 1:
                            return True

                if index - 1 >= 0:
                    if coordinates['x'] == knight.field_x[index - 1]:
                        if int(coordinates['y']) == int(knight.coordinates['y']) + 2 or int(coordinates['y']) == int(
                                knight.coordinates['y']) - 2:
                            return True

                if index - 2 >= 0:
                    if coordinates['x'] == knight.field_x[index - 2]:
                        if int(coordinates['y']) == int(knight.coordinates['y']) + 1 or int(coordinates['y']) == int(
                                knight.coordinates['y']) - 1:
                            return True
        return False

    # Проверяет, может ли слон сделать ход
    @staticmethod
    def _bishop_rules(bishop, coordinates):
        if bishop.name == 'Bishop' or 'Queen':
            if bishop.coordinates != coordinates:
                index = bishop.field_x.index(bishop.coordinates['x'])
                step_x = bishop.field_x.index(coordinates['x']) - bishop.field_x.index(bishop.coordinates['x'])
                step_y = int(coordinates['y']) - int(bishop.coordinates['y'])

                if abs(step_x) == abs(step_y):
                    if step_x > 0:
                        if coordinates['x'] == bishop.field_x[index + step_x]:
                            return True
                    elif step_x < 0:
                        if coordinates['x'] == bishop.field_x[index + step_x]:
                            return True
        return False

    # Проверяет, может ли королева сделать ход
    def _queen_rules(self, queen, coordinates):
        if queen.name == 'Queen':
            if self._rook_rules(queen, coordinates):
                return True
            if self._bishop_rules(queen, coordinates):
                return True


# Класс игрока
class Player:
    def __init__(self, color, pieces):
        if Piece.check_piece_color(color):
            self.__color = color
            self.__pieces = pieces
            # Чья очередь ходить
            self.__queue = 'White'

    # Двигает фигуру, выбранную игроком
    def move_piece(self, piece: 'Piece', coordinates, chess_board: 'Field'):
        if piece.color == self.__color:
            if self.__color == chess_board.queue:
                if piece.move(coordinates):
                    chess_board.set_negative_color()
                    print(chess_board.queue)

                    piece.new_move_piece()

                    chess_board.get_console_field()

                    return True
        return False

    @property
    def pieces(self):
        return self.__pieces


# Класс описывающий фигуру
class Piece(PieceRules, GameRules):
    # coordinates - координаты куда хочет сделать ход фигура
    # self._coordinates - текущие координаты фигуры

    _coordinates = {'x': None, 'y': None}

    def __init__(self, name, coordinates, color):
        super().__init__()
        if super()._check_coordinates(coordinates):
            if self.check_piece_color(color):
                self._name = name
                self._coordinates = coordinates
                self._color = color
                self._id = color + name + coordinates['x'] + coordinates['y']
                self._is_dead = False
                self._start_coordinates = {'x': coordinates['x'], 'y': coordinates['y']}
        else:
            raise Exception('Ошибка при создании фигуры')

    @property
    def name(self):
        return self._name

    @property
    def color(self):
        return self._color

    @property
    def id(self):
        return self._id

    @property
    def coordinates(self):
        return self._coordinates

    @property
    def start_coordinates(self):
        return self._start_coordinates

    def _delete_coordinates(self):
        if self._is_dead:
            self._coordinates = None

    # Ставит фигуру на заданную позицию
    def _set_position(self, piece, coordinates, chess_board: 'Field'):
        chess_board._set_none(self._coordinates, chess_board)
        chess_board._set_piece(piece, coordinates, chess_board)

        self._coordinates = coordinates
        self._id = self._color + self._name + coordinates['x'] + coordinates['y']

    @abstractmethod
    def move(self, coordinates):
        pass

    # Проверяет цвет фигуры
    @staticmethod
    def check_piece_color(color):
        if color == 'White':
            return True
        elif color == 'Black':
            return True
        else:
            print('Неверно введён цвет фигуры')
            return False

    # Если цвет фигуры черные возвращает истину
    def is_black(self):
        if self.color == 'Black':
            return True
        return False

    # Если цвет фигуры белый возвращает истину
    def is_white(self):
        if self.color == 'White':
            return True
        return False

    # "Убивает" фигуру
    @staticmethod
    def __kill_piece(piece: 'Piece'):
        piece._is_dead = True

    # Ест фигуру
    def _eat_piece(self, coordinates, chess_board: 'Field'):
        piece_target = chess_board._field[coordinates['x'] + coordinates['y']]
        self.__kill_piece(piece_target)
        self._set_position(self, coordinates, chess_board)

    def _revive_piece(self):
        self._is_dead = False


# Класс Пешки
class Pawn(Piece, Player):
    _name = 'Pawn'

    def __init__(self, coordinates, color, chess_board):
        super().__init__(self._name, coordinates, color)
        super()._create_piece(self, coordinates, chess_board)

        self.__moves_count = 0
        self._en_passant_move = None
        self.__chess_board = chess_board

    @property
    def moves_count(self):
        return self.__moves_count

    # Приравнивает количество ходов пешки к нулю
    def _init_pawn(self):
        self.__moves_count = 0

    # Ставит пешку на заданную позицию, с проверками
    def move(self, coordinates):
        if super()._check_coordinates(coordinates) and not self._is_dead:
            if super()._pawn_rules(self, coordinates):
                if not super()._is_field_occupied(coordinates, self.__chess_board):
                    if not super()._is_vertical_overstep(self, coordinates, self.__chess_board):
                        super()._set_position(self, coordinates, self.__chess_board)

                        if self.__moves_count == 0:
                            if coordinates['y'] == '4' or '6':
                                pass

                        self.__moves_count += 1
                        return True
            elif super()._is_capture_by_pawn(self, coordinates, self.__chess_board):
                super()._eat_piece(coordinates, self.__chess_board)

                self.__moves_count += 1
                return True


# Класс Ладьи
class Rook(Piece):
    _name = 'Rook'

    def __init__(self, coordinates, color, chess_board):
        super().__init__(self._name, coordinates, color)
        super()._create_piece(self, coordinates, chess_board)

        self.__chess_board = chess_board

    # Ставим ладью на заданную позицию, с проверками
    def move(self, coordinates):
        if super()._check_coordinates(coordinates) and not self._is_dead:
            if super()._rook_rules(self, coordinates):
                if not super()._is_field_occupied(coordinates, self.__chess_board):
                    if not super()._is_vertical_overstep(self, coordinates, self.__chess_board):
                        super()._set_position(self, coordinates, self.__chess_board)
                        return True
                else:
                    if not super()._is_vertical_overstep(self, coordinates, self.__chess_board):
                        if super()._is_capture(self, coordinates, self.__chess_board):
                            super()._eat_piece(coordinates, self.__chess_board)
                            return True


# Класс Коня
class Knight(Piece):
    _name = 'Knight'

    def __init__(self, coordinates, color, chess_board):
        super().__init__(self._name, coordinates, color)
        super()._create_piece(self, coordinates, chess_board)

        self.__chess_board = chess_board

    def move(self, coordinates):
        if super()._check_coordinates(coordinates) and not self._is_dead:
            if super()._knight_rules(self, coordinates):
                if not super()._is_field_occupied(coordinates, self.__chess_board):
                    super()._set_position(self, coordinates, self.__chess_board)
                    return True
                else:
                    if super()._is_capture(self, coordinates, self.__chess_board):
                        super()._eat_piece(coordinates, self.__chess_board)
                        return True


# Класс Слона
class Bishop(Piece):
    _name = 'Bishop'

    def __init__(self, coordinates, color, chess_board):
        super().__init__(self._name, coordinates, color)
        super()._create_piece(self, coordinates, chess_board)

        self.__chess_board = chess_board

    def move(self, coordinates):
        if super()._check_coordinates(coordinates) and not self._is_dead:
            if super()._bishop_rules(self, coordinates):
                if not super()._is_field_occupied(coordinates, self.__chess_board):
                    if not super()._is_diagonal_overstep(self, coordinates, self.__chess_board):
                        super()._set_position(self, coordinates, self.__chess_board)
                        return True
                else:
                    if not super()._is_diagonal_overstep(self, coordinates, self.__chess_board):
                        if super()._is_capture(self, coordinates, self.__chess_board):
                            super()._eat_piece(coordinates, self.__chess_board)
                            return True


# Класс Королевы
class Queen(Piece):
    _name = 'Queen'

    def __init__(self, coordinates, color, chess_board):
        super().__init__(self._name, coordinates, color)
        super()._create_piece(self, coordinates, chess_board)

        self.__chess_board = chess_board

    def move(self, coordinates):
        if super()._check_coordinates(coordinates) and not self._is_dead:
            if super()._queen_rules(self, coordinates):
                if not super()._is_field_occupied(coordinates, self.__chess_board):
                    if self.coordinates['x'] == coordinates['x'] or self.coordinates['y'] == coordinates['y']:
                        if not super()._is_vertical_overstep(self, coordinates, self.__chess_board):
                            super()._set_position(self, coordinates, self.__chess_board)
                            return True
                    elif not super()._is_diagonal_overstep(self, coordinates, self.__chess_board):
                        super()._set_position(self, coordinates, self.__chess_board)
                        return True
                else:
                    if self.coordinates['x'] == coordinates['x'] or self.coordinates['y'] == coordinates['y']:
                        if not super()._is_vertical_overstep(self, coordinates, self.__chess_board):
                            if super()._is_capture(self, coordinates, self.__chess_board):
                                super()._eat_piece(coordinates, self.__chess_board)
                                return True
                    elif not super()._is_diagonal_overstep(self, coordinates, self.__chess_board):
                        if super()._is_capture(self, coordinates, self.__chess_board):
                            super()._eat_piece(coordinates, self.__chess_board)
                            return True


# Класс Короля
class King(Piece):
    _name = 'King'

    def __init__(self, coordinates, color, chess_board):
        super().__init__(self._name, coordinates, color)
        super()._create_piece(self, coordinates, chess_board)

        self.chess_board = chess_board

    def move(self, coordinates):
        pass
