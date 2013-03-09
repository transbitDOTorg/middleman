import sys
from PyQt4 import QtGui, QtCore, QtWebKit
from PyQt4.QtCore import Qt



class selectionWindow(QtGui.QWidget):
    def __init__(self, parent=None, loadNextItemHandle=None):
        QtGui.QWidget.__init__(self, parent)

        self.loadNextItemHandle = loadNextItemHandle

        # The setGeometry method is used to position the control.
        # Order: X, Y position - Width, Height of control.
        self.setGeometry(0, 0, 1000, 120)

        self.setToolTip('Please select whether you would like to save or discard the item being shown below.')
        QtGui.QToolTip.setFont(QtGui.QFont('Helvetica', 12))

        btnWant = QtGui.QPushButton('Save this item.', self)
        btnWant.setGeometry(10, 12, 150, 60)
        btnWant.clicked.connect(self.want)

        btnHate = QtGui.QPushButton('Load next item.', self)
        btnHate.setGeometry(170, 12, 150, 60)
        btnHate.clicked.connect(self.loadNextItemHandle)

        btnHelp = QtGui.QPushButton('Help!', self)
        btnHelp.setGeometry(330, 12, 60, 60)

        btnExit = QtGui.QPushButton('Settings', self)
        btnExit.setGeometry(400, 12, 70, 60)
        btnExit.clicked.connect(quit) # @todo implement settings

        # Instance variables that need to be dynamic, accessible from parent
        self.displayArea = QtGui.QLabel(self)
        self.displayArea.setGeometry(480, 12, 230, 60)

        self.imageArea = QtWebKit.QWebView(self)
        self.imageArea.setGeometry(715, 2, 140, 80)

        self.sellerAttributes = QtGui.QLabel(self)
        self.sellerAttributes.setGeometry(855, 12, 140, 60)

    def want(self):
        self.loadNextItemHandle

    def loadNextItem(self):
        print self.app.loadNextItem();

class mainApp():
    def __init__(self, parser):
        self.parser = parser
        self.app = QtGui.QApplication(sys.argv)
        self.scene = QtGui.QGraphicsScene()
        self.web = QtWebKit.QWebView()
        # Construct window and view @todo rewrite, separate into appropriate methods
        self.mainForm = selectionWindow(self.web, self.loadNextItem)
        self.mainForm.setAutoFillBackground(True)
        self.mainPalette = self.mainForm.palette()
        self.mainPalette.setColor(self.mainForm.backgroundRole(), QtCore.Qt.white)
        self.mainForm.setPalette(self.mainPalette)
        self.web.setGeometry(0, 0, 1020, 700)

    def displayHelp(self):
        self.web.load(QtCore.QUrl("http://transbit.org/middlemanhelp.html")) # @todo localize this

    def display(self):
        self.scene.addWidget(self.web)
        self.web.load(QtCore.QUrl("http://transbit.org/middlemansplash.html")) # @todo localize this
        self.scene.addWidget(self.mainForm)
        self.view = QtGui.QGraphicsView(self.scene)
        self.view.setWindowTitle("Middleman")
        self.view.show()
        self.view.resize(1030, 710)
        self.app.exec_()

    def render(self, price, product, image, minOrder, assessed, escrow, goldYears, inspected):
        append = "..." if len(str(product)) > 25 else ""
        formatString = "Item: {0}{1}<div style='color:{2}; display:inline;'>{3}</div><div style='color:{4}; display:inline;'>Min. Order: {5}</div>"
        #@todo cleanup below line
        self.mainForm.displayArea.setText(formatString.format(str(product)[0:25], append, "red" if price == "N/A" else "green", "Price: "+price, "black", str(minOrder)))
        self.mainForm.imageArea.load(QtCore.QUrl(image))
        self.mainForm.displayArea.setToolTip(product)
        formatString = ""
        self.mainForm.sellerAttributes.setText(self.renderBoolean("Gold", goldYears != 0) + self.renderBoolean("Escrow", escrow) + self.renderBoolean("Onsite Checked: ", inspected))

    def loadNextItem(self):
        QtGui.QApplication.setOverrideCursor(Qt.WaitCursor)
        item =  self.parser.serveNextItem()
        print item
        self.web.load(QtCore.QUrl("http://camelcamelcamel.com/search?sq="+item["name"]))
        # This line is really ugly.  I apologize to all who have the misfortune of reading it.  @todo clean up this line
        self.render(self.extractParamIfExists(item, "FOB Price"), item["name"], self.extractParamIfExists(item, "image"), self.extractParamIfExists(item, "Min. Order"), self.extractParamIfExists(item, "isAssessed"), self.extractParamIfExists(item, "isEscrow"), self.extractParamIfExists(item, "goldYears"), self.extractParamIfExists(item, "isOnsiteCheck"))
        QtGui.QApplication.restoreOverrideCursor()

    # @todo cleanup and document
    def renderBoolean(self, descriptor, hasAttribute):
        formatString = "<div style='color: " + ("green" if hasAttribute else "red") + "'>"+ str(descriptor) + ": " + self.chooseCharacter(hasAttribute) + "</div>"
        return formatString

    def extractParamIfExists(self, dict, key):
        try:
            return dict[key]
        except:
            return "N/A"

    def chooseCharacter(self, boolean):
        return "YES" if boolean else "NO"