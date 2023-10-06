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


# Класс описывающий правила игры
class GameRules(Field):

    # Проверяет, занято ли поле фигурой
    def _is_field_occupied(self, coordinates):
        key = coordinates['x'] + coordinates['y']

        if self.field[key] is not None:
            return True

    # Проверяет, есть ли вертикальном пути фигуры другие фигуры
    def _is_vertical_overstep(self, figure, coordinates):
        key = coordinates['x'] + coordinates['y']

        if self.field[key] is None:
            for i in range(int(figure.coordinates['y']) + 1, int(coordinates['y'])):
                if self.field[coordinates['x'] + str(i)] is not None:
                    return True

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
        if rook.name == 'Rook':
            if rook.coordinates != coordinates:
                if rook.coordinates['x'] == coordinates['x'] or rook.coordinates['y'] == coordinates['y']:
                    return True
        return False


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
        if color == 'White' or color == 'white':
            return True
        elif color == 'Black' or color == 'black':
            return True
        else:
            print('Неверно введён цвет фигуры')
            return False

    # Если цвет фигуры черные возвращает истину
    def is_black(self):
        if self.color == 'Black' or self.color == 'black':
            return True
        return False

    # Если цвет фигуры белый возвращает истину
    def is_white(self):
        if self.color == 'White' or self.color == 'white':
            return True
        return False

    # "Убивает" фигуру
    @staticmethod
    def _kill_figure(figure):
        figure._is_dead = True


# Класс Пешки
class Pawn(Figure):
    _name = 'Pawn'

    def __init__(self, coordinates, color):
        super().__init__(self._name, coordinates, color)
        super()._create_figure(self, coordinates)
        self.__moves_count = 0

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
                        self.__moves_count += 1
            elif super()._is_capture_by_pawn(self, coordinates):
                figure = super()._field[coordinates['x'] + coordinates['y']]
                self._kill_figure(figure)
                super()._set_position(coordinates, self)
                self.__moves_count += 1


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


# Класс Коня
class Knight(Figure):
    _name = 'Knight'

    def __init__(self, coordinates, color):
        super().__init__(self._name, coordinates, color)
        super()._create_figure(self, coordinates)

    def move(self, coordinates):
        pass


# Класс Слона
class Bishop(Figure):
    _name = 'Bishop'

    def __init__(self, coordinates, color):
        super().__init__(self._name, coordinates, color)
        super()._create_figure(self, coordinates)

    def move(self, coordinates):
        pass


# Класс Королевы
class Queen(Figure):
    _name = 'Queen'

    def __init__(self, coordinates, color):
        super().__init__(self._name, coordinates, color)
        super()._create_figure(self, coordinates)

    def move(self, coordinates):
        pass


# Класс Короля
class King(Figure):
    _name = 'King'

    def __init__(self, coordinates, color):
        super().__init__(self._name, coordinates, color)
        super()._create_figure(self, coordinates)

    def move(self, coordinates):
        pass
