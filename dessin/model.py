# Copyright 2022 Francois de Bertrand de Beuvron
#
# This file is part of CoursBeuvron.
#
# CoursBeuvron is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# CoursBeuvron is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CoursBeuvron.  If not, see <http://www.gnu.org/licenses/>.
"""
Created on 2022-07-03

@author: Francois de Bertrand de Beuvron
"""
import random
import abc
from functools import reduce
from typing import Optional

from PySide6.QtGui import QColor
import PySide6.QtWidgets as qtw
import PySide6.QtGui as qtg

class Figure(metaclass=abc.ABCMeta) :
    def __init__(self):
        pass

    @abc.abstractmethod
    def minX(self) -> float:
        raise Exception("ne devrait jamais arriver")

    @abc.abstractmethod
    def maxX(self) -> float:
        raise Exception("ne devrait jamais arriver")

    def largeur(self) -> float:
        return self.maxX() - self.minX()

class FigureSimple(Figure,metaclass=abc.ABCMeta):

    @property
    def couleur(self) -> QColor:
        return self._couleur

    @couleur.setter
    def couleur(self, couleur: QColor) -> None:
        self._couleur = couleur

    def __init__(self, couleur: QColor = QColor(0, 0, 0)):
        super().__init__()
        self._couleur = couleur

    def color_str(self) -> str:
        return str(self.couleur.getRgb())


def demande_composante_couleur(compo_name: str) -> int:
    rep = - 1
    while rep < 0 or rep > 255:
        print(f"composante {compo_name}: (0-255) ?")
        rep = int(input())
    return rep


def demande_couleur() -> QColor:
    rouge = demande_composante_couleur('rouge')
    vert = demande_composante_couleur('vert')
    bleu = demande_composante_couleur('bleu')
    return QColor(rouge, vert, bleu)

def couleurAlea() -> QColor:
    return QColor(random.randrange(256),
                  random.randrange(256),
                  random.randrange(256))

class Point(FigureSimple):

    @property
    def px(self) -> float:
        return self._px

    @px.setter
    def px(self, px: float) -> None:
        self._px = px

    @property
    def py(self) -> float:
        return self._py

    @py.setter
    def py(self, py: float) -> None:
        self._py = py

    def __init__(self, px: float = 0.0, py: float = 0.0,
                 couleur : QColor = QColor(0,0,255)):
        super().__init__(couleur)
        self._px = px
        self._py = py
        self._couleur = QColor(0,0,0)

    def __str__(self):
        return f"({self.px},{self.py})"

    def minX(self) -> float:
        return self.px

    def maxX(self) -> float:
        return self.px


class Segment(FigureSimple):

    @property
    def debut(self) -> Point:
        return self._debut

    @property
    def fin(self) -> Point:
        return self._fin

    def __init__(self, debut: Point, fin: Point,
                 couleur : QColor = QColor(255,0,255)):
        super().__init__(couleur)
        self._debut = debut
        self._fin = fin

    def __str__(self):
        return f"[{self.debut},{self.fin}]"

    def minX(self) -> float:
        return min(self.debut.minX(),self.fin.minX())

    def maxX(self) -> float:
        return max(self.debut.maxX(),self.fin.maxX())


if __name__ == '__main__':
    p0 = Point(0,0)
    print(f"couleur de p0 : {p0.couleur}")
    p1 = Point(1,1)
    print(f"minX de p1 : {p1.minX()}")
    s1 = Segment(p0,p1)
    print(f"s1 = {s1}")
    print(f"minX de s1 : {s1.minX()}")
    print(f"largeur de s1 : {s1.largeur()}")

