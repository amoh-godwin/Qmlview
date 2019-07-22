# -*- coding: utf-8 -*-
import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QGuiApplication, QIcon
from PyQt5.QtQml import QQmlApplicationEngine
from failproof import FixQml

app = QGuiApplication(sys.argv)
app.setWindowIcon(QIcon('./resources/icons/logo.png'))
engine = QQmlApplicationEngine()


def run():

    fix = FixQml(sys.argv[1])
    status, ret_data = fix.handle()
    
    if status:
        engine.load(sys.argv[1])
    else:
        engine.loadData(bytes(ret_data, 'utf-8'), QUrl(sys.argv[1]))


if len(sys.argv) > 1:
    run()
else:
    print('Usage: qmlview file or ./qmlview file')

sys.exit(app.exec_())
