# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PondUI.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QLabel,
    QMainWindow, QPushButton, QSizePolicy, QWidget)
import ui.resources.resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1080, 720)
        MainWindow.setStyleSheet(u"background-color: #FAFAFA;")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.pondnameLabel = QLabel(self.centralwidget)
        self.pondnameLabel.setObjectName(u"pondnameLabel")
        self.pondnameLabel.setGeometry(QRect(350, 30, 381, 51))
        self.pondnameLabel.setStyleSheet(u"font: 700 36pt \"Times New Roman\";\n"
"color: rgb(0, 0, 0);")
        self.pondnameLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.buttonsFrame = QFrame(self.centralwidget)
        self.buttonsFrame.setObjectName(u"buttonsFrame")
        self.buttonsFrame.setGeometry(QRect(219, 480, 650, 61))
        self.buttonsFrame.setStyleSheet(u"border: 1px solid black;")
        self.buttonsFrame.setFrameShape(QFrame.NoFrame)
        self.addfishButton = QPushButton(self.buttonsFrame)
        self.addfishButton.setObjectName(u"addfishButton")
        self.addfishButton.setGeometry(QRect(50, 10, 250, 41))
        self.addfishButton.setStyleSheet(u"font: 600 18pt \"Times New Roman\";\n"
"background-color: #66CC99;\n"
"border: none;\n"
"border-radius: 8px;")
        self.connectButton = QPushButton(self.buttonsFrame)
        self.connectButton.setObjectName(u"connectButton")
        self.connectButton.setGeometry(QRect(350, 10, 250, 41))
        self.connectButton.setStyleSheet(u"font: 600 18pt \"Times New Roman\";\n"
"background-color: #B0AFE6;\n"
"border: none;\n"
"border-radius: 8px;")
        self.mainFrame = QFrame(self.centralwidget)
        self.mainFrame.setObjectName(u"mainFrame")
        self.mainFrame.setGeometry(QRect(159, 110, 771, 341))
        self.mainFrame.setStyleSheet(u"background-color: #F5F5F5;\n"
"image: url(:/pond/images/pond.png);\n"
"border: 1px solid black;")
        self.mainFrame.setFrameShape(QFrame.NoFrame)
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(50, 639, 161, 51))
        self.frame.setStyleSheet(u"border: 1px solid black;")
        self.frame.setFrameShape(QFrame.NoFrame)
        self.fashLabel = QLabel(self.frame)
        self.fashLabel.setObjectName(u"fashLabel")
        self.fashLabel.setGeometry(QRect(20, 10, 111, 31))
        font = QFont()
        font.setFamilies([u"Times New Roman"])
        font.setPointSize(18)
        self.fashLabel.setFont(font)
        self.fashLabel.setStyleSheet(u"color:rgb(0, 0, 0)")
        self.sendFrame = QFrame(self.centralwidget)
        self.sendFrame.setObjectName(u"sendFrame")
        self.sendFrame.setGeometry(QRect(219, 560, 651, 61))
        self.sendFrame.setStyleSheet(u"border: 1px solid black;")
        self.sendFrame.setFrameShape(QFrame.NoFrame)
        self.sendfishButton = QPushButton(self.sendFrame)
        self.sendfishButton.setObjectName(u"sendfishButton")
        self.sendfishButton.setGeometry(QRect(60, 10, 230, 41))
        self.sendfishButton.setStyleSheet(u"font: 600 18pt \"Times New Roman\";\n"
"background-color: #FE9F06;\n"
"border: none;\n"
"border-radius: 8px;")
        self.groupselectionbox = QComboBox(self.sendFrame)
        self.groupselectionbox.setObjectName(u"groupselectionbox")
        self.groupselectionbox.setGeometry(QRect(350, 10, 250, 41))
        self.groupselectionbox.setStyleSheet(u"font: 600 18pt \"Times New Roman\";\n"
"background-color: #e6e6e6;\n"
"border: none;\n"
"border-radius: 8px;")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.pondnameLabel.setText(QCoreApplication.translate("MainWindow", u"Pond DC Universe ", None))
        self.addfishButton.setText(QCoreApplication.translate("MainWindow", u"Add Fish", None))
        self.connectButton.setText(QCoreApplication.translate("MainWindow", u"Connect to MQTT", None))
        self.fashLabel.setText(QCoreApplication.translate("MainWindow", u"Fish: 0", None))
        self.sendfishButton.setText(QCoreApplication.translate("MainWindow", u"Send Fish", None))
    # retranslateUi

