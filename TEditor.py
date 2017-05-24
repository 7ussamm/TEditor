#!/usr/bin/python 
#__author__ = 'Hussam Ashraf'


from PyQt4.QtGui import *
from PyQt4.QtCore import *
from os import getcwd
import sys



# main app class

class TEditor(QMainWindow):

    def __init__(self):
        super(TEditor, self).__init__()

        QApplication.setStyle(QStyleFactory.create('plastique'))
        self.resize(1000, 600)
        self.setWindowTitle('TEditor')
        self.setStyleSheet('QWidget {background-color:#404552; color:white}')
        self.setWindowIcon(QIcon('icons/pyico.ico'))
        self.setMinimumWidth(1000)



        #self.setWindowFlags(Qt.FramelessWindowHint)



       ## File Choices

        openFile = QAction('Open', self)
        openFile.triggered.connect(self.opnFle)
        openFile.setShortcut('alt+o')
        openFile.setStatusTip('Open New File')

        save = QAction('Save', self)
        save.triggered.connect(self.saveMe)
        save.setShortcut('ctrl+s')
        save.setStatusTip('Save your current adjustments')

        saveAs = QAction('Save As...', self)
        saveAs.triggered.connect(self.saveMeAs)
        saveAs.setShortcut('ctrl+alt+s')
        saveAs.setStatusTip('Save Your File As...')

        ext = QAction('Exit', self)
        ext.triggered.connect(self.closeMe)
        ext.setStatusTip('Exiting your Application!!')
        ext.setShortcut('ctrl+q')

###############################################################
       ## Edit Choices

        undo = QAction('Undo', self)
        undo.triggered.connect(self.undoMe)
        undo.setShortcut('ctrl+z')


        redo = QAction('Redo', self)
        redo.triggered.connect(self.redoMe)
        redo.setShortcut('ctrl+y')


        cut = QAction('Cut', self)
        cut.triggered.connect(self.cutText)
        cut.setShortcut('ctrl+x')


        cpy = QAction('Copy', self)
        cpy.triggered.connect(self.copyText)
        cpy.setShortcut('ctrl+c')


        paste = QAction('Paste', self)
        paste.triggered.connect(self.pasteText)
        paste.setShortcut('ctrl+v')

##########################################################
       ## Help Choices
        self.about = QAction('About', self)
        self.about.triggered.connect(self.aboutMe)
        self.about.setStatusTip('About this Program')


        self.statusBar()


        mMenue = self.menuBar()
        mMenue.setStyleSheet('QWidget {background-color:#2F343F;}')
        fileMenue = mMenue.addMenu('File')
        editMenue = mMenue.addMenu('Edit')
        helpMenue = mMenue.addMenu('Help')


        fileMenue.addActions((openFile, save, saveAs , ext))
        editMenue.addActions((undo, redo, cut, cpy, paste))
        helpMenue.addAction(self.about)

    #################################################



        self.center()
        self.body()
        self.TextEditor()

        self.compareText = '' + str(self.readText()) # store the text in TextEditor once the app starts


        self.dirctory = '' # if open bottun clicked, this var will change





    ## place the app in the center of the screen



    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())



    def body(self):

    ### toolbar section
        openBtn = QAction(QIcon('icons/open.png'),'Open New File', self)
        openBtn.triggered.connect(self.opnFle)
        openBtn.setStatusTip('Open New File')

        saveBtn = QAction(QIcon('icons/save.png'), 'Save', self)
        saveBtn.triggered.connect(self.saveMe)
        saveBtn.setStatusTip('Overwrite The Current')

        extBtn = QAction(QIcon('icons/close.png'), 'Exit', self)
        extBtn.triggered.connect(self.closeMe)
        extBtn.setStatusTip('Leaving The Program!!!')

        selectBtn = QAction(QIcon('icons/select.png'), 'Select', self)
        selectBtn.triggered.connect(self.selectAll)
        selectBtn.setStatusTip('Select All text')







        toolbar = self.addToolBar('toolbar')
        toolbar.setStyleSheet('QWidget {background-color:#383C4A; border-top: 0.5px solid #404552}')

        toolbar.addActions((openBtn, saveBtn, selectBtn ,extBtn))

    ### bottuns section

        fontBtn = QPushButton('Font', self)
        fontBtn.setGeometry(700, 27, 80, 30)
        fontBtn.setToolTip('Change The Text Font')
        fontBtn.setCursor(QCursor(Qt.PointingHandCursor))
        fontBtn.setStyleSheet('QWidget {background-color:#505666; color: gray; font-weight:Bold; font-family:Segoe Print; font-size:20px} ')
        fontBtn.clicked.connect(self.fontChoice)


        colorBtn = QPushButton('Color', self)
        colorBtn.setGeometry(800, 27, 80, 30)
        colorBtn.setToolTip('Change The Text Color')
        colorBtn.setCursor(QCursor(Qt.PointingHandCursor))
        colorBtn.setStyleSheet('QWidget {background-color:#505666; color: gray; font-weight:Bold; font-family:Segoe Print; font-size:20px;} ')
        colorBtn.clicked.connect(self.colorChoice)


    ### choose window style

        self.styleLbl = QLabel('Window Style', self)
        self.styleLbl.setGeometry(300, 31, 100, 20)
        self.styleLbl.setStyleSheet('QWidget {background-color:#383C4A ;color: gray; font-weight:Bold; font-family:Segoe Print; font-size:13px} ')

        cmBox = QComboBox(self)
        cmBox.move(400, 27)
        cmBox.setCursor(QCursor(Qt.PointingHandCursor))
        cmBox.setStyleSheet('QWidget {color: white; font-style:italic; font-family:Capture it; font-size:13px} ')
        cmBox.addItems((
            'Windows',
            'Gtk',
            'cde',
            'plastique',
            'Cleanlooks'
        ))

        cmBox.activated[str].connect(self.windowStyle)

#########################################################

    def TextEditor(self):
        self.edt = QTextEdit()
        self.edt.setStyleSheet('QWidget {font-size:20px}')
        self.setCentralWidget(self.edt)


    def readText(self):
        return self.edt.toPlainText()

    def readTextAgain(self):
        return self.edt.toPlainText()




###############################################
    ## actions methods
    @pyqtSlot()
    #### File Menue Actions

    def opnFle(self):
        try:
            self.opnFile = QFileDialog.getOpenFileName(self, 'Open New File')
            self.TextEditor()
            with open(self.opnFile, 'r') as file:
                self.edt.setText(file.read())
            self.dirctory = self.dirctory + getcwd()
        except FileNotFoundError:
            pass

    def saveMe(self):
        if self.dirctory == '':
            self.saveMeAs()
        else:
            try:
                with open(self.opnFile, 'w') as file:
                    file.write(self.edt.toPlainText())
            except:
                pass

    def saveMeAs(self):
        try:
            saveAs = QFileDialog.getSaveFileName(self, 'Save As...')
            newText = self.edt.toPlainText()
            with open(saveAs, 'w') as file:
                file.write(newText)
        except :
            pass

    def closeMe(self):

        if self.compareText == self.readTextAgain():

            self.close()
            try:
                self.About.close()
            except:
                pass

        else:
            msgBox = QMessageBox.question(self, 'Save Changes', 'Do you want to save the changes before closing?', QMessageBox.Save | QMessageBox.Discard| QMessageBox.Cancel)

            if msgBox == QMessageBox.Discard:
                self.close()
                try:
                    self.About.close()
                except:
                    pass
            elif msgBox == QMessageBox.Save:
                self.saveMeAs()
            else:
                pass

    ##########################################
    ### EDit Menue Actions

    def cutText(self):
        return self.edt.cut()

    def copyText(self):
        return self.edt.copy()

    def pasteText(self):
        return self.edt.paste()

    def undoMe(self):
        return self.edt.undo()

    def redoMe(self):
        return self.edt.redo()
    def selectAll(self):
        return self.edt.selectAll()


    ## about me

    def aboutMe(self):

        self.About = About()

        self.About.show()

  ###################################3
  #### tool bar actions

    def windowStyle(self, text):
        self.styleLbl.setText(text)
        QApplication.setStyle(QStyleFactory.create(text))


    def fontChoice(self):
        font, valid = QFontDialog.getFont()
        if valid:
            self.edt.setFont(font)

    def colorChoice(self):
        clr = QColorDialog.getColor()
        self.edt.setStyleSheet('QWidget {color: %s} ' %clr.name()
        )



class About(QWidget):
    def __init__(self):
        super(About, self).__init__()

        self.setWindowFlags(Qt.Window)
        self.setWindowTitle('About TEditor')
        self.setMaximumWidth(300)
        self.setMaximumHeight(300)
        self.setMinimumHeight(300)
        self.setMinimumWidth(300)
        self.setStyleSheet('QWidget {background-color:#383C4A;}')

        imgLbl =QLabel(self)
        imge = QPixmap("icons/teditor.png")
        resizedImge = imge.scaled(64, 64, Qt.KeepAspectRatio)
        imgLbl.setPixmap(resizedImge)
        imgLbl.move(120, 30)

        titleLbl = QLabel('TEditor V0.1.0', self)
        titleLbl.move(30, 110)
        titleLbl.setStyleSheet('QWidget {color:#D3DAE3; font-family:Segoe Script; font-size:30px; font-weight:bold}')
        textLbl = QLabel('TEditor is a fast text editor for \n '
                         '    all Desktop Environments', self)
        textLbl.setStyleSheet('QWidget {font-size:15px}')
        textLbl.move(50, 155)

        authorLbl = QLabel('Coded by:\nHussam El Husseiny', self)
        authorLbl.move(3, 250)

        extBtn = QPushButton(QIcon('icons/abtcls.png'),'Close', self)
        extBtn.move(200,250)
        extBtn.setCursor(QCursor(Qt.PointingHandCursor))
        extBtn.setStyleSheet('QWidget {font-weight:bold; font-size:13px}')
        extBtn.clicked.connect(self.close)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TEditor()
    window.show()
    sys.exit(app.exec_())
