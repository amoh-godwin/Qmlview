# -*- coding: utf-8 -*-
import sys
import os
from PyQt5.QtCore import QUrl, QResource
from PyQt5.QtGui import QGuiApplication, QIcon
from PyQt5.QtQml import QQmlApplicationEngine
from func import FixQml, Check
from frame import PhoneFrame

QResource.registerResource("resource.rcc")

app = QGuiApplication(sys.argv)
app.setWindowIcon(QIcon(':/icons/logo.png'))
engine = QQmlApplicationEngine()

def chk_style():
    # check if it contains styling
    chk = Check(sys.argv[1])
    style_name = chk.check_style()

    #os.environ['QT_QUICK_CONTROLS_STYLE'] = style_name

    if style_name:
        os.environ['QT_QUICK_CONTROLS_STYLE'] = style_name


def _construct_Qurl(path):
    url = QUrl()
    url.setScheme("file")
    raw_path = "/" + os.path.dirname(path) + "/"
    url.setPath(raw_path)
    return url


def fix_qml():
    # fix if it is a component
    fix = FixQml(sys.argv[1])
    chk = Check(sys.argv[1])
    status = chk.check_for_parent()

    if status:
        engine.load(sys.argv[1])
    else:
        ret_data = fix.put_in_parent()
        url = _construct_Qurl(sys.argv[1])
        engine.loadData(bytes(ret_data, 'utf-8'), url)

    # check for qml loading errors and exit the app
    if engine.rootObjects():
        pass
    else:
        sys.exit(1)


def put_into_frame():

    chk = Check(sys.argv[1])
    status = chk.check_for_parent()

    if status:
        pass
    else:
        pass


def run():
    # run the for engine
    chk_style()
    # contains the call to the engine
    fix_qml()


def run_in_frame():

    chk_style()

    put_into_frame()

if len(sys.argv) > 1:
    # check if it comes with parameters
    if len(sys.argv) > 2 and sys.argv[2] == '-phone':
        # has a parameter
        run_in_frame()
    else:
        # it has no other parameter
        run()
else:
    print('Usage: qmlview file or ./qmlview file')
    sys.exit(2)

sys.exit(app.exec_())
