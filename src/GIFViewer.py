# -*- coding: utf-8 -*-

'''
* The MIT License (MIT)
* 
* Copyright (c) 2016 Wolfgang Almeida <wolfgang.almeida@yahoo.com>
* 
* Permission is hereby granted, free of charge, to any person obtaining a copy
* of this software and associated documentation files (the "Software"), to deal
* in the Software without restriction, including without limitation the rights
* to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
* copies of the Software, and to permit persons to whom the Software is
* furnished to do so, subject to the following conditions:
* 
* The above copyright notice and this permission notice shall be included in all
* copies or substantial portions of the Software.
* 
* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
* IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
* FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
* AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
* LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
* OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
* SOFTWARE.
'''

from PyQt4 import QtCore, QtGui
from os.path import expanduser, isfile
import sys
import os
import struct

version = "1.0"
home_dir = expanduser("~")
program_dir = os.environ["ProgramFiles"] + "\\GIFViewer\\"

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        global imageIndex
        global gifsInDir
        self.imageIndex = -1
        self.gifsInDir = []

        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(640, 480)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(program_dir + "Icon.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setFrameShape(QtGui.QFrame.StyledPanel)
        self.label.setFrameShadow(QtGui.QFrame.Sunken)
        self.label.setText(_fromUtf8(""))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton.clicked.connect(self.changePreviousImage)
        self.gridLayout.addWidget(self.pushButton, 1, 0, 1, 1)
        self.pushButton_2 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton_2.clicked.connect(self.changeNextImage)
        self.gridLayout.addWidget(self.pushButton_2, 1, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 20))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuArquivo = QtGui.QMenu(self.menubar)
        self.menuArquivo.setObjectName(_fromUtf8("menuArquivo"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionAbrir = QtGui.QAction(MainWindow)
        self.actionAbrir.setObjectName(_fromUtf8("actionAbrir"))
        self.actionAbrir.triggered.connect(self.getfile)
        self.actionLimpar = QtGui.QAction(MainWindow)
        self.actionLimpar.setObjectName(_fromUtf8("actionLimpar"))
        self.actionLimpar.triggered.connect(self.clearfile)
        self.actionSair = QtGui.QAction(MainWindow)
        self.actionSair.setObjectName(_fromUtf8("actionSair"))
        self.actionSair.triggered.connect(self.exitprogram)
        self.menuArquivo.addAction(self.actionAbrir)
        self.menuArquivo.addAction(self.actionLimpar)
        self.menuArquivo.addAction(self.actionSair)
        self.menubar.addAction(self.menuArquivo.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.openImageAssociate()

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "GIFViewer - v%s - " % (version), None))
        self.menuArquivo.setTitle(_translate("MainWindow", "Arquivo", None))
        self.actionAbrir.setText(_translate("MainWindow", "Abrir imagem...", None))
        self.actionLimpar.setText(_translate("MainWindow", "Limpar", None))
        self.actionSair.setText(_translate("MainWindow", "Sair", None))
        self.pushButton.setText(_translate("MainWindow", "<< Anterior", None))
        self.pushButton_2.setText(_translate("MainWindow", "Próxima >>", None))

    #================================================
    # Métodos do programa: Abrir e Reproduzir Imagens
    #================================================

    # Método de Troca para a Próxima Imagem
    # =====================================
    def changeNextImage(self):
        if self.gifsInDir == []:
            return
        else:
            self.nextIndex = self.imageIndex + 1
            if self.nextIndex > len(self.gifsInDir):
                return
            else:
                self.getNextImage = self.gifsInDir[self.nextIndex]
                self.getNextImagePath = os.path.abspath(self.getNextImage)

                self.gifsInDir = self.gettingFilesInDir(self.getNextImagePath)
                self.imageIndex = self.gifsInDir.index(self.getNextImage)
                self.width, self.height = self.getFileResolution(self.getNextImagePath)

                MainWindow.setWindowTitle(_translate("MainWindow", "GIFViewer - v%s - %s" % (version, str(self.getNextImagePath)), None))
                QtGui.QApplication.processEvents()

                MainWindow.resize(int(self.width), int(self.height))

                self.imgfile = QtGui.QMovie(self.getNextImagePath)
                self.label.setMovie(self.imgfile)
                self.label.setScaledContents(True)
                self.imgfile.start()

    # Método de Troca para a Imagem Anterior
    # ======================================
    def changePreviousImage(self):
        if self.imageIndex == -1:
            return
        else:
            self.previousIndex = self.imageIndex - 1
            if self.previousIndex == -1:
                return
            else:
                self.getPreviousImage = self.gifsInDir[self.previousIndex]
                self.getPreviousImagePath = os.path.abspath(self.getPreviousImage)

                self.gifsInDir = self.gettingFilesInDir(self.getPreviousImagePath)
                self.imageIndex = self.gifsInDir.index(self.getPreviousImage)
                self.width, self.height = self.getFileResolution(self.getPreviousImagePath)

                MainWindow.setWindowTitle(_translate("MainWindow", "GIFViewer - v%s - %s" % (version, str(self.getPreviousImagePath)), None))
                QtGui.QApplication.processEvents()

                MainWindow.resize(int(self.width), int(self.height))

                self.imgfile = QtGui.QMovie(self.getPreviousImagePath)
                self.label.setMovie(self.imgfile)
                self.label.setScaledContents(True)
                self.imgfile.start()

    # Método de Resgate de Resolução do Arquivo GIF
    # =============================================
    def getFileResolution(self, fnamePath):
        self.imgSize = os.path.getsize(str(self.fnamePath))

        with open(self.fnamePath) as self.input:
            self.height = -1
            self.width = -1
            self.imgData = self.input.read(25)

            try:
                if (self.imgSize >= 10) and self.imgData[:6] in ('GIF87a', 'GIF89a'):
                    self.w, self.h = struct.unpack("<HH", self.imgData[6:10])
                    self.width = int(self.w)
                    self.height = int(self.h)
                else:
                    return [1, 1]
            except Exception:
                return [1, 1]

        return [self.width, self.height]

    # Método de Recuperação de Arquivos GIF na Pasta do Arquivo Aberto
    # ================================================================
    def gettingFilesInDir(self, fnamePath):
        self.gifs = []
        self.fnameAbsPath = os.path.dirname(os.path.abspath(self.fnamePath))
        os.chdir(self.fnameAbsPath)
        
        for self.files in os.listdir(self.fnameAbsPath):
            if isfile(str(self.files)) == True:
                if self.files.endswith(".gif"):
                    self.gifs.append(self.files)
        
        return self.gifs

    # Método para Abrir Arquivos GIF Associados pelo Windows
    # ======================================================
    def openImageAssociate(self):
        try:
            if str(sys.argv[1]) != None:
                self.fnamePath = os.path.realpath(str(sys.argv[1]))
                self.fnameRealName = os.path.basename(self.fnamePath)

                MainWindow.setWindowTitle(_translate("MainWindow", "GIFViewer - v%s - %s" % (version, str(self.fnamePath).replace("/", "\\")), None))
                QtGui.QApplication.processEvents()

                self.width, self.height = self.getFileResolution(self.fnamePath)
                self.gifsInDir = self.gettingFilesInDir(self.fnamePath)
                self.imageIndex = self.gifsInDir.index(self.fnameRealName)

                self.imgfile = QtGui.QMovie(self.fnamePath)
                self.label.setMovie(self.imgfile)
                self.label.setScaledContents(True)
                MainWindow.resize(int(self.width), int(self.height))
                self.imgfile.start()
        except Exception:
            pass

    # Método de Abertura de Arquivos GIF Pelo Menu do Programa
    # ========================================================
    def getfile(self):
        global gifsInDir
        global imageIndex

        self.fname = QtGui.QFileDialog.getOpenFileName(MainWindow, 'Abrir Imagem...', home_dir, "Arquivo GIF (*.gif)")
        self.fnamePath = str(self.fname).replace("/", "\\")
        self.fnameRealName = os.path.basename(self.fnamePath)
        
        if str(self.fnamePath) != "":
            MainWindow.setWindowTitle(_translate("MainWindow", "GIFViewer - v%s - %s" % (version, str(self.fnamePath)), None))
            QtGui.QApplication.processEvents()

        self.width, self.height = self.getFileResolution(self.fnamePath)
        self.gifsInDir = self.gettingFilesInDir(self.fnamePath)
        self.imageIndex = self.gifsInDir.index(self.fnameRealName)

        MainWindow.resize(int(self.width), int(self.height))

        self.imgfile = QtGui.QMovie(self.fname)
        self.label.setMovie(self.imgfile)
        self.label.setScaledContents(True)
        self.imgfile.start()

    # Método de Limpeza de Arquivo GIF no Programa
    # ============================================
    def clearfile(self):
        self.label.clear()
        MainWindow.setWindowTitle(_translate("MainWindow", "GIFViewer - v%s" % (version), None))
        QtGui.QApplication.processEvents()

    # Método de Saída do Programa pelo Menu
    # =====================================
    def exitprogram(self):
        sys.exit(0)

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

