import sys, time
from PyQt4 import QtGui, QtCore, QtWebKit, QtScript

class browserWindow(QtWebKit.QWebView):
    def __init__(self, parent=None, child=None):
        super(browserWindow, self).__init__(parent)
        self.child = child

class selectionWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        #The setGeometry method is used to position the control.
        #Order: X, Y position - Width, Height of control.
        self.setGeometry(0, 0, 470, 80)

        self.setToolTip('Please select whether you would like to save or <br>discard the item being shown in the browser.')
        QtGui.QToolTip.setFont(QtGui.QFont('Helvetica', 12))

        btnWant = QtGui.QPushButton('Save this item.', self)
        btnWant.setGeometry(10, 12, 150, 60)

        btnHate = QtGui.QPushButton('Discard this item.', self)
        btnHate.setGeometry(170, 12, 150, 60)

        btnHelp = QtGui.QPushButton('Help!', self)
        btnHelp.setGeometry(330, 12, 60, 60)

        btnExit = QtGui.QPushButton('Exit', self)
        btnExit.setGeometry(400, 12, 60, 60)

        self.connect(btnWant, QtCore.SIGNAL('clicked()'), QtGui.qApp, QtCore.SLOT('quit()'))

app = QtGui.QApplication(sys.argv)
scene = QtGui.QGraphicsScene()
web = browserWindow()
mainForm = selectionWindow(web)
mainForm.setAutoFillBackground(True)
#mainPalette = mainForm.palette()
#mainPalette.setColor(mainForm.backgroundRole(), QtCore.Qt.black)
#mainForm.setPalette(mainPalette)
web.load(QtCore.QUrl("http://news.google.com/"))
scene.addWidget(web)
scene.addWidget(mainForm)
view = QtGui.QGraphicsView(scene)
view.setWindowTitle("MiddleMan - Main View")
view.show()
app.exec_()