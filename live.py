"""
Module for Live Reloading
"""
import threading
from time import sleep

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QFile, QResource, QIODevice


QResource.registerResource("_qmlview_resource_.rcc")


class Live(QObject):


    """
    """


    def __init__(self):
        QObject.__init__(self)
        #self.engine = engine
    
    updated = pyqtSignal(str, arguments=['updater'])

    def _initialiase(self):
        self._call_auto_reload()

    def _call_auto_reload(self):
        a_thread = threading.Thread(target=self._auto_reload)
        a_thread.daemon = True
        a_thread.start()

    def _auto_reload(self):
        self.updater()

    @pyqtSlot()
    def caller(self):
        self._initialiase()

    def updater(self):
        self.updated.emit('Saladine')
