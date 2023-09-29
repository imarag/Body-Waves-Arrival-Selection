from PyQt5.QtWidgets import QPushButton, QPlainTextEdit, QMainWindow, QAction, QComboBox,QLabel, QScrollArea, QColorDialog, QLineEdit, QApplication, QWidget, QVBoxLayout, QRadioButton, QButtonGroup, QHBoxLayout, QFileDialog, QMessageBox,QToolBar, QCheckBox 
from PyQt5.Qt import Qt
from PyQt5 import QtGui


class test(QScrollArea):
    def __init__(self):
        super().__init__()

        self.setWidgetResizable(True)

        # scrollContent = QWidget()
        # self.setWidget(scrollContent)

        scrollLayout = QVBoxLayout()
        self.setLayout(scrollLayout)

        items = [QPushButton('btdddddddddddddddddddddddddddddddd' + str(i)) for i in range(10)]
        for item in items:
            scrollLayout.addWidget(item)
        # scroll.setWidget(scrollContent)





class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        button = QPushButton("Press Me!")
        button.clicked.connect(self.the_button_was_clicked)

        # Set the central widget of the Window.
        self.setCentralWidget(button)

    def the_button_was_clicked(self):
        self.window2 = test()
        # self.window2.setFixedHeight(300)
        # self.window2.setFixedWidth(300)
        self.window2.resize(300, 300)
        self.window2.show()


app = QApplication([])

window = MainWindow()
window.show()

app.exec()
