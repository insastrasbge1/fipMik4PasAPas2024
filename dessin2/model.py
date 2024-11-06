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


class Figure(metaclass=abc.ABCMeta):

    @property
    def groupe(self) -> Optional['Groupe']:
        return self._groupe

    def __init__(self):
        # appel de la méthode init de object
        # inutile puisqu'elle ne fait rien, mais je trouve
        # qu'appeler 'super' systématiquement (sauf cas très particuliers)
        # est une bonne habitude
        # print("init de Figure")
        super().__init__()
        self._groupe = None

    def str_detail(self) -> str:
        """renvoie une description textuelle détaillée de la figure
        par defaut, simplement même chose que __str__
        mais peut-être spécialisée dans certaines sous-classes
        """
        return self.__str__()

    @abc.abstractmethod
    def min_x(self) -> float:
        """ renvoie l'abscice minimale d'une figure"""
        raise NotImplementedError("pas de valeur par défaut pour minX")

    @abc.abstractmethod
    def dessine(self,zg : qtw.QGraphicsScene) -> None:
        """ renvoie l'abscice minimale d'une figure"""
        raise NotImplementedError("doit être défini dans sous-classes")


    @abc.abstractmethod
    def max_x(self) -> float:
        """ renvoie l'abscice maximale d'une figure"""
        raise NotImplementedError("pas de valeur par défaut pour maxX")

    @abc.abstractmethod
    def min_y(self) -> float:
        """ renvoie l'ordonnée minimale d'une figure"""
        raise NotImplementedError("pas de valeur par défaut pour minY")

    @abc.abstractmethod
    def max_y(self) -> float:
        """ renvoie l'ordonnée maximale d'une figure"""
        raise NotImplementedError("pas de valeur par défaut pour maxY")

    def largeur(self) -> float:
        return self.max_x() - self.min_x()

    def hauteur(self) -> float:
        return self.max_y() - self.min_y()

    @abc.abstractmethod
    def distance_point(self, p: 'Point') -> float:
        """ calcule la distance euclidienne entre une Figure et un Point"""
        raise NotImplementedError("pas de valeur par défaut pour distance_point")

    @abc.abstractmethod
    def dessine(self,scene : qtw.QGraphicsScene) -> None:
        """ajoute la représentation graphique de la figure à la scene"""
        raise NotImplementedError("pas de valeur par défaut pour dessine")


class FigureSimple(Figure, metaclass=abc.ABCMeta):

    @property
    def couleur(self) -> QColor:
        return self._couleur

    @couleur.setter
    def couleur(self, couleur: QColor) -> None:
        self._couleur = couleur

    def __init__(self, couleur: QColor = QColor(0, 0, 0)):
        # print("init de FigureSimple")
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
                 couleur: QColor = QColor(0, 0, 0)):
        # print("init de Point")
        super().__init__(couleur)
        self._px = px
        self._py = py

    def __str__(self):
        return f"({self.px},{self.py};{self.color_str()})"

    def min_x(self) -> float:
        return self.px

    def max_x(self) -> float:
        return self.px

    def min_y(self) -> float:
        return self.py

    def max_y(self) -> float:
        return self.py

    def distance_point(self, p: 'Point') -> float:
        dx = self.px - p.px
        dy = self.py - p.py
        return (dx * dx + dy * dy) ** 0.5

    def dessine(self,scene : qtw.QGraphicsScene) -> None:
        ellipse = qtw.QGraphicsEllipseItem(self.px-Point.taillePoint()/2,
                                           self.py-Point.taillePoint()/2,
                                           Point.taillePoint(),
                                           Point.taillePoint())
        # Define the brush (fill).
        brush = qtg.QBrush(self.couleur)
        ellipse.setBrush(brush)
        # Define the pen (line)
        pen = qtg.QPen(qtg.QPen(self.couleur, 1))
        ellipse.setPen(pen)
        # puis on l'ajoute à la scene
        scene.addItem(ellipse)

    @classmethod
    def taillePoint(cls):
        return 10;

    @classmethod
    def demande(cls) -> 'Point':
        print("px ?")
        px = float(input())
        print("py ?")
        py = float(input())
        print("couleur ?")
        couleur = demande_couleur()
        return cls(px, py, couleur)

    @classmethod
    def point_alea(cls,
                   min_x: float = 0, max_x: float = 400.0,
                   min_y: float = 0, max_y: float = 400.0) -> 'Point':
        return Point(random.uniform(min_x, max_x),
                     random.uniform(min_y, max_y),
                     couleurAlea())


class Segment(FigureSimple):

    @property
    def debut(self) -> Point:
        return self._debut

    @property
    def fin(self) -> Point:
        return self._fin

    def __init__(self, debut: Point, fin: Point,
                 couleur: QColor = QColor(0, 0, 0)):
        super().__init__(couleur)
        self._debut = debut
        self._fin = fin

    def __str__(self):
        return f"[{self.debut},{self.fin}]"

    def min_x(self) -> float:
        return min(self.debut.min_x(), self.fin.min_x())

    def max_x(self) -> float:
        return max(self.debut.min_x(), self.fin.min_x())

    def min_y(self) -> float:
        return min(self.debut.min_y(), self.fin.min_y())

    def max_y(self) -> float:
        return min(self.debut.min_y(), self.fin.min_y())

    def distance_point(self, p: 'Point') -> float:
        x1 = self.debut.px
        y1 = self.debut.py
        x2 = self.fin.px
        y2 = self.fin.py
        x3 = p.px
        y3 = p.py
        up = ((x3 - x1) * (x2 - x1) + (y3 - y1) * (y2 - y1)) / ((x2 - x1)**2 + (y2 - y1)**2)
        if up < 0:
            # la projection du point sur la droite est "avant" le point début du segment
            return self.debut.distance_point(p)
        elif up > 1:
            # la projection du point sur la droite est "après" le point fin du segment
            return self.fin.distance_point(p)
        else:
            # on calcule la projection du point p sur le segment
            proj = Point(x1 + up * (x2 - x1),
                         y1 + up * (y2 - y1))
            return proj.distance_point(p)

    def dessine(self,scene : qtw.QGraphicsScene) -> None:
        ligne = qtw.QGraphicsLineItem(self.debut.px,self.debut.py,
                                           self.fin.px,self.fin.py)
        # Define the pen (line)
        pen = qtg.QPen(qtg.QPen(self.couleur, 2))
        ligne.setPen(pen)
        # puis on l'ajoute à la scene
        scene.addItem(ligne)

    @classmethod
    def demande(cls):
        print("point début ?")
        debut = Point.demande()
        print("point fin ?")
        fin = Point.demande()
        print("couleur ?")
        couleur = demande_couleur()
        return cls(debut, fin, couleur)

    @classmethod
    def segment_alea(cls,
                     min_x: float = 0, max_x: float = 400.0,
                     min_y: float = 0, max_y: float = 400.0) -> 'Segment':
        return Segment(Point.point_alea(min_x, max_x, min_y, max_y),
                       Point.point_alea(min_x, max_x, min_y, max_y),
                       couleurAlea())


def prefixe_lignes(s: str, prefix: str) -> str:
    """
    ajoute prefix au début de chaque ligne de str
    """
    lignes = s.split("\n")
    return prefix + reduce((lambda s1, s2: s1 + "\n" + prefix + s2), lignes)


class Groupe(Figure):

    @property
    def contient(self) -> list['Figure']:
        return self._contient

    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # !!! attention piège python !!!
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #
    # ci-dessous un exemple d'init avec une liste optionnelle :
    # on veut, dans le cas ou l'argument "contient" n'est pas donné
    # l'initialiser avec une liste vide.
    # on pourrait penser présenter les chose comme ci-dessous :
    #    def __init__(self, contient: list[Figure] = []):
    # Malheureusement, ce n'est pas faux en python, mais cela ne fait
    # pas ce que l'on veut :
    #   . la liste vide [] apparait dans l'entête de la fonction
    #   . cette entete ne sera évalué qu'une fois par python lors de
    #     la définition de la fonction
    #   ==> !!! tous les appels sans paramètres utiliseront la même liste
    #   ==> !!! si une instance modifie la liste, elle sera modifiée pour
    #   ==> !!! toutes les instances
    #   ==> Ce n'est clairement pas ce que l'on veut :
    #       Chaque groupe doit posséder sa propre liste de sous-figure
    #       indépendament des autres groupes
    # Vous avez ci-dessous le contournement classique de ce piège :
    #    . si le paramètre n'est pas présent, on l'initialise à None
    #    . dans le corps de la méthode d'initialisation, on teste:
    #    . si le paramètre est None, on affecte la liste vide à l'attribut
    # Notez que dans ce cas, la liste vide apparait dans le corps de la
    # méthode
    # ==> une NOUVELLE liste vide sera créée pour chaque appel
    def __init__(self, contient: list[Figure] = None):
        super().__init__()
        if contient:
            self._contient = contient
        else:
            self._contient = []

    def __str__(self):
        return f"Groupe({len(self._contient)} sous-figures)"

    def str_detail(self):
        res = ''
        for nf in range(len(self.contient)):
            res = res + self.contient[nf].str_detail()
            if nf != len(self.contient) - 1:
                res = res + '\n'
        return 'Groupe{\n' + \
               prefixe_lignes(res, '  | ') + "\n}"

    def min_x(self) -> float:
        if self.contient:
            return reduce((lambda m1, m2: min(m1, m2)),
                          map(lambda f: f.min_x(), self.contient))
        else:
            # par convention, un groupe vide est considéré
            # de taille nulle à l'origine
            return 0.0

    def max_x(self) -> float:
        if self.contient:
            return reduce((lambda m1, m2: min(m1, m2)),
                          map(lambda f: f.max_x(), self.contient))
        else:
            # par convention, un groupe vide est considéré
            # de taille nulle à l'origine
            return 0.0

    def min_y(self) -> float:
        if self.contient:
            return reduce((lambda m1, m2: min(m1, m2)),
                          map(lambda f: f.min_y(), self.contient))
        else:
            # par convention, un groupe vide est considéré
            # de taille nulle à l'origine
            return 0.0

    def max_y(self) -> float:
        if self.contient:
            return reduce((lambda m1, m2: min(m1, m2)),
                          map(lambda f: f.min_x(), self.contient))
        else:
            # par convention, un groupe vide est considéré
            # de taille nulle à l'origine
            return 0.0

    def distance_point(self, p: 'Point') -> float:
        if self.contient:
            res = 0
            for fig in self.contient :
                d = fig.distance_point(p)
                if d < res :
                    res = d
            return res
        else :
            # pour ne pas générer d'erreurs,
            # on estime qu'un groupe vide est situé en (0,0)
            return (p.px*p.px + p.py * p.py) ** 0.5

    def dessine(self,scene : qtw.QGraphicsScene) -> None:
        for fig in self.contient :
            fig.dessine(scene)

    def choisi_point(self) -> Point:
        """permet à l'utilisateur de choisir un point existant"""
        les_points = [x for x in self.contient if isinstance(x, Point)]
        rep = -1
        while rep <= 0 or rep > len(les_points):
            print("points existants: ")
            num = 1
            for p in les_points:
                print(f"{num}: {p.str_detail()}")
                num = num + 1
            print("choisissez un point en indiquant son numéro ?")
            rep = int(input())
        return les_points[rep-1]

    def choisi_sous_figures(self) -> list[Figure]:
        rep = -1
        res: list[Figure] = []
        reste = self.contient.copy()
        while rep != 0:
            print("--- actuellement selectionnés ---")
            if res:
                for p in res:
                    print(p.str_detail())
            else:
                print("aucun")
            num = 1
            print("--- selectionnables ---")
            for p in reste:
                print(f"{num}: {p.str_detail()}")
                num = num + 1
            print("choisissez une figure a ajouter à la selection (0 pour finir) ?")
            rep = int(input())
            if rep < 0 or rep > len(reste):
                print(f"indiquez un entier entre 1 et {len(reste)}, ou 0 pour quitter")
            elif rep != 0:
                nouveau = reste[rep-1]
                del reste[rep-1]
                res.append(nouveau)
        return res

    def add_figure(self, f: Figure) -> None:
        """
        ajoute la figure f au groupe self
        :raises Exception() si f appartient déjà à un groupe
        """
        if f._groupe:
            raise Exception('figure déjà dans un groupe')
        self._contient.append(f)
        f._groupe = self

    def remove_figure(self, f: Figure) -> None:
        """
        enleve la figure f du groupe self
        :raises Exception() si f n'appartient pas au groupe
        """
        if f._groupe != self:
            raise Exception('figure pas dans le groupe')
        self.contient.remove(f)

    @classmethod
    def groupe_alea(cls, nbr_points: int = 10, nbr_segments: int = 5,
                    min_x: float = 0, max_x: float = 400.0,
                    min_y: float = 0, max_y: float = 400.0) -> 'Groupe':
        res = Groupe()
        for i in range(nbr_points):
            res.add_figure(Point.point_alea(min_x, max_x, min_y, max_y))
        for i in range(nbr_segments):
            res.add_figure(Segment.segment_alea(min_x, max_x, min_y, max_y))
        return res

    @classmethod
    def menu_principal(cls) -> None:
        choix = -1
        nbr_items = 0
        cur = Groupe()
        while choix != 0:
            print("creation/lecture d'un groupe de figures")
            print("---------------------------------------")
            print(f"groupe courant : {cur}")
            nbr_items = 1
            print(f"{nbr_items}): créer un groupe vide")
            nbr_items = nbr_items + 1
            print(f"{nbr_items}): créer un groupe aléatoire 10 points 3 segments dans rectangle [0,0,400,400]")
            nbr_items = nbr_items + 1
            print(f"{nbr_items}): créer un groupe aléatoire quelconque")
            nbr_items = nbr_items + 1
            print(f"{nbr_items}): modifier le groupe courant")
            nbr_items = nbr_items + 1

            print("0): quitter")
            print("votre choix ?")
            choix = int(input())
            if choix == 1:
                cur = Groupe()
            elif choix == 2:
                cur = Groupe.groupe_alea()
            elif choix == 3:
                print("nombre de points")
                nbr_points = int(input())
                print("nombre de segments")
                nbr_segments = int(input())
                print("min X")
                min_x = float(input())
                print("max X")
                max_x = float(input())
                print("min Y")
                min_y = float(input())
                print("max Y")
                max_y = float(input())
                cur = Groupe.groupe_alea(nbr_points, nbr_segments,
                                         min_x, max_x, min_y, max_y)
            elif choix == 4:
                cur.menu_gestion()

    def menu_gestion(self) -> None:
        choix = -1
        nbr_items = 0
        while choix != 0:
            print("Gestion groupe de figures")
            print("-------------------------")
            nbr_items = 1
            print(f"{nbr_items}): afficher la liste des sous-figure")
            nbr_items = nbr_items + 1
            print(f"{nbr_items}): ajouter un point")
            nbr_items = nbr_items + 1
            print(f"{nbr_items}): ajouter des points aléatoires")
            nbr_items = nbr_items + 1
            print(f"{nbr_items}): ajouter un segment en définissant les points extremités")
            nbr_items = nbr_items + 1
            print(f"{nbr_items}): ajouter un segment avec des points extremités existants")
            nbr_items = nbr_items + 1
            print(f"{nbr_items}): calculer minX du groupe")
            nbr_items = nbr_items + 1
            print(f"{nbr_items}): créer un sous-groupe")
            nbr_items = nbr_items + 1
            print(f"{nbr_items}): supprimer des sous-figures")

            print("0): quitter")
            print("votre choix ?")
            choix = int(input())
            if choix == 1:
                print(self.str_detail())
            elif choix == 2:
                self.add_figure(Point.demande())
            elif choix == 3:
                print("nombre de points:")
                n = int(input())
                for i in range(n):
                    self.add_figure(Point.point_alea())
            elif choix == 4:
                self.add_figure(Segment.demande())
            elif choix == 5:
                print("point début: ")
                p1 = self.choisi_point()
                print("point fin: ")
                p2 = self.choisi_point()
                self.add_figure(Segment(p1, p2))
            elif choix == 6:
                print(f"minX = {self.min_x()}")
            elif choix == 7:
                to_groupe = self.choisi_sous_figures()
                for f in to_groupe:
                    self.remove_figure(f)
                nouveau = Groupe(to_groupe)
                self.add_figure(nouveau)
            elif choix == 8:
                to_del = self.choisi_sous_figures()
                for f in to_del:
                    self.remove_figure(f)


if __name__ == '__main__':
    Groupe.menu_principal()
