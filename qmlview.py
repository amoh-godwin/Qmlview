# -*- coding: utf-8 -*-
import sys
import os
from base64 import b64decode
from PyQt5.QtCore import QUrl, QResource
from PyQt5.QtGui import QGuiApplication, QIcon
from PyQt5.QtQml import QQmlApplicationEngine
from func import FixQml, Check
from frame import PhoneFrame

from _qmlview_resource_ import rcc

rcc_data = b64decode(rcc)

with open('_qmlview_resource_.rcc', 'wb') as rcc_b:
    rcc_b.write(rcc_data)

QResource.registerResource("_qmlview_resource_.rcc")

ERROR_CODES = {1: 'Qml rootObject not created', 2: 'File Not Found',
               3: 'Invalid parameter'}

PATH_EG = os.path.join(os.environ['USERPROFILE'], 'main.qml')

def cleanUp():
    pass


app = QGuiApplication(sys.argv)
app.setWindowIcon(QIcon(':/icons/logo.png'))
app.aboutToQuit.connect(cleanUp)
engine = QQmlApplicationEngine()

def chk_style():
    # check if it contains styling
    chk = Check(sys.argv[1])
    style_name = chk.check_style()

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
        engine.quit.connect(app.quit)
        engine.load(sys.argv[1])
    else:
        ret_data = fix.put_in_parent()
        url = _construct_Qurl(sys.argv[1])
        engine.quit.connect(app.quit)
        engine.loadData(bytes(ret_data, 'utf-8'), url)

    # check for qml loading errors and exit the app
    if engine.rootObjects():
        pass
    else:
        sys.exit(1)

def put_into_frame():

    chk = Check(sys.argv[1])
    status = chk.check_for_parent()
    frm = PhoneFrame(sys.argv[1])

    if status:
        ret_data = frm.parentised_handling()
    else:
        ret_data = frm.unparentised_handling()

    ## Debugging block   
    print('****************')
    no = 0
    for line in ret_data.splitlines():
        no += 1
        print(no, line)
    print('****************')
    ## End of debuggin block

    url = _construct_Qurl(sys.argv[1])
    engine.quit.connect(app.quit)
    engine.loadData(bytes(ret_data, 'utf-8'), url)

def run():
    # run the for engine
    chk_style()
    # contains the call to the engine
    fix_qml()


def run_in_frame():

    chk_style()

    put_into_frame()


def main_run():
    if os.path.exists('_qmlview_resource.rcc'):
        os.remove('_qmlview_resource.rcc')

if len(sys.argv) > 1:
    
    # if files exist
    if os.path.exists(sys.argv[1]):
        pass
    else:
        print('qmlview error: File Not Found [{0}]'.format(sys.argv[1]))
        print('Please write Filepath in full.')
        print('    Eg:', PATH_EG)
        sys.exit(2)

    # check if it comes with parameters

    if len(sys.argv) > 2:
        if sys.argv[2] in ('-phone', '--phone'):
            # has a parameter
            run_in_frame()
        else:
            print('Usage: qmlview [file] [-phone, --phone]')
            print('qmlview error: invalid parameter')
            sys.exit(3)
    else:
        # it has no other parameter
        run()

else:
    print('Usage: qmlview file or ./qmlview file')
    sys.exit(2)

sys.exit(app.exec_())
