# -*- coding: utf-8 -*-
import sys
import os
from PyQt5.QtCore import QUrl, QResource
from PyQt5.QtGui import QGuiApplication, QIcon
from PyQt5.QtQml import QQmlApplicationEngine
from func import FixQml, CheckStyle
QResource.registerResource("./resource")
app = QGuiApplication(sys.argv)
app.setWindowIcon(QIcon(':/icons/logo.png'))
engine = QQmlApplicationEngine()

def chk_style():
    # check if it contains styling
    chk = CheckStyle(sys.argv[1])
    style_name = chk.check_style()
    
    #os.environ['QT_QUICK_CONTROLS_STYLE'] = style_name

    if style_name:
        os.environ['QT_QUICK_CONTROLS_STYLE'] = style_name


def fix_qml():
    # fix if it is a component
    fix = FixQml(sys.argv[1])
    status, ret_data = fix.handle()

    if status:
        engine.load(sys.argv[1])
    else:
        engine.loadData(bytes(ret_data, 'utf-8'), QUrl(sys.argv[1]))

    # check for qml loading errors and exit the app
    if engine.rootObjects():
        pass
    else:
        sys.exit(1)


def run():
    # run the for engine
    chk_style()
    # contains the call to the engine
    fix_qml()


if len(sys.argv) > 1:
    run()
else:
    print('Usage: qmlview file or ./qmlview file')
    sys.exit(2)

sys.exit(app.exec_())
