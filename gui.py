import sys
from PyQt4 import QtGui, QtCore, QtWebKit
from PyQt4.QtCore import Qt



class selectionWindow(QtGui.QWidget):
    def __init__(self, parent=None, loadNextItemHandle=None):
        QtGui.QWidget.__init__(self, parent)

        self.loadNextItemHandle = loadNextItemHandle

        # The setGeometry method is used to position the control.
        # Order: X, Y position - Width, Height of control.
        self.setGeometry(0, 0, 800, 120)

        self.setToolTip('Please select whether you would like to save or discard the item being shown below.')
        QtGui.QToolTip.setFont(QtGui.QFont('Helvetica', 12))

        btnWant = QtGui.QPushButton('Save this item.', self)
        btnWant.setGeometry(10, 12, 150, 60)

        btnHate = QtGui.QPushButton('Load next item.', self)
        btnHate.setGeometry(170, 12, 150, 60)
        btnHate.clicked.connect(self.loadNextItemHandle)

        btnHelp = QtGui.QPushButton('Help!', self)
        btnHelp.setGeometry(330, 12, 60, 60)

        btnExit = QtGui.QPushButton('Exit', self)
        btnExit.setGeometry(400, 12, 60, 60)
        btnExit.clicked.connect(quit)

        self.displayArea = QtGui.QLabel(self)
        self.displayArea.setGeometry(470, 12, 200, 60)

    def want(self, loadNextItemHandle):
        self.loadNextItemHandle

    def loadNextItem(self):
        print self.app.loadNextItem();

class mainApp():
    def __init__(self, parser):
        self.parser = parser
        self.app = QtGui.QApplication(sys.argv)
        self.scene = QtGui.QGraphicsScene()
        self.web = QtWebKit.QWebView()
        self.web.resize(1000, 500)
        # Construct window and view @todo rewrite
        self.mainForm = selectionWindow(self.web, self.loadNextItem)
        self.mainForm.setAutoFillBackground(True)
        self.mainPalette = self.mainForm.palette()
        self.mainPalette.setColor(self.mainForm.backgroundRole(), QtCore.Qt.white)
        self.mainForm.setPalette(self.mainPalette)

    def display(self):
        self.web.load(QtCore.QUrl("http://transbit.org/middlemansplash.html")) # @todo localize this
        self.scene.addWidget(self.web)
        self.scene.addWidget(self.mainForm)
        self.view = QtGui.QGraphicsView(self.scene)
        self.view.setWindowTitle("Middleman")
        self.view.show()
        self.app.exec_()

    def render(self, price, product):
        self.mainForm.displayArea.setText("Item: {0}<br>Price:<div style='color:{1}; display:inline;'>{2}</div>".format(str(product), "green", str(price)))

    def loadNextItem(self):
        QtGui.QApplication.setOverrideCursor(Qt.WaitCursor)
        item =  self.parser.serveNextItem()
        print item
        self.web.load(QtCore.QUrl("http://camelcamelcamel.com/search?sq="+item["name"]))
        self.render(self.extractParamIfExists(item, "price"), item["name"])
        QtGui.QApplication.restoreOverrideCursor()

    def extractParamIfExists(self, dict, key):
        try:
            return dict[key]
        except:
            return "N/A"

