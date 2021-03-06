from PyQt5.QtWidgets import QHBoxLayout, QTreeView, QFileSystemModel
from PyQt5.QtCore import Qt, pyqtSignal, QProcess, QDir
from PyQt5.QtGui import QFont, QColor, QPalette
from utils.config import config_reader
from widgets.Messagebox import MessageBox
config0 = config_reader(0)
config1 = config_reader(1)
config2 = config_reader(2)

with open("default.json") as choice:
    choiceIndex = int(choice.read())

if choiceIndex == 0:
    editor = config0['editor']
elif choiceIndex == 1:
    editor = config1['editor']
elif choiceIndex == 2:
    editor = config2['editor']
else:
    editor = config0['editor']


class Directory(QTreeView):
    def __init__(self, callback, app=None, palette=None):  # TODO: App and palette will be passed from the Tabs class
        super().__init__()
        directoryFont = QFont()
        self.app = app
        self.palette = palette
        directoryFont.setFamily(editor["directoryFont"])
        directoryFont.setPointSize(editor["directoryFontSize"])
        self.open_callback = callback
        self.setFont(directoryFont)
        self.layout = QHBoxLayout()
        self.model = QFileSystemModel()
        self.setModel(self.model)
        self.model.setRootPath(QDir.rootPath())
        self.setMaximumWidth(300)
        self.setIndentation(10)
        self.setAnimated(True)

        self.setSortingEnabled(True)
        self.setWindowTitle("Dir View")
        self.hideColumn(1)
        self.resize(200, 600)
        self.hideColumn(2)
        self.confirmation = MessageBox()
        self.hideColumn(3)
        # self.layout.addWidget(self)
        self.doubleClicked.connect(self.openFile)

    def focusInEvent(self, event):
        # If we are focused then we change the selected item highlighting color
        self.focused = True
        self.palette.setColor(QPalette.Highlight, QColor(editor["HighlightColor"]).lighter())

        self.app.setPalette(self.palette)

    def focusOutEvent(self, event):
        # If we un focus from the QTreeView then we make the highlighted item color white
        self.palette.setColor(QPalette.Highlight, QColor(editor["UnfocusedHighlightColor"]).lighter())
        # self.clearSelection() Uncomment this if you want to remove all highlighting when unfocused
        self.app.setPalette(self.palette)

    def openDirectory(self, path):
        self.setRootIndex(self.model.index(path))

    def openFile(self, signal):
        file_path = self.model.filePath(signal)
        self.open_callback(file_path)
        return file_path

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Delete:

            try:
                self.fileObject = self.selectedIndexes()[0]
                fileName = self.model.filePath(self.fileObject)
                self.confirmation.run("Are you sure you want to delete ", str(fileName))

            except IndexError:
                print("No file selected")

