from abc import abstractmethod

from django.db import models


# Create your models here.


# Класс игрового поля
class Field:
    # Шахматное поле
    _field = {
        'A8': None, 'B8': None, 'C8': None, 'D8': None, 'E8': None, 'F8': None, 'G8': None, 'H8': None,
        'A7': None, 'B7': None, 'C7': None, 'D7': None, 'E7': None, 'F7': None, 'G7': None, 'H7': None,
        'A6': None, 'B6': None, 'C6': None, 'D6': None, 'E6': None, 'F6': None, 'G6': None, 'H6': None,
        'A5': None, 'B5': None, 'C5': None, 'D5': None, 'E5': None, 'F5': None, 'G5': None, 'H5': None,
        'A4': None, 'B4': None, 'C4': None, 'D4': None, 'E4': None, 'F4': None, 'G4': None, 'H4': None,
        'A3': None, 'B3': None, 'C3': None, 'D3': None, 'E3': None, 'F3': None, 'G3': None, 'H3': None,
        'A2': None, 'B2': None, 'C2': None, 'D2': None, 'E2': None, 'F2': None, 'G2': None, 'H2': None,
        'A1': None, 'B1': None, 'C1': None, 'D1': None, 'E1': None, 'F1': None, 'G1': None, 'H1': None,
    }

    # Необходим для индексации фигуры по иксам (A => 0, B => 1, ... , H => 7)
    _field_x = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

    @property
    def field(self):
        return self._field

    @property
    def field_x(self):
        return self._field_x

    # Возвращает поле в читабельном виде для консоли
    def _get_console_field(self):
        i = 0
        y = 8

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

    # Ставит фигуру на заданное положение в доске
    def _set_figure(self, figure, coordinates):
        if self._check_coordinates(coordinates):
            self._field[coordinates['x'] + coordinates['y']] = figure

    # Создает фигуру на доске в заданной позиции
    def _create_figure(self, figure, coordinates):
        if self._check_coordinates(coordinates):
            if self._field[coordinates['x'] + coordinates['y']] is None:
                self._field[coordinates['x'] + coordinates['y']] = figure
            else:
                raise Exception('Нельзя создать фигуру поверх другой')

    # Удаляет фигуру с позиции
    def _set_none(self, coordinates):
        if self._check_coordinates(coordinates):
            self._field[coordinates['x'] + coordinates['y']] = None

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
    def _get_figure(self, coordinates):
        return self._field[coordinates]


# Класс описывающий правила игры
class GameRules(Field):

    # Проверяет, занято ли поле фигурой
    def _is_field_occupied(self, coordinates):
        key = coordinates['x'] + coordinates['y']

        if self.field[key] is not None:
            return True

    # Проверяет, есть ли на вертикальном пути фигуры
    def _is_vertical_overstep(self, figure, coordinates):
        index_current = self.field_x.index(figure.coordinates['x'])
        index_future = self.field_x.index(coordinates['x'])
        step_x = index_future - index_current
        step_y = int(coordinates['y']) - int(figure.coordinates['y'])

        if step_x == 0:
            if step_y > 0:
                for i in range(int(figure.coordinates['y']) + 1, int(coordinates['y'])):
                    if self.field[coordinates['x'] + str(i)] is not None:
                        return True
            else:
                for i in range(int(figure.coordinates['y']) - 1, int(coordinates['y']), -1):
                    if self.field[coordinates['x'] + str(i)] is not None:
                        return True
        else:
            if step_x > 0:
                for i in range(index_current + 1, index_future):
                    if self.field[self.field_x[i] + figure.coordinates['y']] is not None:
                        return True
            else:
                for i in range(index_current - 1, index_future, -1):
                    if self.field[self.field_x[i] + figure.coordinates['y']] is not None:
                        return True

    # Проверяет, есть ли на диагональном пути фигуры
    def _is_diagonal_overstep(self, figure, coordinates):
        index = self.field_x.index(figure.coordinates['x'])
        step_y = self.field_x.index(coordinates['x']) - index
        if step_y > 0:
            if coordinates['y'] > figure.coordinates['y']:
                step = 1
                for i in range(int(figure.coordinates['y']), int(coordinates['y']) - 1):
                    if self.field[self.field_x[index + step] + str(i + 1)] is not None:
                        return True
                    step += 1

            else:
                step = 1
                for i in range(int(figure.coordinates['y']), int(coordinates['y']) + 1, -1):
                    if self.field[self.field_x[index + step] + str(i - 1)] is not None:
                        return True
                    step += 1
        else:
            if coordinates['y'] > figure.coordinates['y']:
                step = 1
                for i in range(int(figure.coordinates['y']), int(coordinates['y']) - 1):
                    if self.field[self.field_x[index - step] + str(i + 1)] is not None:
                        return True
                    step += 1
            else:
                step = 1
                for i in range(int(figure.coordinates['y']), int(coordinates['y']) + 1, -1):
                    if self.field[self.field_x[index - step] + str(i - 1)] is not None:
                        return True
                    step += 1

    # Взятие пешкой
    def _is_capture_by_pawn(self, pawn, coordinates):
        def _is_capture():
            if self._is_field_occupied(coordinates):
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
    def _is_capture(self, figure, coordinates):
        figure_target = super()._field[coordinates['x'] + coordinates['y']]
        if figure.color != figure_target.color:
            return True
        else:
            return False


# Класс правил хода для фигур
class FigureRules:

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


# Класс описывающий фигуру
class Figure(FigureRules, GameRules):
    # coordinates - координаты куда хочет сделать ход фигура
    # self._coordinates - текущие координаты фигуры

    _coordinates = {'x': None, 'y': None}

    def __init__(self, name, coordinates, color):
        if super()._check_coordinates(coordinates):
            if self.check_figure_color(color):
                self._name = name
                self._coordinates = coordinates
                self._color = color
                self._id = color + name + coordinates['x'] + coordinates['y']
                self._is_dead = False
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

    def _delete_coordinates(self):
        if self._is_dead:
            self._coordinates = None

    # Ставит фигуру на заданную позицию
    def _set_position(self, coordinates, figure):
        super()._set_none(self._coordinates)
        super()._set_figure(figure, coordinates)

        self._coordinates = coordinates
        self._id = self._color + self._name + coordinates['x'] + coordinates['y']

    @abstractmethod
    def move(self, coordinates):
        pass

    # Проверяет цвет фигуры
    @staticmethod
    def check_figure_color(color):
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
    def __kill_figure(figure: 'Figure'):
        figure._is_dead = True
        figure._delete_coordinates()

    # Ест фигуру
    def _eat_figure(self, coordinates):
        figure_target = super()._field[coordinates['x'] + coordinates['y']]
        self.__kill_figure(figure_target)
        self._set_position(coordinates, self)


# Класс игрока
class Player(Field):
    # Чья очередь ходить
    __queue = 'White'
    __moves_count = 0

    @property
    def moves_count(self):
        return self.__moves_count

    def __init__(self, color):
        if Figure.check_figure_color(color):
            self.__color = color

    # Двигает фигуру, выбранную игроком
    def move_figure(self, figure: 'Figure', coordinates):
        if figure.color == self.__color:
            if self.__color == self.__queue:
                if figure.move(coordinates):
                    self.__set_negative_color()

                    self.__new_move_figure()
                    return True
        return False

    # Ставит противоположный цвет
    @classmethod
    def __set_negative_color(cls):
        if cls.__queue == 'White':
            cls.__queue = 'Black'
        else:
            cls.__queue = 'White'

    @classmethod
    def __new_move_figure(cls):
        cls.__moves_count += 1


# Класс Пешки
class Pawn(Figure, Player):
    _name = 'Pawn'

    def __init__(self, coordinates, color):
        super().__init__(self._name, coordinates, color)
        super()._create_figure(self, coordinates)

        self.__moves_count = 0
        self._en_passant_move = None

    @property
    def moves_count(self):
        return self.__moves_count

    # Ставит пешку на заданную позицию, с проверками
    def move(self, coordinates):
        if super()._check_coordinates(coordinates) and not self._is_dead:
            if super()._pawn_rules(self, coordinates):
                if not super()._is_field_occupied(coordinates):
                    if not super()._is_vertical_overstep(figure=self, coordinates=coordinates):
                        super()._set_position(coordinates, self)

                        if self.__moves_count == 0:
                            if coordinates['y'] == '4' or '6':
                                self._en_passant_move = super().moves_count + 1

                        self.__moves_count += 1
                        return True
            elif super()._is_capture_by_pawn(self, coordinates):
                super()._eat_figure(coordinates)

                self.__moves_count += 1
                return True


# Класс Ладьи
class Rook(Figure):
    _name = 'Rook'

    def __init__(self, coordinates, color):
        super().__init__(self._name, coordinates, color)
        super()._create_figure(self, coordinates)

    # Ставим ладью на заданную позицию, с проверками
    def move(self, coordinates):
        if super()._check_coordinates(coordinates) and not self._is_dead:
            if super()._rook_rules(self, coordinates):
                if not super()._is_field_occupied(coordinates):
                    if not super()._is_vertical_overstep(figure=self, coordinates=coordinates):
                        super()._set_position(coordinates, self)
                        return True
                else:
                    if not super()._is_vertical_overstep(figure=self, coordinates=coordinates):
                        if super()._is_capture(self, coordinates):
                            super()._eat_figure(coordinates)
                            return True


# Класс Коня
class Knight(Figure):
    _name = 'Knight'

    def __init__(self, coordinates, color):
        super().__init__(self._name, coordinates, color)
        super()._create_figure(self, coordinates)

    def move(self, coordinates):
        if super()._check_coordinates(coordinates) and not self._is_dead:
            if super()._knight_rules(self, coordinates):
                if not super()._is_field_occupied(coordinates):
                    super()._set_position(coordinates, self)
                    return True
                else:
                    if super()._is_capture(self, coordinates):
                        super()._eat_figure(coordinates)
                        return True


# Класс Слона
class Bishop(Figure):
    _name = 'Bishop'

    def __init__(self, coordinates, color):
        super().__init__(self._name, coordinates, color)
        super()._create_figure(self, coordinates)

    def move(self, coordinates):
        if super()._check_coordinates(coordinates) and not self._is_dead:
            if super()._bishop_rules(self, coordinates):
                if not super()._is_field_occupied(coordinates):
                    if not super()._is_diagonal_overstep(figure=self, coordinates=coordinates):
                        super()._set_position(coordinates, self)
                        return True
                else:
                    if not super()._is_diagonal_overstep(figure=self, coordinates=coordinates):
                        if super()._is_capture(self, coordinates):
                            super()._eat_figure(coordinates)
                            return True


# Класс Королевы
class Queen(Figure):
    _name = 'Queen'

    def __init__(self, coordinates, color):
        super().__init__(self._name, coordinates, color)
        super()._create_figure(self, coordinates)

    def move(self, coordinates):
        if super()._check_coordinates(coordinates) and not self._is_dead:
            if super()._queen_rules(self, coordinates):
                if not super()._is_field_occupied(coordinates):
                    if self.coordinates['x'] == coordinates['x'] or self.coordinates['y'] == coordinates['y']:
                        if not super()._is_vertical_overstep(figure=self, coordinates=coordinates):
                            super()._set_position(coordinates, self)
                            return True
                    elif not super()._is_diagonal_overstep(figure=self, coordinates=coordinates):
                        super()._set_position(coordinates, self)
                        return True
                else:
                    if self.coordinates['x'] == coordinates['x'] or self.coordinates['y'] == coordinates['y']:
                        if not super()._is_vertical_overstep(figure=self, coordinates=coordinates):
                            if super()._is_capture(self, coordinates):
                                super()._eat_figure(coordinates)
                                return True
                    elif not super()._is_diagonal_overstep(figure=self, coordinates=coordinates):
                        if super()._is_capture(self, coordinates):
                            super()._eat_figure(coordinates)
                            return True


# Класс Короля
class King(Figure):
    _name = 'King'

    def __init__(self, coordinates, color):
        super().__init__(self._name, coordinates, color)
        super()._create_figure(self, coordinates)

    def move(self, coordinates):
        pass
