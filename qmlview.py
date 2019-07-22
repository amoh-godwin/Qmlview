# -*- coding: utf-8 -*-
import sys
from PyQt5.QtGui import QGuiApplication, QIcon
from PyQt5.QtQml import QQmlApplicationEngine

app = QGuiApplication(sys.argv)
app.setWindowIcon(QIcon('./resources/icons/logo.png'))
engine = QQmlApplicationEngine()


def run():

    engine.load(sys.argv[1])


if len(sys.argv) > 1:
    run()
else:
    print('Usage: qmlview file or ./qmlview file')

sys.exit(app.exec_())
