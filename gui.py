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
        self.displayArea.setGeometry(470, 12, 230, 60)

        self.imageArea = QtWebKit.QWebView(self);
        self.imageArea.setGeometry(700, 2, 140, 80)

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
        # Construct window and view @todo rewrite, separate into appropriate methods
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

    def render(self, price, product, image, minOrder):
        self.mainForm.displayArea.setText("Item: {0}<div style='color:{1}; display:inline;'>{2}</div><div style='color:{3}; display:inline;'>{4}</div>".format(str(product)[0:25], "green", str(price)), "black", minOrder)
        self.mainForm.imageArea.load(QtCore.QUrl(image))
        self.mainForm.displayArea.setToolTip(product)

    def loadNextItem(self):
        QtGui.QApplication.setOverrideCursor(Qt.WaitCursor)
        item =  self.parser.serveNextItem()
        print item
        self.web.load(QtCore.QUrl("http://camelcamelcamel.com/search?sq="+item["name"]))
        self.render(self.extractParamIfExists(item, "FOB Price"), item["name"], self.extractParamIfExists(item, "image"), self.extractParamIfExists("Min. Order"))
        QtGui.QApplication.restoreOverrideCursor()

    # Return "red" when colorBoolean is false,
    # green otherwise
    def chooseColor(self, colorBoolean):
        return "green" if colorBoolean else "red"

    def extractParamIfExists(self, dict, key):
        try:
            return dict[key]
        except:
            return "N/A"