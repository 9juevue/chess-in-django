from abc import abstractmethod

from django.db import models


# Create your models here.


# Класс игрового поля
class Field:
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

    @property
    def field(self):
        return self._field

    # Возвращает поле в читабельном виде для консоли
    def _get_console_field(self):
        i = 0
        for key in self._field:
            obj = self._field[key]
            if i % 8 == 0:
                print('')
            if obj is None:
                print(None, end=' ')
            else:
                print(obj.name, end=' ')
            i += 1
        print('')

    # Ставит фигуру на начальное положение в доске
    def _set_figure(self, coordinates, figure):
        if self._check_coordinates(coordinates):
            self._field[coordinates['x'] + coordinates['y']] = figure

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


# Класс описывающий правила игры
class GameRules(Field):

    # Проверяет, не перешла ли границы поля фигура
    def _field_borders(self, coordinates):
        if coordinates['x'] + coordinates['y'] in self._field:
            return True

    # Проверяет, занято ли поле фигурой
    def _is_field_occupied(self, figure, coordinates):
        key = coordinates['x'] + coordinates['y']
        if self.field[key] is not None:
            if figure.color == self.field[key].color:
                print('Поле занято союзной фигурой')
                return True
            else:
                print('Поле занято вражеской фигурой')
                return True

    # Проверяет, есть ли вертикальном пути фигуры другие фигуры
    def _is_vertical_overstep(self, figure, coordinates):
        key = coordinates['x'] + coordinates['y']
        if self.field[key] is None:
            for i in range(int(figure.coordinates['y']) + 1, int(coordinates['y'])):
                if self.field[coordinates['x'] + str(i)] is not None:
                    print('Вы пытаетесь перешагнуть через фигуру(ы)')
                    return True

    # Взятие пешкой
    def _is_capture_by_pawn(self, pawn, coordinates):
        pass


# Класс правил хода для фигур
class FigureRules:

    # Проверяет, может ли пешка сделать ход
    @staticmethod
    def _pawn_rules(pawn, coordinates):
        if pawn.name == 'Pawn':
            if pawn.coordinates != coordinates:
                if pawn.moves_count == 0:
                    if pawn.coordinates['x'] == coordinates['x'] and 0 < int(coordinates['y']) - \
                            int(pawn.coordinates['y']) <= 2:
                        return True
                else:
                    if pawn.coordinates['x'] == coordinates['x'] and 0 < int(coordinates['y']) - \
                            int(pawn.coordinates['y']) <= 1:
                        return True
        print('Ход невозможен')

    # Проверяет, может ли ладья сделать ход
    @staticmethod
    def _rook_rules(rook, coordinates):
        if rook.name == 'Rook':
            if rook.coordinates != coordinates:
                if rook.coordinates['x'] == coordinates['x'] or rook.coordinates['y'] == coordinates['y']:
                    return True
        print('Ход невозможен')


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

    # Ставит фигуру на заданную позицию
    def _set_position(self, coordinates, figure):
        super()._set_none(self._coordinates)
        super()._set_figure(coordinates, figure)
        self._coordinates = coordinates
        self._id = self._color + self._name + coordinates['x'] + coordinates['y']

    @abstractmethod
    def move(self, coordinates):
        pass

    # Проверяет цвет фигуры
    @staticmethod
    def check_figure_color(color):
        if color == 'White' or color == 'white':
            return True
        elif color == 'Black' or color == 'black':
            return True
        else:
            print('Неверно введён цвет фигуры')


# Класс Пешки
class Pawn(Figure):
    _name = 'Pawn'

    def __init__(self, coordinates, color):
        super().__init__(self._name, coordinates, color)
        super()._set_figure(coordinates, self)
        self.__moves_count = 0

    @property
    def moves_count(self):
        return self.__moves_count

    # Ставит пешку на заданную позицию, с проверками
    def move(self, coordinates):
        if super()._check_coordinates(coordinates):
            if super()._pawn_rules(self, coordinates):
                if super()._field_borders(coordinates):
                    if not super()._is_field_occupied(figure=self, coordinates=coordinates):
                        if not super()._is_vertical_overstep(figure=self, coordinates=coordinates):
                            super()._set_position(coordinates, self)
                            self.__moves_count += 1


# Класс Ладьи
class Rook(Figure):
    _name = 'Rook'

    def __init__(self, coordinates, color):
        super().__init__(self._name, coordinates, color)
        super()._set_figure(coordinates, self)

    # Ставим ладью на заданную позицию, с проверками
    def move(self, coordinates):
        if super()._check_coordinates(coordinates):
            if super()._rook_rules(self, coordinates):
                if not super()._is_field_occupied(figure=self, coordinates=coordinates):
                    if not super()._is_vertical_overstep(figure=self, coordinates=coordinates):
                        super()._set_position(coordinates, self)


# Класс Коня
class Knight(Figure):
    _name = 'Knight'

    def __init__(self, coordinates, color):
        super().__init__(self._name, coordinates, color)
        super()._set_figure(coordinates, self)

    def move(self, coordinates):
        pass


# Класс Слона
class Bishop(Figure):
    _name = 'Bishop'

    def __init__(self, coordinates, color):
        super().__init__(self._name, coordinates, color)
        super()._set_figure(coordinates, self)

    def move(self, coordinates):
        pass


# Класс Королевы
class Queen(Figure):
    _name = 'Queen'

    def __init__(self, coordinates, color):
        super().__init__(self._name, coordinates, color)
        super()._set_figure(coordinates, self)

    def move(self, coordinates):
        pass


# Класс Короля
class King(Figure):
    _name = 'King'

    def __init__(self, coordinates, color):
        super().__init__(self._name, coordinates, color)
        super()._set_figure(coordinates, self)

    def move(self, coordinates):
        pass
