# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PondUI.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QLabel,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QWidget,
)
from ui.resources import resources_rc


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1080, 720)
        MainWindow.setStyleSheet("background-color: #FAFAFA;")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pondnameLabel = QLabel(self.centralwidget)
        self.pondnameLabel.setObjectName("pondnameLabel")
        self.pondnameLabel.setGeometry(QRect(300, 30, 480, 41))
        self.pondnameLabel.setStyleSheet(
            'font: 700 36pt "Times New Roman";\n' "color: rgb(0, 0, 0);"
        )
        self.pondnameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.buttonsFrame = QFrame(self.centralwidget)
        self.buttonsFrame.setObjectName("buttonsFrame")
        self.buttonsFrame.setGeometry(QRect(100, 480, 880, 61))
        self.buttonsFrame.setStyleSheet("border: 1px solid black;")
        self.buttonsFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.buttonsFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.sendfishButton = QPushButton(self.buttonsFrame)
        self.sendfishButton.setObjectName("sendfishButton")
        self.sendfishButton.setGeometry(QRect(330, 10, 230, 41))
        self.sendfishButton.setStyleSheet(
            'font: 600 18pt "Times New Roman";\n'
            "background-color: #FE9F06;\n"
            "border: none;\n"
            "border-radius: 8px;"
        )
        self.addfishButton = QPushButton(self.buttonsFrame)
        self.addfishButton.setObjectName("addfishButton")
        self.addfishButton.setGeometry(QRect(60, 10, 230, 41))
        self.addfishButton.setStyleSheet(
            'font: 600 18pt "Times New Roman";\n'
            "background-color: #66CC99;\n"
            "border: none;\n"
            "border-radius: 8px;"
        )
        self.connectButton = QPushButton(self.buttonsFrame)
        self.connectButton.setObjectName("connectButton")
        self.connectButton.setGeometry(QRect(600, 10, 230, 41))
        self.connectButton.setStyleSheet(
            'font: 600 18pt "Times New Roman";\n'
            "background-color: #B0AFE6;\n"
            "border: none;\n"
            "border-radius: 8px;"
        )
        self.mainFrame = QFrame(self.centralwidget)
        self.mainFrame.setObjectName("mainFrame")
        self.mainFrame.setGeometry(QRect(159, 110, 771, 341))
        self.mainFrame.setStyleSheet(
            "background-color: #F5F5F5;\n"
            "image: url(:/pond/Asset/pond.png);\n"
            "border: 1px solid black;"
        )
        self.mainFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.mainFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName("frame")
        self.frame.setGeometry(QRect(50, 639, 161, 51))
        self.frame.setStyleSheet("border: 1px solid black;")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.fashLabel = QLabel(self.frame)
        self.fashLabel.setObjectName("fashLabel")
        self.fashLabel.setGeometry(QRect(20, 10, 111, 31))
        font = QFont()
        font.setFamilies(["Times New Roman"])
        font.setPointSize(18)
        self.fashLabel.setFont(font)
        self.fashLabel.setStyleSheet("color:rgb(0, 0, 0)")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate("MainWindow", "MainWindow", None)
        )
        self.pondnameLabel.setText(
            QCoreApplication.translate("MainWindow", "Pond DC Universe ", None)
        )
        self.sendfishButton.setText(
            QCoreApplication.translate("MainWindow", "Send Fish", None)
        )
        self.addfishButton.setText(
            QCoreApplication.translate("MainWindow", "Add Fish", None)
        )
        self.connectButton.setText(
            QCoreApplication.translate("MainWindow", "Connect to MQTT", None)
        )
        self.fashLabel.setText(
            QCoreApplication.translate("MainWindow", "Fishes: 0", None)
        )

    # retranslateUi
