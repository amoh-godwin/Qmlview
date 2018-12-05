# -*- coding: utf-8 -*-
import sys
from PyQt5.QtGui import QGuiApplication, QIcon
from PyQt5.QtQml import QQmlApplicationEngine


def run():

    engine.load(sys.argv[1])


app = QGuiApplication(sys.argv)
app.setWindowIcon(QIcon('./resources/icons/ic_airplay_white_18dp.png'))
engine = QQmlApplicationEngine()

if len(sys.argv) > 1:
    run()
else:
    print('Usage: qmlview file or ./qmlview file')

sys.exit(app.exec_())
