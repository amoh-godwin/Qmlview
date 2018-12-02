# -*- coding: utf-8 -*-
import sys
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine

def run():
    
    engine.load(sys.argv[1])

app = QGuiApplication(sys.argv)
engine = QQmlApplicationEngine()

if len(sys.argv) > 1:
    run()
else:
    print('Usage: qmlview file')

sys.exit(app.exec_())