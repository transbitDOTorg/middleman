import sys, time
from PyQt4 import QtGui, QtCore, QtWebKit, QtScript

class selectionWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        # The setGeometry method is used to position the control.
        # Order: X, Y position - Width, Height of control.
        self.setGeometry(0, 0, 680, 100)

        self.setToolTip('Please select whether you would like to save or <br>discard the item being shown below.')
        QtGui.QToolTip.setFont(QtGui.QFont('Helvetica', 12))

        btnWant = QtGui.QPushButton('Save this item.', self)
        btnWant.setGeometry(10, 12, 150, 60)

        btnHate = QtGui.QPushButton('Discard this item.', self)
        btnHate.setGeometry(170, 12, 150, 60)

        btnHelp = QtGui.QPushButton('Help!', self)
        btnHelp.setGeometry(330, 12, 60, 60)

        btnExit = QtGui.QPushButton('Exit', self)
        btnExit.setGeometry(400, 12, 60, 60)

        #btnExit = QtGui.QPushButton('Amazon', self)
        #btnExit.setFlat(True)
        #btnExit.setGeometry(470, 12, 60, 60)

        #btnExit = QtGui.QPushButton('BestBuy', self)
        #btnExit.setGeometry(540, 12, 60, 60)

        #btnExit = QtGui.QPushButton('NewEgg', self)
        #btnExit.setGeometry(610, 12, 60, 60)

        self.connect(btnWant, QtCore.SIGNAL('clicked()'), QtGui.qApp, QtCore.SLOT('quit()'))

class mainApp:
	def __init__(self):
		self.app = QtGui.QApplication(sys.argv)
		self.scene = QtGui.QGraphicsScene()
		self.web = QtWebKit.QWebView()
		self.mainForm = selectionWindow(self.web)
		self.mainForm.setAutoFillBackground(True)
		self.mainPalette = self.mainForm.palette()
		self.mainPalette.setColor(self.mainForm.backgroundRole(), QtCore.Qt.white)
		self.mainForm.setPalette(self.mainPalette)
	def display(self):
		self.web.load(QtCore.QUrl("http://camelcamelcamel.com/"))
		self.scene.addWidget(self.web)
		self.scene.addWidget(self.mainForm)
		self.view = QtGui.QGraphicsView(self.scene)
		self.view.setWindowTitle("MiddleMan - Main View")
		self.view.show()
		self.app.exec_()
	def render(self, price):
		# Update 	
		pass
