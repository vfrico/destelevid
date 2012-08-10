#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from PySide import QtCore, QtGui
import destelevid_ui
import destelevid
import info_ui
class Destelevid(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(Destelevid, self).__init__(parent)
        self.ui = destelevid_ui.Ui_Destelevid()
        self.ui.setupUi(self)
        # Cerrar programa
        self.ui.botoncerrar.clicked.connect(self.cerrar)
        # Acerca de...
        self.ui.botonacercade.clicked.connect(self.acercade)
        # Descargar
        self.ui.botondescargar.clicked.connect(self.descargar)
        # Información de los servicios
        self.ui.botonintroduce.clicked.connect(self.informacion)
        # Descifrar
        self.ui.botondescifrar.clicked.connect(self.descifrar)
    def cerrar(self):
        """Cerrar programa"""
        print "Cerrando Destelevid"
        exit(0)
    def acercade(self):
        """Diálogo Acerca de"""
    def descargar(self):
        """Descargar vídeo"""
    def informacion(self):
        """Información de servicios"""
        infowindow = Ui_Dialog().setupUi()
    def descifrar(self):
        """Descifrar URL"""
        salida = destelevid.downloader(self.ui.lineEdit.text()).conseguirUrlVideo()
        if salida[1] != 0:
            ret = self.crearmessage('No se ha podido procesar el enlace',salida[0],'Error').exec_()
            if ret == QtGui.QMessageBox.Help:
                self.informacion()
        else:
            self.ui.lineEdit_2.setText(salida[0])
    def crearmessage(self,primario,secundario,error):
        mesbox = QtGui.QMessageBox()
        mesbox.setStandardButtons(QtGui.QMessageBox.Help|QtGui.QMessageBox.Ok)
        mesbox.setWindowTitle(error)
        mesbox.setText(primario)
        mesbox.setInformativeText(secundario)
        return mesbox
        
class Ui_Dialog():
    def __init__(self):
        """Muestra un diálogo con todos los servicios soportados"""
    def setupUi(self):
        Dialog = QtGui.QDialog()
        Dialog.setObjectName("Servicios")
        Dialog.resize(400, 300)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(50, 260, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 300, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.servicios = QtGui.QLabel(Dialog)
        self.servicios.setGeometry(QtCore.QRect(10, 50, 381, 151))
        self.servicios.setText("")
        self.servicios.setWordWrap(True)
        self.servicios.setObjectName("servicios")
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(10, 210, 371, 51))
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.exec_()
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Servicios", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Servicios soportados por Destelevid", None, QtGui.QApplication.UnicodeUTF8))
        self.servicios.setText(QtGui.QApplication.translate("Dialog", "rtve.es: alacarta\nrtvv.es: Mediateca\n\nGracias a PyDownTV:\nmitele.es", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "Destelevid usa la misma librería que PyDownTV. Gracias a su autor por liberarla libremente y permitir que este programa sea realidad", None, QtGui.QApplication.UnicodeUTF8))

        
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = Destelevid()
    myapp.show()
    sys.exit(app.exec_())

