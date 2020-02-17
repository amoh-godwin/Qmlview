# -*- coding: utf-8 -*-
import sys
import os
from base64 import b64decode
from PyQt5.QtCore import QUrl, QResource, QT_VERSION_STR
from PyQt5.QtGui import QGuiApplication, QIcon
from PyQt5.QtQml import QQmlApplicationEngine
from func import FixQml, Check
from frame import PhoneFrame

from _qmlview_resource_ import rcc

rcc_data = b64decode(rcc)

with open('_qmlview_resource_.rcc', 'wb') as rcc_b:
    rcc_b.write(rcc_data)

QResource.registerResource("_qmlview_resource_.rcc")


def param_help():
    print_help()
    sys.exit(0)


def param_phone():
    run_in_frame()


def param_version():
    print(VERSION)
    sys.exit(0)


def cleanUp():
    pass


ERROR_CODES = {1: 'Qml rootObject Could Not Be Created', 2: 'File Not Found',
               3: 'Invalid Parameter'}
HELP_PARAMS = {
        '-version': param_version, '--version': param_version,
        '-v': param_version, '--v': param_version,
        '-help': param_help, '--help': param_help,
        '-h': param_help, '--h': param_help}
VERSION = 'Qt ' +  QT_VERSION_STR

PARAMS = {
        '-phone': param_phone, '--phone': param_phone,
        '-p': param_phone, '--p': param_phone,
        '-version': param_version, '--version': param_version,
        '-v': param_version, '--v': param_version,
        '-help': param_help, '--help': param_help,
        '-h': param_help, '--h': param_help
        }

PATH_EG = os.path.join(os.environ['USERPROFILE'], 'main.qml')

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


def print_help():
    print('''
Usage: qmlview source [Optional PARAMS]
               source The .qml file to be run. This should be a full path
          \t      [-phone, --phone, -p, --p] Runs source in phone mode
          \t      [help, --help, -h, --h] Prints this help screen.

eg:
    qmlview C:\\path\\to\\main.qml
                 or 
    qmlview C:\\path\\to\\main.qml --phone
Note: Help works even without a source specified.
''')


def main_run():
    if os.path.exists('_qmlview_resource.rcc'):
        os.remove('_qmlview_resource.rcc')

if len(sys.argv) > 1:
    
    # if help param
    if sys.argv[1] in HELP_PARAMS:
        # it is a parameter
        help_func = HELP_PARAMS[sys.argv[1]]
        # run that param function
        help_func()
    # if files exist
    elif os.path.exists(sys.argv[1]):
        pass
    else:
        print('qmlview error: File Not Found [{0}]'.format(sys.argv[1]))
        print('Please write Filepath in full.')
        print('    Eg:', PATH_EG)
        print('or Do: qmlview -help or --help: for help')
        sys.exit(2)

    # check if it comes with parameters

    if len(sys.argv) > 2:
        
        if sys.argv[2] in PARAMS:
            # has a parameter
            func = PARAMS[sys.argv[2]]
            # run that param function
            func()
        else:
            print('qmlview error: Invalid Parameter')
            print_help()
            sys.exit(3)
    else:
        # it has no other parameter
        run()

else:
    print('Usage: qmlview file or ./qmlview file')
    sys.exit(2)

sys.exit(app.exec_())
