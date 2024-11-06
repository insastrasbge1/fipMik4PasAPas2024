import PySide6.QtWidgets as qtw
import PySide6.QtGui as qtg
from model import Groupe,Point

class CoordPoint(qtw.QFrame) :
    def __init__(self,main : 'Main'):
        super().__init__()
        self._main = main
        self._tfPx = qtw.QLineEdit()
        self._tfPy = qtw.QLineEdit()
        self._bCreer = qtw.QPushButton("créer")
        self._bCreer.clicked.connect(self.doCree)
        labels = qtw.QVBoxLayout()
        labels.addWidget(qtw.QLabel("px :"))
        labels.addWidget(qtw.QLabel("py :"))
        mainLayout = qtw.QHBoxLayout()
        mainLayout.addLayout(labels)
        coords = qtw.QVBoxLayout()
        coords.addWidget(self._tfPx)
        coords.addWidget(self._tfPy)
        mainLayout.addLayout(coords)
        mainLayout.addWidget(self._bCreer)
        self.setLayout(mainLayout)

    def doCree(self):
        m = self._main.model
        px = float(self._tfPx.text())
        py = float(self._tfPy.text())
        newPoint = Point(px,py)
        m.add_figure(newPoint)
        self._main.updateView()

    def updateView(self):
        pass

class DessineModel(qtw.QGraphicsScene) :
    def __init__(self,main : 'Main'):
        super().__init__()
        self._main = main
        self.setSceneRect(0,0,600,400)
        self.updateView()

    def updateView(self):
        self.clear()
        self._main.model.dessine(self)

    def mousePressEvent(self, event:qtw.QGraphicsSceneMouseEvent):
        px = event.scenePos().x()
        py = event.scenePos().y()
        self._main.model.add_figure(Point(px,py))
        self._main.updateView()


class dessinView(qtw.QGraphicsView) :
    def __init__(self,main : 'Main'):
        super().__init__()
        self._main = main
        self._scene = DessineModel(self._main)
        self.setScene(self._scene)
        self.updateView()

    def updateView(self):
        self._scene.updateView()

class Main(qtw.QFrame) :
    def __init__(self,model : 'Groupe'):
        super().__init__()
        self._model = model
        self._coords = CoordPoint(self)
        self._taMessage = qtw.QTextEdit()
        self._taMessage.setEnabled(False)
        mainLayout = qtw.QVBoxLayout()
        mainLayout.addWidget(self._coords)
        mainLayout.addWidget(self._taMessage)
        self._vueGraphique = dessinView(self)
        mainLayout.addWidget(self._vueGraphique)
        self.setLayout(mainLayout)
        self.updateView()

    @property
    def model(self):
        return self._model

    def updateView(self):
        self._taMessage.setText(self.model.str_detail())
        self._coords.updateView()
        self._vueGraphique.updateView()

def debut():
    app = qtw.QApplication()
    main = Main(Groupe())
    main.show()
    app.exec()

if __name__ == '__main__':
    debut()
