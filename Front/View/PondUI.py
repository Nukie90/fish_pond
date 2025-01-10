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
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QMainWindow,
    QPushButton, QSizePolicy, QWidget)
import Front.View.picture_rc as picture_rc

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
        self.pondnameLabel.setGeometry(QRect(300, 30, 480, 41))
        self.pondnameLabel.setStyleSheet(u"font: 700 36pt \"Times New Roman\";")
        self.pondnameLabel.setAlignment(Qt.AlignCenter)
        self.buttonsFrame = QFrame(self.centralwidget)
        self.buttonsFrame.setObjectName(u"buttonsFrame")
        self.buttonsFrame.setGeometry(QRect(100, 480, 880, 61))
        self.buttonsFrame.setStyleSheet(u"border: 1px solid black;")
        self.buttonsFrame.setFrameShape(QFrame.StyledPanel)
        self.buttonsFrame.setFrameShadow(QFrame.Raised)
        self.removefishButton = QPushButton(self.buttonsFrame)
        self.removefishButton.setObjectName(u"removefishButton")
        self.removefishButton.setGeometry(QRect(330, 10, 230, 41))
        self.removefishButton.setStyleSheet(u"font: 600 18pt \"Times New Roman\";\n"
"background-color: #FF6666;\n"
"border: none;\n"
"border-radius: 8px;")
        self.addfishButton = QPushButton(self.buttonsFrame)
        self.addfishButton.setObjectName(u"addfishButton")
        self.addfishButton.setGeometry(QRect(60, 10, 230, 41))
        self.addfishButton.setStyleSheet(u"font: 600 18pt \"Times New Roman\";\n"
"background-color: #66CC99;\n"
"border: none;\n"
"border-radius: 8px;")
        self.connectButton = QPushButton(self.buttonsFrame)
        self.connectButton.setObjectName(u"connectButton")
        self.connectButton.setGeometry(QRect(600, 10, 230, 41))
        self.connectButton.setStyleSheet(u"font: 600 18pt \"Times New Roman\";\n"
"background-color: #B0AFE6;\n"
"border: none;\n"
"border-radius: 8px;")
        self.mainFrame = QFrame(self.centralwidget)
        self.mainFrame.setObjectName(u"mainFrame")
        self.mainFrame.setGeometry(QRect(159, 110, 771, 341))
        self.mainFrame.setStyleSheet(u"background-color: #F5F5F5;\n"
"image: url(:/pond/Asset/pond.png);\n"
"border: 1px solid black;")
        self.mainFrame.setFrameShape(QFrame.StyledPanel)
        self.mainFrame.setFrameShadow(QFrame.Raised)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.pondnameLabel.setText(QCoreApplication.translate("MainWindow", u"Pond DC Universe ", None))
        self.removefishButton.setText(QCoreApplication.translate("MainWindow", u"Remove Fish", None))
        self.addfishButton.setText(QCoreApplication.translate("MainWindow", u"Add Fish", None))
        self.connectButton.setText(QCoreApplication.translate("MainWindow", u"Connect to MQTT", None))
    # retranslateUi

