from abc import abstractmethod

from django.db import models


# Create your models here.


# Класс игрового поля
class Field:
    _field = {
        'A1': None, 'B1': None, 'C1': None, 'D1': None, 'E1': None, 'F1': None, 'G1': None, 'H1': None,
        'A2': None, 'B2': None, 'C2': None, 'D2': None, 'E2': None, 'F2': None, 'G2': None, 'H2': None,
        'A3': None, 'B3': None, 'C3': None, 'D3': None, 'E3': None, 'F3': None, 'G3': None, 'H3': None,
        'A4': None, 'B4': None, 'C4': None, 'D4': None, 'E4': None, 'F4': None, 'G4': None, 'H4': None,
        'A5': None, 'B5': None, 'C5': None, 'D5': None, 'E5': None, 'F5': None, 'G5': None, 'H5': None,
        'A6': None, 'B6': None, 'C6': None, 'D6': None, 'E6': None, 'F6': None, 'G6': None, 'H6': None,
        'A7': None, 'B7': None, 'C7': None, 'D7': None, 'E7': None, 'F7': None, 'G7': None, 'H7': None,
        'A8': None, 'B8': None, 'C8': None, 'D8': None, 'E8': None, 'F8': None, 'G8': None, 'H8': None
    }

    @property
    def field(self):
        return self._field

    def set_figure(self, coordinates, figure):
        self._field[coordinates['x'] + coordinates['y']] = figure

    def set_none(self, coordinates):
        self._field[coordinates['x'] + coordinates['y']] = None


# Класс описывающий правила игры
class GameRules(Field):
    def _field_borders(self, coordinates):
        if coordinates['x'] + coordinates['y'] in self._field:
            return True


# Класс правил хода для фигур
class FigureRules:
    @staticmethod
    def _pawn_rules(name, coordinates_old, coordinates_new, moves_count):
        if name == 'pawn':
            if coordinates_old != coordinates_new:
                if moves_count == 0:
                    if coordinates_old['x'] == coordinates_new['x'] and 0 < int(coordinates_new['y']) - \
                            int(coordinates_old['y']) <= 2:
                        return True
                else:
                    if coordinates_old['x'] == coordinates_new['x'] and 0 < int(coordinates_new['y']) - \
                            int(coordinates_old['y']) <= 1:
                        return True


# Класс описывающий фигуру
class Figure(FigureRules, GameRules):
    # coordinates - координаты куда хочет сделать ход фигура
    # self._coordinates - текущие координаты фигуры

    _coordinates = {'x': None, 'y': None}

    def __init__(self, name, coordinates):
        if 'x' in coordinates:
            if 'y' in coordinates:
                if coordinates['x'] + coordinates['y'] in self._field:
                    self._name = name
                    self._coordinates = coordinates
                else:
                    raise Exception('Неверно введены координаты')
        else:
            raise Exception('Неверно введены ключи координат')

    def _set_position(self, coordinates):
        super().set_none(self._coordinates)
        super().set_figure(coordinates, self._name)
        self._coordinates = coordinates

    @abstractmethod
    def move_figure(self, coordinates):
        pass


# Класс пешки
class Pawn(Figure):
    _name = 'pawn'

    def __init__(self, coordinates):
        super().__init__(self._name, coordinates)
        super().set_figure(coordinates, self._name)
        self.__moves_count = 0

    def move_figure(self, coordinates):
        if super()._pawn_rules(self._name, self._coordinates, coordinates,
                               self.__moves_count) and super()._field_borders(coordinates):
            super()._set_position(coordinates)
            self.__moves_count += 1
        else:
            print('Ход невозможен')


# Класс Ладьи
class Rook(Figure):
    _name = 'Rook'

    def __init__(self, name, coordinates):
        super().__init__(name, coordinates)
        super().set_figure(coordinates, self._name)

    def move_figure(self, coordinates):
        pass


# Класс Коня
class Knight(Figure):
    _name = 'Knight'

    def __init__(self, name, coordinates):
        super().__init__(name, coordinates)
        super().set_figure(coordinates, self._name)

    def move_figure(self, coordinates):
        pass


# Класс Слона
class Bishop(Figure):
    _name = 'Bishop'

    def __init__(self, name, coordinates):
        super().__init__(name, coordinates)
        super().set_figure(coordinates, self._name)

    def move_figure(self, coordinates):
        pass


# Класс Королевы
class Queen(Figure):
    _name = 'Queen'

    def __init__(self, name, coordinates):
        super().__init__(name, coordinates)
        super().set_figure(coordinates, self._name)

    def move_figure(self, coordinates):
        pass


# Класс Короля
class King(Figure):
    _name = 'King'

    def __init__(self, name, coordinates):
        super().__init__(name, coordinates)
        super().set_figure(coordinates, self._name)

    def move_figure(self, coordinates):
        pass
